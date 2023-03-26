# stdlib
import random
from typing import Any
from typing import Dict
from typing import List

# third party
from creator import Creator
import pandas as pd


class Field:
    def __init__(self, method: str) -> None:
        self.method = method

    def get_kwargs(self, num_samples, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError

    def infer_metadata(self, series: pd.Series) -> Dict[str, Any]:
        raise NotImplementedError


class ChoicesField(Field):
    method: str = "choices"

    def __init__(self) -> None:
        super().__init__(method=ChoicesField.method)

    def get_kwargs(self, num_samples, **kwargs) -> Dict[str, Any]:
        return {**kwargs, "k": num_samples}

    def infer_metadata(self, series: pd.Series) -> Dict[str, Any]:
        normalized_counts = series.value_counts(normalize=True)
        return {
            "random": self.method,
            "args": [normalized_counts.index.tolist()],
            "weights": normalized_counts.tolist(),
        }


PANDAS_FIELD_FIELD_MAP: Dict[str, ChoicesField] = {
    "int64": ChoicesField(),
    "bool": ChoicesField(),
    "string": ChoicesField(),
    "object": ChoicesField(),
}

RANDOM_METHODS_FIELD_MAP: Dict[str, ChoicesField] = {"choices": ChoicesField()}


class RandomCreator(Creator):
    def __init__(
        self, metadata: Dict[str, Any] = None, generated: List[pd.DataFrame] = None
    ) -> None:
        super().__init__(metadata=metadata, generated=generated)

    def infer_metadata(self, series: pd.Series) -> Field:
        field_type = PANDAS_FIELD_FIELD_MAP.get(series.dtype.name, Field)
        return field_type.infer_metadata(series)

    def generate_data(
        self, method_name: str, params: Dict[str, Any], num_samples: int
    ) -> List[Any]:
        if method_name is None:
            return [None] * num_samples

        args = params.pop("args", [])
        field = RANDOM_METHODS_FIELD_MAP.get(method_name)

        if field:
            kwargs = field.get_kwargs(num_samples, **params)
            data = getattr(random, method_name)(*args, **kwargs)
        else:
            data = [
                getattr(random, method_name)(*args, **params)
                for _ in range(num_samples)
            ]
        return data
