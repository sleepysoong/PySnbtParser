from typing import Any

class Tag:
    def __init__(self, value: Any):
        self.value = value

    def __repr__(self):
        return f"Tag({self.value})"