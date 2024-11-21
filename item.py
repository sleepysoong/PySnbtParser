from tags.compound_tag import CompoundTag
from tags.list_tag import ListTag
from tags.string_tag import StringTag
from tags.byte_tag import ByteTag
from tags.short_tag import ShortTag


class Item:
    def __init__(self, id: str, count: int, damage: int = 0, tag: CompoundTag = None):
        self.id = id
        self.count = count
        self.damage = damage
        self.tag = tag
        self.name = self.id
        self.lore = []

        if self.tag:
            display_tag = self.tag.get("display")
            if isinstance(display_tag, CompoundTag):
                name_tag = display_tag.get("Name")
                if isinstance(name_tag, StringTag):
                    self.name = name_tag.value
                lore_tag = display_tag.get("Lore")
                if isinstance(lore_tag, ListTag):
                    self.lore = [tag.value for tag in lore_tag.get_all() if isinstance(tag, StringTag)]

    @classmethod
    def from_nbt(cls, nbt_tag: CompoundTag):
        id_tag = nbt_tag.get('Name')
        count_tag = nbt_tag.get('Count')
        damage_tag = nbt_tag.get('Damage', ShortTag(0))
        tag = nbt_tag.get('tag', CompoundTag({}))

        if not isinstance(id_tag, StringTag):
            raise ValueError("Name 태그는 StringTag여야 해요.")
        if not isinstance(count_tag, ByteTag):
            raise ValueError("Count 태그는 ByteTag여야 해요.")
        if not isinstance(damage_tag, ShortTag):
            raise ValueError("Damage 태그는 ShortTag여야 해요.")
        if not isinstance(tag, CompoundTag):
            raise ValueError("tag 태그는 CompoundTag여야 해요.")

        return cls(
            id=id_tag.value,
            count=count_tag.value,
            damage=damage_tag.value,
            tag=tag
        )

    def __repr__(self):
        return f"Item(id='{self.id}', name='{self.name}', count={self.count}, damage={self.damage}, lore={self.lore}, tag={self.tag})"