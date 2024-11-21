from tags.tag import Tag

class FloatTag(Tag):
    def __repr__(self):
        return f"FloatTag({self.value})"


class DoubleTag(Tag):
    def __repr__(self):
        return f"DoubleTag({self.value})"