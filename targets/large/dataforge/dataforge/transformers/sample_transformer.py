import random
from typing import List, Dict, Any
from .base import BaseTransformer

class SampleTransformer(BaseTransformer):
    """Return a random sample of records (for testing/dev pipelines)."""

    def __init__(self, sample_size: int = 100, seed: int = None, **kwargs):
        super().__init__(**kwargs)
        self.sample_size = sample_size
        self.seed = seed

    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if self.seed is not None:
            random.seed(self.seed)
        if len(data) <= self.sample_size:
            return data
        return random.sample(data, self.sample_size)
