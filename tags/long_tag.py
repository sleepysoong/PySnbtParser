from tags.tag import Tag

class LongTag(Tag):
    def __repr__(self):
        return f"LongTag({self.value})"


class LongArrayTag(Tag):
    def __repr__(self):
        return f"LongArrayTag({self.value})"