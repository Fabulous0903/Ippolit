# The purpose of this code is to simulate passing of time in the game.
import utility.resource_management as resource


# Function that passes time by appending 1 element to time list, and the length of that list is in military time."
def pass_time(game_state: dict[str, str | list[str]]) -> None:
    clock = len(game_state["time"])

    for hours in range(1):
        if clock == 24:
            game_state["time"].clear()
            game_state["time"].append("hour")
        elif clock < 24:
            game_state["time"].append("hour")
        elif clock > 24:
            game_state["time"].clear()
            game_state["time"].append("hour")


# Function that passes time by appending 1 element to time list, and the length of that list is in military time."
def pass_time_room(
    game_state: dict[str, str | list[str]],
    room_name: str,
    rooms: dict[str, dict[str, str | list[str] | dict[str, str]]],
) -> None:
    game_state["current_room"] = room_name
    room = rooms[room_name]
    # Defines time tag of room
    time_tag = room["time_tag"]
    clock = len(game_state["time"])

    if time_tag == "none":
        return

    elif time_tag == "quick":
        for hours in range(1):
            pass_time(game_state)
            game_state["hunger"] = max(0, game_state["hunger"] - 20)
            resource.check_hunger(game_state)

    elif time_tag == "medium":
        for hours in range(2):
            pass_time(game_state)
            game_state["hunger"] = max(0, game_state["hunger"] - 20)
            resource.check_hunger(game_state)

    elif time_tag == "long":
        for hours in range(3):
            pass_time(game_state)
            game_state["hunger"] = max(0, game_state["hunger"] - 20)
            resource.check_hunger(game_state)

    return
