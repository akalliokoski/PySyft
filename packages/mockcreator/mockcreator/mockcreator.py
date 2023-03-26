# stdlib
from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List

# third party
from creator import Creator
from faker_creator import FakerCreator
import pandas as pd
from random_creator import RandomCreator
from relation_creator import RelationCreator
import yaml

CREATOR_MAP: Dict[str, Creator] = {
    "faker": FakerCreator,
    "faker.unique": FakerCreator,
    "random": RandomCreator,
    "relation": RelationCreator,
}


def _get_creator(creator_name: str) -> Creator:
    creator = CREATOR_MAP.get(creator_name, None)
    if creator is None:
        raise ValueError(f"Creator {creator_name} not found")
    return creator


def _dataframe_metadata(
    df: pd.DataFrame, hints: Dict[str, str] = {}, df_index: int = 0
) -> Dict[str, Any]:
    metadata = {
        "fields": {},
    }
    creators = hints.get("creators", {})
    for column_name, series in df.iteritems():
        creator_name = creators.get(column_name, "faker")
        creator = _get_creator(creator_name)()
        inferred = creator.infer_metadata(series)
        metadata["fields"][column_name] = inferred

    name = hints.get("name", "table_" + str(df_index + 1))
    return (name, metadata)


class MockCreator:
    def __init__(self, metadata: Dict[str, Any]) -> None:
        self.metadata = metadata
        self.generated: List[pd.DataFrame] = []

    def _generate_table_data(
        self, metadata: Dict[str, Any], num_samples: int
    ) -> pd.DataFrame:
        data = {}
        for feature_name, params in metadata["fields"].items():
            ordered_params = OrderedDict(params)
            creator_name, method_name = ordered_params.popitem(0)

            creator = _get_creator(creator_name)(self.metadata, self.generated)
            feature = creator.generate_data(method_name, ordered_params, num_samples)
            data[feature_name] = feature
        return pd.DataFrame(data)

    def to_yaml(self, path: str) -> None:
        with open(path, "w") as f:
            yaml.dump(self.metadata, f, sort_keys=False)

    def set_field(self, table: str, field: str, metadata: Dict[str, Any]) -> None:
        self.metadata["tables"][table]["fields"][field] = metadata

    def generate_data(self, num_samples: int) -> List[pd.DataFrame]:
        self.generated = []
        for _, table_metadata in self.metadata["tables"].items():
            self.generated.append(
                self._generate_table_data(table_metadata, num_samples)
            )
        return self.generated

    @classmethod
    def from_yaml(cls, path: str) -> "MockCreator":
        with open(path, "r") as f:
            metadata = yaml.safe_load(f)
        return cls(metadata)

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame, hints: Dict[str, Any]) -> "MockCreator":
        name, metadata = _dataframe_metadata(df, hints)
        tables = {"tables": {name: metadata}}
        return cls(tables)

    @classmethod
    def from_dataframes(
        cls, dfs: List[pd.DataFrame], hints=List[Dict[str, Any]]
    ) -> "MockCreator":
        metadata = {
            "tables": {},
        }
        for df_index, df in enumerate(dfs):
            df_hints = hints[df_index] if len(hints) > df_index else {}
            name, table_metadata = _dataframe_metadata(df, df_hints, df_index)
            metadata["tables"][name] = table_metadata
        return cls(metadata)
