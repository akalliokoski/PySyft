# stdlib
from typing import Any
from typing import Dict
from typing import List

# third party
import pandas as pd


class Creator:
    def __init__(
        self, metadata: Dict[str, Any] = None, generated: List[pd.DataFrame] = None
    ) -> None:
        self.metadata = metadata
        self.generated = generated

    def infer_metadata(self, series: pd.Series) -> Dict[str, Any]:
        raise NotImplementedError

    def generate_data(
        self, method_name: str, params: Dict[str, Any], num_samples: int
    ) -> List[Any]:
        raise NotImplementedError
