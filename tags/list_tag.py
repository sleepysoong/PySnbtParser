from typing import List, Optional
from tags.tag import Tag

class ListTag(Tag):
    def __init__(self, value: List[Tag]):
        super().__init__(value)

    def __repr__(self):
        return f"ListTag({self.value})"

    def get(self, index: int) -> Optional[Tag]:
        if 0 <= index < len(self.value):
            return self.value[index]
        return None

    def get_all(self) -> List[Tag]:
        return self.value