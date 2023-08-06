from ..common.interfaces import AbstractMetric, TypeTimeSeries, TypeQuantiles, TypeDistribution
import numpy as np


class Metric(AbstractMetric):
    def __init__(self, meta, queue, test_start, raw=True, aggregate=False, **kw):
        super(Metric, self).__init__(meta, queue, test_start, raw=raw, aggregate=aggregate, **kw)
        self.dtypes = {
            'ts': np.int64,
            'value': np.float64
        }
        self.columns = ['ts', 'value']

    @property
    def type(self):
        return TypeTimeSeries

    @property
    def aggregate_types(self):
        return [TypeQuantiles, TypeDistribution]
