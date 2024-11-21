from tags.tag import Tag

class ByteTag(Tag):
    def __repr__(self):
        return f"ByteTag({self.value})"


class ByteArrayTag(Tag):
    def __repr__(self):
        return f"ByteArrayTag({self.value})"