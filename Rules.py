from typing import Callable
from BaseClasses import CollectionState


def get_bingo_rule(location, world) -> Callable[[CollectionState], bool]:
    required_keys = extract_bingo_spaces(location)
    return lambda state: all(state.has(key, world.player) for key in required_keys)


def special_rules(world, all_keys, bingo) -> Callable[[CollectionState], bool]:
    match bingo:
        case "Blackout":
            return lambda state: all(state.has(key, world.player) for key in all_keys)
        case "Checkerboard":
            # Extract rows and columns from the keys
            rows = sorted(set(key[0] for key in all_keys))  # ['A','B','C', ...]
            cols = sorted(set(int(key[1:]) for key in all_keys))  # [1,2,3,...]

            # Compute checkerboard squares
            checkerboard_keys = [
                f"{r}{c}"
                for i, r in enumerate(rows)
                for j, c in enumerate(cols)
                if (i + j) % 2 == 0  # "every second square" pattern
            ]

            return lambda state: all(state.has(key, world.player) for key in checkerboard_keys)
        case "Reverse Checkerboard":
            # Extract rows and columns from the keys
            rows = sorted(set(key[0] for key in all_keys))
            cols = sorted(set(int(key[1:]) for key in all_keys))

            # Compute reverse checkerboard squares
            reverse_checkerboard_keys = [
                f"{r}{c}"
                for i, r in enumerate(rows)
                for j, c in enumerate(cols)
                if (i + j) % 2 == 1  # every other square, starting from second
            ]

            return lambda state: all(state.has(key, world.player) for key in reverse_checkerboard_keys)
        case "Pictureframe":  # All edges
            # Extract rows and columns from the keys
            rows = sorted(set(key[0] for key in all_keys))  # e.g., ['A','B','C',...]
            cols = sorted(set(int(key[1:]) for key in all_keys))  # e.g., [1,2,3,...]
            edge_keys = []

            for r in rows:
                for c in cols:
                    # A square is on the edge if it's in the first or last row, or first or last column
                    if r == rows[0] or r == rows[-1] or c == cols[0] or c == cols[-1]:
                        edge_keys.append(f"{r}{c}")
            return lambda state: all(state.has(key, world.player) for key in edge_keys)
        case "Corners":  # All corners
            # Extract rows and columns from the keys
            rows = sorted(set(key[0] for key in all_keys))  # e.g., ['A', 'B', 'C', ...]
            cols = sorted(set(int(key[1:]) for key in all_keys))  # e.g., [1, 2, 3, ...]

            # Corner keys: top-left, top-right, bottom-left, bottom-right
            corners = [
                f"{rows[0]}{cols[0]}",  # top-left
                f"{rows[0]}{cols[-1]}",  # top-right
                f"{rows[-1]}{cols[0]}",  # bottom-left
                f"{rows[-1]}{cols[-1]}"  # bottom-right
            ]
            return lambda state: all(state.has(key, world.player) for key in corners)
        case _:  # default case
            return lambda state: all(state.has(key, world.player) for key in all_keys)


def can_goal(state, player, required_bingos, board_size, additional_bingos) -> bool:

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
    player_keys = set()
    for key in possible_keys:  # possible_keys contains all keys (A1, A2, ..., E5)
        if state.has(key, player):
            player_keys.add(key)

    # Count how many Bingos the player has
    bingo_count = 0
    for bingo in possible_bingos:
        if all(key in player_keys for key in bingo):
            bingo_count += 1

    # Check blackout (player owns all squares)
    if "Blackout" in additional_bingos:
        if len(player_keys) == len(possible_keys):
            bingo_count += 1

    rows = sorted(set(key[0] for key in possible_keys))
    cols = sorted(set(int(key[1:]) for key in possible_keys))

    # Check Corners (player owns all corners)
    if "Corners" in additional_bingos:
        # Calc corners
        corner_keys = [
            f"{rows[0]}{cols[0]}",    # top-left
            f"{rows[0]}{cols[-1]}",   # top-right
            f"{rows[-1]}{cols[0]}",   # bottom-left
            f"{rows[-1]}{cols[-1]}"   # bottom-right
        ]
        if all(key in player_keys for key in corner_keys):
            bingo_count += 1

    # Check Pictureframe (player owns all edge squares)
    if "Pictureframe" in additional_bingos:
        # Calculate edges
        edge_keys = [
            f"{r}{c}"
            for r in rows
            for c in cols
            if r == rows[0] or r == rows[-1] or c == cols[0] or c == cols[-1]
        ]
        if all(key in player_keys for key in edge_keys):
            bingo_count += 1

    # Check Checkerboard (player owns all regular checkerboard squares)
    if "Checkerboard" in additional_bingos:
        checkerboard_keys = [
            f"{r}{c}"
            for i, r in enumerate(rows)
            for j, c in enumerate(cols)
            if (i + j) % 2 == 1  # regular checkerboard pattern
        ]
        if all(key in player_keys for key in checkerboard_keys):
            bingo_count += 1

    # Check Reverse Checkerboard (player owns all reverse checkerboard squares)
    if "Reverse Checkerboard" in additional_bingos:
        reverse_checkerboard_keys = [
            f"{r}{c}"
            for i, r in enumerate(rows)
            for j, c in enumerate(cols)
            if (i + j) % 2 == 0  # reverse checkerboard pattern
        ]
        if all(key in player_keys for key in reverse_checkerboard_keys):
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
