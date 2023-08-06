"""Simply returns the majority label from the train set."""

import pandas as pd

from ethicml.common import implements
from ethicml.algorithms.inprocess.in_algorithm import InAlgorithm
from ethicml.utility.data_structures import DataTuple, TestTuple


class Majority(InAlgorithm):
    """Simply returns the majority label from the train set."""

    @implements(InAlgorithm)
    def run(self, train: DataTuple, test: TestTuple) -> pd.DataFrame:
        maj = train.y.mode().to_numpy()
        return pd.DataFrame(maj.repeat(len(test.x)), columns=["preds"])

    @property
    def name(self) -> str:
        """Getter for algorithm name."""
        return "Majority"
