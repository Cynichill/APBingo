from typing import NamedTuple, Optional
from BaseClasses import Item, ItemClassification


class BingoItem(Item):
    game = "APBingo"


class BingoItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler


item_data_table = {
    f"{chr(col)}{row}": BingoItemData(code=code, type=ItemClassification.progression)
    for code, (col, row) in enumerate(((ord('A') + c, r) for c in range(26) for r in range(1, 27)), start=1)
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
