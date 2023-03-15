from faker import Faker
import pandas as pd
import yaml
from typing import Any, Dict, List, Union

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
        data: List[Dict[str, Any]] = []
        for _ in range(num_samples):
            sample: Dict[str, Any] = {}
            for feature_name, feature_params in self.metadata["fields"].items():
                faker_method = feature_params.get("faker")
                if faker_method:
                    faker_method_name, *faker_params = faker_method
                    value = getattr(fake, faker_method_name)(*faker_params)
                else:
                    value = None
                sample[feature_name] = value
            data.append(sample)

        return pd.DataFrame(data)

    @classmethod
    def from_yaml(cls, path: str) -> "MockCreator":
        with open(path, "r") as f:
            metadata = yaml.safe_load(f)
        return cls(metadata)
