from typing import Callable
from BaseClasses import CollectionState


def get_bingo_rule(location, world) -> Callable[[CollectionState], bool]:
    required_keys = extract_bingo_spaces(location)
    return lambda state: all(state.has(key, world.player) for key in required_keys)


def special_rule(world, all_keys) -> Callable[[CollectionState], bool]:
    return lambda state: all(state.has(key, world.player) for key in all_keys)


def can_goal(state, player, required_bingos, board_size) -> bool:

    # Generate all possible Bingo keys for the board
    possible_keys = [f"{chr(col)}{row}" for col in range(ord('A'), ord('A') + board_size) for row in range(1, board_size + 1)]

    possible_bingos = []

    # Generate rows
    possible_bingos += [
        [f"{chr(ord('A') + row)}{col}" for row in range(board_size)]
        for col in range(1, board_size + 1)
    ]

    # Generate columns
    possible_bingos += [
        [f"{chr(ord('A') + row)}{col}" for col in range(1, board_size + 1)]
        for row in range(board_size)
    ]

    # Generate the main diagonal (\) from top-left to bottom-right
    possible_bingos.append([
        f"{chr(ord('A') + i)}{i + 1}" for i in range(board_size)
    ])

    # Generate the anti-diagonal (/) from top-right to bottom-left
    possible_bingos.append([
        f"{chr(ord('A') + i)}{board_size - i}" for i in range(board_size)
    ])

    # Collect keys that the player has
    player_keys = []
    for key in possible_keys:  # possible_keys contains all keys (A1, A2, ..., E5)
        if state.has(key, player):
            player_keys.append(key)

    # Count how many Bingos the player has
    bingo_count = 0
    for bingo in possible_bingos:
        if all(key in player_keys for key in bingo):
            bingo_count += 1

    # Check if the number of completed Bingos meets or exceeds the required amount
    return bingo_count >= required_bingos


def extract_bingo_spaces(location):
    # Extract the content within the brackets
    start, end = location[location.index("(") + 1:location.index(")")].split("-")

    # Determine the range of rows and columns
    start_col = start[0]  # 'A', 'B', 'C', etc.
    start_row = int(start[1:])  # 1, 2, 3, etc.
    end_col = end[0]  # 'A', 'B', 'C', etc.
    end_row = int(end[1:])  # 1, 2, 3, etc.

    spaces = []

    # Generate spaces for horizontal or vertical Bingo
    if start_row == end_row:  # Horizontal Bingo
        col_range = range(ord(start_col), ord(end_col) + 1) if ord(start_col) < ord(end_col) else range(ord(start_col), ord(end_col) - 1, -1)
        for col in col_range:
            spaces.append(f"{chr(col)}{start_row}")
    elif start_col == end_col:  # Vertical Bingo
        row_range = range(start_row, end_row + 1) if start_row < end_row else range(start_row, end_row - 1, -1)
        for row in row_range:
            spaces.append(f"{start_col}{row}")
    else:  # Diagonal Bingo
        col_range = range(ord(start_col), ord(end_col) + 1) if ord(start_col) < ord(end_col) else range(ord(start_col), ord(end_col) - 1, -1)
        row_range = range(start_row, end_row + 1) if start_row < end_row else range(start_row, end_row - 1, -1)
        for col, row in zip(col_range, row_range):
            spaces.append(f"{chr(col)}{row}")

    return spaces
