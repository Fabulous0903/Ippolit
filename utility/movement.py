import utility.clock as time


def check_time_for_room(
    room_name: str,
    game_state: dict[str, str | int | list[str]],
    rooms: dict[str, dict[str, str | list[str] | dict[str, str]]],
) -> None:
    game_state["current_room"] = room_name
    room = rooms[room_name]
    clock = len(game_state["time"])

    if 6 <= clock < 18:
        if room_name not in game_state["visited_rooms"]:
            game_state["visited_rooms"].append(room_name)
            game_state["output_history"].append(room["on_enter_first_day"])
        elif room_name in game_state["visited_rooms"]:
            game_state["output_history"].append(room["on_enter_day"])

    elif 18 <= clock < 20:
        if room_name not in game_state["visited_rooms"]:
            game_state["visited_rooms"].append(room_name)
            game_state["output_history"].append(room["on_enter_first_sunset"])
        elif room_name in game_state["visited_rooms_sunset"]:
            game_state["output_history"].append(room["on_enter_sunset"])

    elif 20 <= clock < 24 or 24 < clock < 4:
        if room_name not in game_state["visited_rooms"]:
            game_state["visited_rooms"].append(room_name)
            game_state["output_history"].append(room["on_enter_first_night"])
        elif room_name in game_state["visited_rooms"]:
            game_state["output_history"].append(room["on_enter_night"])

    elif 4 <= clock < 6:
        if room_name not in game_state["visited_rooms"]:
            game_state["visited_rooms"].append(room_name)
            game_state["output_history"].append(room["on_enter_first_sunrise"])
        elif room_name in game_state["visited_rooms_sunset"]:
            game_state["output_history"].append(room["on_enter_sunset"])

    return


# Function that updates room and gives text depending of the time when entering room.
def enter_room(
    room_name: str,
    game_state: dict[str, str | int | list[str]],
    rooms: dict[str, dict[str, str | list[str] | dict[str, str]]],
) -> None:
    game_state["current_room"] = room_name
    room = rooms[room_name]

    time.pass_time_room(game_state, room_name, rooms)
    check_time_for_room(room_name, game_state, rooms)

    return


# Function that shows text for room, used when sleeping and such.
def enter_room_text(
    room_name: str,
    game_state: dict[str, str | int | list[str]],
    rooms: dict[str, dict[str, str | list[str] | dict[str, str]]],
) -> None:
    game_state["current_room"] = room_name
    room = rooms[room_name]

    check_time_for_room(room_name, game_state, rooms)

    return


def movement_north(
    game_state: dict[str, str | list[str]],
    rooms: dict[str, dict[str, str | list[str] | dict[str, str]]],
) -> None:
    room_key = game_state["current_room"]
    room = rooms[room_key]
    text = room["exits"]["north"]

    text_before = text.split(": ")[0]
    text_after = text.split(": ")[1]

    if text_before == "open":
        game_state["current_room"] = text_after
        room_name = game_state["current_room"]
        enter_room(room_name, game_state, rooms)

    elif text_before == "closed":
        game_state["output_history"].append(text_after)
        return


def movement_south(
    game_state: dict[str, str | int | list[str]],
    rooms: dict[str, dict[str, str | list[str] | dict[str, str]]],
) -> None:
    room_key = game_state["current_room"]
    room = rooms[room_key]
    text = room["exits"]["south"]

    text_before = text.split(": ")[0]
    text_after = text.split(": ")[1]

    if text_before == "open":
        game_state["current_room"] = text_after
        room_name = game_state["current_room"]
        enter_room(room_name, game_state, rooms)

    elif text_before == "closed":
        game_state["output_history"].append(text_after)
        return


def movement_west(
    game_state: dict[str, str | int | list[str]],
    rooms: dict[str, dict[str, str | list[str] | dict[str, str]]],
) -> None:
    room_key = game_state["current_room"]
    room = rooms[room_key]
    text = room["exits"]["west"]

    text_before = text.split(": ")[0]
    text_after = text.split(": ")[1]

    if text_before == "open":
        game_state["current_room"] = text_after
        room_name = game_state["current_room"]
        enter_room(room_name, game_state, rooms)

    elif text_before == "closed":
        game_state["output_history"].append(text_after)
        return


def movement_east(
    game_state: dict[str, str | int | list[str]],
    rooms: dict[str, dict[str, str | list[str] | dict[str, str]]],
) -> None:
    room_key = game_state["current_room"]
    room = rooms[room_key]
    text = room["exits"]["east"]

    text_before = text.split(": ")[0]
    text_after = text.split(": ")[1]

    if text_before == "open":
        game_state["current_room"] = text_after
        room_name = game_state["current_room"]
        enter_room(room_name, game_state)

    elif text_before == "closed":
        game_state["output_history"].append(text_after)
        return
