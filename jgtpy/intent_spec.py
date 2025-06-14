import yaml


class StrategySpec:
    """Simple container for strategy intent loaded from YAML."""

    def __init__(self, data):
        self.data = data or {}

    @property
    def instruments(self):
        return self.data.get("instruments", [])

    @property
    def timeframes(self):
        return self.data.get("timeframes", [])


def load_strategy(path):
    """Load YAML strategy intent from a file."""
    with open(path, "r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return StrategySpec(data)
