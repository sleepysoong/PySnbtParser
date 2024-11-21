from tags.tag import Tag

class IntTag(Tag):
    def __repr__(self):
        return f"IntTag({self.value})"


class IntArrayTag(Tag):
    def __repr__(self):
        return f"IntArrayTag({self.value})"