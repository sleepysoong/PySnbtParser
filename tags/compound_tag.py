from typing import Dict, Optional
from tags.tag import Tag

class CompoundTag(Tag):
    def __init__(self, value: Dict[str, Tag]):
        super().__init__(value)

    def __repr__(self):
        return f"CompoundTag({self.value})"

    def get(self, key: str, default: Optional[Tag] = None) -> Optional[Tag]:
        return self.value.get(key, default)

    def get_all(self) -> Dict[str, Tag]:
        return self.value