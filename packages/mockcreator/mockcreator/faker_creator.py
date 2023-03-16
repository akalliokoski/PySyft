# stdlib
from typing import Any, Dict, List

# third party
from faker import Faker
import pandas as pd

# relative
from creator import Creator

fake = Faker()


class Field:
    def __init__(self, method: str) -> None:
        self.method = method

    def infer_metadata(self, series: pd.Series) -> Dict[str, Any]:
        raise NotImplementedError


class IntegerField(Field):
    method: str = "pyint"

    def __init__(self) -> None:
        super().__init__(method=IntegerField.method)

    def infer_metadata(self, series: pd.Series) -> Dict[str, Any]:
        return {
            "faker": self.method,
            "min_value": series.min().item(),
            "max_value": series.max().item(),
        }


class FloatField(Field):
    method: str = "pyfloat"

    def __init__(self) -> None:
        super().__init__(method=FloatField.method)

    def infer_metadata(self, series: pd.Series) -> Dict[str, Any]:
        return {
            "faker": self.method,
            "min_value": series.min().item(),
            "max_value": series.max().item(),
        }


class BooleanField(Field):
    method: str = "pybool"

    def __init__(self) -> None:
        super().__init__(method=BooleanField.method)

    def infer_metadata(self, series: pd.Series) -> Dict[str, Any]:
        return {"faker": self.method}


class StringField(Field):
    method: str = "pystr"

    def __init__(self) -> None:
        super().__init__(method=StringField.method)

    def infer_metadata(self, series: pd.Series) -> Dict[str, Any]:
        return {
            "faker": self.method,
            "min_chars": series.str.len().min().item(),
            "max_chars": series.str.len().max().item(),
        }


PANDAS_FIELD_MAP = {
    "int64": IntegerField(),
    "float64": FloatField(),
    "bool": BooleanField(),
    "string": StringField(),
    "object": StringField(),  # TODO
}


class FakerCreator(Creator):
    def __init__(self) -> None:
        super().__init__()

    def infer_metadata(self, series: pd.Series) -> Field:
        field_type = PANDAS_FIELD_MAP.get(series.dtype.name, Field)
        return field_type.infer_metadata(series)

    def generate_data(
        self, method_name: str, params: Dict[str, Any], num_samples: int
    ) -> List[Any]:
        if method_name is None:
            return [None] * num_samples

        fake_obj = fake
        fake_subs = method_name.split(".")[:-1]
        for sub in fake_subs:
            fake_obj = getattr(fake_obj, sub)

        args = params.pop("args", [])
        kwargs = params
        return list(
            [
                getattr(fake_obj, method_name)(*args, **kwargs)
                for _ in range(num_samples)
            ]
        )
