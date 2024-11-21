from tags.tag import Tag

class ShortTag(Tag):
    def __repr__(self):
        return f"ShortTag({self.value})"