import utility.clock as clock
import utility.resource_management as resource
import utility.movement as movement


# When user sleeps, time 8 hours passes.
def sleep(
    game_state: dict[str, str | list[str]],
    rooms: dict[str, dict[str, str | list[str] | dict[str, str]]],
) -> None:
    room_name = game_state["current_room"]
    room = rooms[room_name]

    for hours in range(8):
        clock.pass_time(game_state)
        game_state["hunger"] = max(0, game_state["hunger"] - 2)
        resource.check_hunger(game_state)

    game_state["output_history"].append("You slept for a while")
    movement.enter_room_text(room_name, game_state, rooms)


# Same as sleep, but 2 hours.
def loiter(
    game_state: dict[str, str | list[str]],
    rooms: dict[str, dict[str, str | list[str] | dict[str, str]]],
) -> None:
    room_name = game_state["current_room"]
    room = rooms[room_name]

    for hours in range(2):
        clock.pass_time(game_state)
        game_state["hunger"] = max(0, game_state["hunger"] - 3)
        resource.check_hunger(game_state)

    game_state["output_history"].append("You loitered for some time")
    movement.enter_room_text(room_name, game_state, rooms)
