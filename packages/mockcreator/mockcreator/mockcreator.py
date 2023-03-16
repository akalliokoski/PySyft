from typing import Any, Dict, List, Union
import copy

from faker import Faker
import pandas as pd
import yaml

# relative
from fields import Field, IntegerField, FloatField, BooleanField


fake = Faker()

PANDAS_FIELD_TYPE_MAP = {
    "int64": IntegerField,
    "float64": FloatField,
    "bool": BooleanField,
    "object": Field,
}


class MockCreator:
    def __init__(self, metadata: Dict[str, Any]) -> None:
        self.metadata = metadata

    def to_yaml(self, path: str) -> None:
        with open(path, "w") as f:
            yaml.dump(self.metadata, f)

    def generate_data(self, num_samples: int) -> pd.DataFrame:
        data = []
        for _ in range(num_samples):
            sample = {}
            for feature_name, params in self.metadata["fields"].items():
                params = copy.deepcopy(params)
                faker_method_name = params.pop("faker", None)
                if faker_method_name is None:
                    continue

                args = params.pop("args", [])
                value = getattr(fake, faker_method_name)(*args, **params)
                sample[feature_name] = value
            data.append(sample)

        return pd.DataFrame(data)

    @classmethod
    def from_yaml(cls, path: str) -> "MockCreator":
        with open(path, "r") as f:
            metadata = yaml.safe_load(f)
        return cls(metadata)
