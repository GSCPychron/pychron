import unittest
from types import SimpleNamespace

from pychron.graph.stream_graph import StreamGraph


def _fake_graph(data, calls):
    value = SimpleNamespace(get_data=lambda: data)
    plot = SimpleNamespace(plots={"a": [SimpleNamespace(value=value)]})
    return SimpleNamespace(
        plots=[plot],
        track_y_max=[True],
        track_y_min=[True],
        set_y_limits=lambda **kw: calls.append(kw),
    )


class StreamGraphUpdateYLimitsTestCase(unittest.TestCase):
    def setUp(self):
        self.calls = []
        self.graph = _fake_graph([1.0, 3.0], self.calls)

    def test_default_pad(self):
        StreamGraph.update_y_limits(self.graph, plotid=0)
        self.assertEqual(self.calls[0]["pad"], 5)
        self.assertEqual((self.calls[0]["min_"], self.calls[0]["max_"]), (1.0, 3.0))

    def test_caller_pad_overrides_default(self):
        # ScanManager passes pad="0.1"; this used to raise
        # "got multiple values for keyword argument 'pad'"
        StreamGraph.update_y_limits(self.graph, plotid=0, pad="0.1")
        self.assertEqual(self.calls[0]["pad"], "0.1")


if __name__ == "__main__":
    unittest.main()
