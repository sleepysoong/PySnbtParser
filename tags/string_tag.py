from tags.tag import Tag

class StringTag(Tag):
    def __repr__(self):
        return f"StringTag('{self.value}')"