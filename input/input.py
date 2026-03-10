import pygame as pg
import sys

import utility.item_management as item_managment
import utility.movement as movement
import utility.pass_time as pass_time


# Interprets user input
def handle_command(
    command,
    game_state: dict[str, str | int | list[str]],
    rooms: dict[str, dict[str, str | list[str] | dict[str, str]]],
    items: dict[str, dict[str, str | bool | list[str] | dict[str, int]]],
) -> None:
    # Divides words that have spaces between, and interprits capital letters as lowercase
    words = command.lower().split()
    room = rooms[game_state["current_room"]]

    # Logic for taking from and putting things in containers needs to use if logic and therefore comes before match words
    if len(words) >= 4 and words[0] == "take":
        before = []
        after = []
        is_after = False
        for word in words[1:]:
            if word == "from":
                is_after = True
            elif is_after:
                after.append(word)
            else:
                before.append(word)
        if not after or not before:
            game_state["output_history"].append("what?")
        else:
            container_key = "_".join(after)
            item_key = "_".join(before)
            item_management.take_from_container(
                item_key, container_key, game_state, items
            )
        return

    if len(words) >= 4 and words[0] == "put":
        before = []
        after = []
        is_after = False
        for word in words[1:]:
            if word == "into":
                is_after = True
            elif is_after:
                after.append(word)
            else:
                before.append(word)
        if not after or not before:
            game_state["output_history"].append("what?")
        else:
            container_key = "_".join(after)
            item_key = "_".join(before)
            item_managment.put_in_container(item_key, container_key, game_state, items)
        return

    match words:
        case ["look", "around"]:
            game_state["output_history"].append(room["on_look"])

        case ["pick", "up", *item_key_segments] | ["take", *item_key_segments]:
            if not item_key_segments:
                game_state["output_history"].append(
                    "You look around as if you are about to pick something up."
                    + " A mental haze clouds your mind, it is as if the thing you were about to pick up has fallen out of this world"
                )
                return
            item_key = "_".join(item_key_segments)
            item_managment.pick_up_items(item_key, room, game_state, items)

        case ["look"]:
            game_state["output_history"].append("Look at what?")

        case ["look", "inside", *container_key_segments]:
            container_key = "_".join(container_key_segments)
            item_managment.look_inside_container(container_key, game_state, items)

        case ["check", "inventory"]:
            item_managment.check_inventory(game_state)
        case ["inventory"]:
            item_managment.check_inventory(game_state)
        case ["check", "pockets"]:
            item_managment.check_inventory(game_state)
        case ["pockets"]:
            item_managment.check_inventory(game_state)

        case ["empty", *container_key_segments]:
            container_key = "_".join(container_key_segments)
            container = items[container_key]
            contents = container.get("contents", [])
            for item_key in contents[:]:
                item_managment.empty_container(
                    item_key, container_key, game_state, items
                )

        case ["examine", *item_key_segments] | ["look", "at", *item_key_segments]:
            if not item_key_segments:
                game_state["output_history"].append("what are you looking for?")
            item_key = "_".join(item_key_segments)
            item_managment.examine_item(item_key, game_state, items)

        # For passing time
        case ["sleep"]:
            pass_time.sleep(game_state, rooms)
        case ["pass", "time"]:
            pass_time.loiter(game_state, rooms)
        case ["loiter"]:
            pass_time.loiter(game_state, rooms)
        case ["wait"]:
            pass_time.loiter(game_state, rooms)
        case ["rest"]:
            pass_time.loiter(game_state, rooms)

        # For movement
        case ["go", "north"]:
            movement.movement_north(game_state, rooms)
        case ["north"]:
            movement.movement_north(game_state, rooms)

        case ["go", "south"]:
            movement.movement_south(game_state, rooms)
        case ["south"]:
            movement.movement_south(game_state, rooms)

        case ["go", "west"]:
            movement.movement_west(game_state, rooms)
        case ["west"]:
            movement.movement_west(game_state, rooms)

        case ["go", "east"]:
            movement.movement_east(game_state, rooms)
        case ["east"]:
            movement.movement_east(game_state, rooms)

        case ["help"]:
            game_state["output_history"].append(
                "You need a moment to recuperate and to evaluate your options. There's four directions you can go, north, west, south, east,"
                + " though there wont always be a way forward in a given direction. Your senses are yours to use, that can change... your eyes can look around,"
                + " your ears can listen, and your nose can smell. You can check your pockets, and you kan look inside bags."
                + " Taking inventory of your basic human functions reasures you that you are ready for what is to come."
            )

        case ["quit"]:
            pg.quit()
            sys.exit()

        case _:
            game_state["output_history"].append(
                "You feel that there is something you want to do,"
                + " but the idea isn't strong enough to solidify in your mind"
            )
