from parser import Parser
from tags.list_tag import ListTag
from tags.compound_tag import CompoundTag
from item import Item

def deserialize_snbt(snbt_string: str) -> Item:
    parser = Parser(snbt_string)
    nbt_tag = parser.parse()
    if not isinstance(nbt_tag, CompoundTag):
        raise ValueError("snbt는 CompoundTag여야 해요.")
    return Item.from_nbt(nbt_tag)


def deserialize_snbt_list(snbt_list_string: str) -> list:
    parser = Parser(snbt_list_string)
    nbt_tag = parser.parse()
    if not isinstance(nbt_tag, ListTag):
        raise ValueError("snbt는 ListTag여야 해요.")
    items = []
    for item_tag in nbt_tag.get_all():
        if not isinstance(item_tag, CompoundTag):
            raise ValueError("리스트의 요소는 CompoundTag여야 해요.")
        item = Item.from_nbt(item_tag)
        items.append(item)
    return items