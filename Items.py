from typing import NamedTuple, Optional
from BaseClasses import Item, ItemClassification


class BingoItem(Item):
    game = "APBingo"


class BingoItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler

coords = [
    (chr(ord('A') + c), r)
    for c in range(26)
    for r in range(1, 27)
]

item_data_table = {
    f"{col}{row}": BingoItemData(code=code, type=ItemClassification.progression)
    for code, (col, row) in enumerate(coords, start=1)
}

free_hint_item_data_table = {
    f"Free Location Hint #{i}": BingoItemData(code=len(coords) + i, type=ItemClassification.useful)
    for i in range(1, len(coords) + 1)
}

item_data_table.update(free_hint_item_data_table)

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
