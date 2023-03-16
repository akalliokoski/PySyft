# stdlib
from collections import OrderedDict
from typing import Any, Dict

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


class MockCreator:
    def __init__(self, metadata: Dict[str, Any]) -> None:
        self.metadata = metadata

    def to_yaml(self, path: str) -> None:
        with open(path, "w") as f:
            yaml.dump(self.metadata, f, sort_keys=False)

    def set_metadata(self, field: str, metadata: Dict[str, Any]) -> None:
        self.metadata["fields"][field] = metadata

    def generate_data(self, num_samples: int) -> pd.DataFrame:
        data = {}
        for feature_name, params in self.metadata["fields"].items():
            ordered_params = OrderedDict(params)
            creator_name, method_name = ordered_params.popitem(0)

            creator = _get_creator(creator_name)
            feature = creator.generate_data(method_name, ordered_params, num_samples)
            data[feature_name] = feature
        return pd.DataFrame(data)

    @classmethod
    def from_yaml(cls, path: str) -> "MockCreator":
        with open(path, "r") as f:
            metadata = yaml.safe_load(f)
        return cls(metadata)

    @classmethod
    def from_dataframe(
        cls, df: pd.DataFrame, series_creators: Dict[str, str]
    ) -> "MockCreator":
        metadata = {
            "fields": {},
        }
        for column_name, series in df.iteritems():
            creator_name = series_creators.get(column_name, "faker")
            creator = _get_creator(creator_name)
            inferred = creator.infer_metadata(series)
            metadata["fields"][column_name] = inferred

        return cls(metadata)
