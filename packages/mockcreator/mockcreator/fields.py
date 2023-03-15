from faker import Faker
from typing import Any, Optional

fake = Faker()


class Field:
    def __init__(self) -> None:
        pass

    def generate(self) -> Any:
        raise NotImplementedError


class IntegerField(Field):
    def __init__(
        self, min_value: Optional[int] = None, max_value: Optional[int] = None
    ) -> None:
        super().__init__()
        self.min_value = min_value
        self.max_value = max_value

    def generate(self) -> int:
        return fake.pyint(min_value=self.min_value, max_value=self.max_value)


class FloatField(Field):
    def __init__(
        self,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.min_value = min_value
        self.max_value = max_value

    def generate(self) -> float:
        return fake.pyfloat(min_value=self.min_value, max_value=self.max_value)


class BooleanField(Field):
    def generate(self) -> bool:
        return fake.pybool()
