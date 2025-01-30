from actions.list_datasets import list_datasets
from actions.pollute import pollute
from strategies.pollutions.depth_reduce import VirtualDepthReduceStrategy
from strategies.pollutions.samplerate_reduce import VirtualSamplerateReduceStrategy

# depth_reduce_strategy = VirtualDepthReduceStrategy(depth=10)
# pollute(depth_reduce_strategy, "../data/SALVE001/test", "../data/SALVE001/pollute/0003")
# print(list_datasets("../data/SALVE001"))
samplerate_reduce_strategy = VirtualSamplerateReduceStrategy(11025)
pollute(
    samplerate_reduce_strategy, "../data/SALVE001/test", "../data/SALVE001/pollute/0003"
)
