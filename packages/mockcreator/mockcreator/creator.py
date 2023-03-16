# stdlib
from typing import Any, Dict, List

# third party
import pandas as pd


class Creator:
    def __init__(self) -> None:
        pass

    def infer_metadata(self, series: pd.Series) -> Dict[str, Any]:
        raise NotImplementedError

    def generate_data(
        self, method_name: str, params: Dict[str, Any], num_samples: int
    ) -> List[Any]:
        raise NotImplementedError
