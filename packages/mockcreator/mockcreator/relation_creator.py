# stdlib
from collections import OrderedDict
import random
from typing import Any
from typing import Dict
from typing import List

# third party
from creator import Creator
from faker import Faker
import pandas as pd

fake = Faker()


def _generate_matching_strings(original: List[str]) -> List[str]:
    return random.choices(original, k=len(original))


def _generate_fuzzy_strings(original: List[str]) -> List[str]:
    # TODO: generate actually fuzzy strings
    choices = random.choices(original, k=len(original))
    return [choice + "_" for choice in choices]


def _generate_no_match_strings(original: List[str]) -> List[str]:
    return [fake.pystr() for i in range(len(original))]


def _split_list_randomly(input_list, lengths):
    indexed_list = list(enumerate(input_list))
    random.shuffle(indexed_list)
    sublists = []
    original_indices = []
    start = 0

    for length_idx, length in enumerate(lengths):
        is_last = length_idx == len(lengths) - 1
        end = None if is_last else start + length
        indices, sublist = zip(*indexed_list[start:end])
        sublists.append(list(sublist))
        original_indices.append(list(indices))
        start = end

    return sublists, original_indices


def _generate_fuzzy_match_strings(original_list, weights):
    match_weight = weights.get("match", 0)
    fuzzy_weight = weights.get("fuzzy", 0)
    no_match_weight = weights.get("no_match", 0)
    total_weight = match_weight + fuzzy_weight + no_match_weight

    num_strings = len(original_list)
    num_matching = int(num_strings * match_weight / total_weight)
    num_fuzzy = int(num_strings * fuzzy_weight / total_weight)
    num_no_match = int(num_strings * no_match_weight / total_weight)

    lists, indices = _split_list_randomly(
        original_list, [num_matching, num_fuzzy, num_no_match]
    )

    return [
        *_generate_matching_strings(lists[0]),
        *_generate_fuzzy_strings(lists[1]),
        *_generate_no_match_strings(lists[2]),
    ]


class Field:
    def __init__(self, method: str) -> None:
        self.method = method

    def generate_data(self, params: Dict[str, Any], ref_data: pd.Series) -> List[Any]:
        raise NotImplementedError


class FuzzyMatch(Field):
    method: str = "fuzzy_match"

    def __init__(self) -> None:
        super().__init__(method=FuzzyMatch.method)

    def generate_data(self, params: Dict[str, Any], ref_data: pd.Series) -> List[Any]:
        weights = params["weights"]
        return _generate_fuzzy_match_strings(ref_data.tolist(), weights)


FIELD_MAP: Dict[str, Field] = {"fuzzy_match": FuzzyMatch()}


class RelationCreator(Creator):
    def __init__(
        self, metadata: Dict[str, Any] = None, generated: List[pd.DataFrame] = None
    ) -> None:
        super().__init__(metadata=metadata, generated=generated)

    def infer_metadata(self, series: pd.Series) -> Field:
        raise NotImplementedError

    def generate_data(
        self, method_name: str, params: Dict[str, Any], num_samples: int
    ) -> List[Any]:
        field = FIELD_MAP.get(method_name)
        if not field:
            raise ValueError(f"Unknown method {method_name}")

        splitted_ref = params["ref"].split(".")
        table = splitted_ref[0]
        field_name = splitted_ref[1]
        ordered_tables = OrderedDict(self.metadata["tables"])
        table_index = list(ordered_tables.keys()).index(table)
        ref_data = self.generated[table_index][field_name]
        return field.generate_data(params, ref_data)
