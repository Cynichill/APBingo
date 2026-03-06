from typing import NamedTuple, Optional
from BaseClasses import Location


class BingoLocation(Location):
    game = "APBingo"


class BingoLocationData(NamedTuple):
    region: str
    address: Optional[int] = None


# Initialize parameters for the board generation
min_size = 3
max_size = 26
location_data_table = {}
address = 1

# Generate entries for board sizes from 3x3 to 10x10
for size in range(min_size, max_size + 1):
    cols = [chr(ord('A') + i) for i in range(size)]  # A to appropriate letter for row size
    rows = list(range(1, size + 1))  # 1 to appropriate number for column size

    # Generate row entries (e.g., "Bingo (A1-A3)-0" and "Bingo (A1-A3)-1" for 3x3)
    for col in cols:
        location_data_table.update({
            f"Bingo ({col}1-{col}{size})-{i}": BingoLocationData(region="Bingo Board", address=address + i)
            for i in range(5)
        })
        address += 5

    # Generate column entries (e.g., "Bingo (A1-C1)-0" and "Bingo (A1-C1)-1" for 3x3)
    for row in rows:
        location_data_table.update({
            f"Bingo (A{row}-{cols[-1]}{row})-{i}": BingoLocationData(region="Bingo Board", address=address + i)
            for i in range(5)
        })
        address += 5

    # Generate main diagonal entries (e.g., "Bingo (A1-C3)-0" and "Bingo (A1-C3)-1" for 3x3)
    location_data_table.update({
        f"Bingo (A1-{cols[-1]}{rows[-1]})-{i}": BingoLocationData(region="Bingo Board", address=address + i)
        for i in range(5)
    })
    address += 5

    # Generate anti-diagonal entries (e.g., "Bingo (A3-C1)-0" and "Bingo (A3-C1)-1" for 3x3)
    location_data_table.update({
        f"Bingo (A{rows[-1]}-{cols[-1]}1)-{i}": BingoLocationData(region="Bingo Board", address=address + i)
        for i in range(5)
    })
    address += 5

# Add a single "Bingo (ALL)" entry for the entire data set
location_data_table["Bingo (ALL)"] = BingoLocationData(region="Bingo Board", address=address)
address += 1

# Create the final dictionary with address-only values
location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}