# stdlib
from collections import OrderedDict
from typing import Any, Dict, List

# third party
import pandas as pd
import yaml

# relative
from creator import Creator
from faker_creator import FakerCreator
from random_creator import RandomCreator


CREATOR_MAP: Dict[str, Creator] = {
    "faker": FakerCreator(),
    "faker.unique": FakerCreator(),
    "random": RandomCreator(),
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
        creator = _get_creator(creator_name)
        inferred = creator.infer_metadata(series)
        metadata["fields"][column_name] = inferred

    name = hints.get("name", "table_" + str(df_index + 1))
    return (name, metadata)


def _generate_table_data(metadata: Dict[str, Any], num_samples: int) -> pd.DataFrame:
    data = {}
    for feature_name, params in metadata["fields"].items():
        ordered_params = OrderedDict(params)  ## TODO: is OrderedDict required?
        creator_name, method_name = ordered_params.popitem(0)

        creator = _get_creator(creator_name)
        feature = creator.generate_data(method_name, ordered_params, num_samples)
        data[feature_name] = feature
    return pd.DataFrame(data)


class MockCreator:
    def __init__(self, metadata: Dict[str, Any]) -> None:
        self.metadata = metadata

    def to_yaml(self, path: str) -> None:
        with open(path, "w") as f:
            yaml.dump(self.metadata, f, sort_keys=False)

    def set_field(self, table: str, field: str, metadata: Dict[str, Any]) -> None:
        tables = self.metadata.get("tables", {})
        fields = self.metadata.get(table, {"fields": {}})
        fields[field] = metadata
        self.metadata["tables"] = tables

    def generate_data(self, num_samples: int) -> List[pd.DataFrame]:
        dfs: List[pd.DataFrame] = []
        for _, table_metadata in self.metadata["tables"].items():
            dfs.append(_generate_table_data(table_metadata, num_samples))
        return dfs

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
