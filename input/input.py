import pygame as pg
import sys

import utility.item_management as item_management
import utility.movement as movement
import utility.pass_time as pass_time
import utility.resource_management as resource_management


# Interprets user input
def handle_command(
    command,
    game_state: dict[str, str | int | list[str]],
    rooms: dict[str, dict[str, str | list[str] | dict[str, str]]],
    items: dict[str, dict[str, str | bool | list[str] | dict[str, int]]],
) -> None:
    # Divides words that have spaces between, and interprits capital letters as lowercase
    words = command.lower().replace("  ", " ").replace("  ", " ").split()
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
            item_management.put_in_container(item_key, container_key, game_state, items)
        return

    match words:
        case ["look", "around"]:
            game_state["output_history"].append(room["on_look"])

        case ["pick", "up", *item_key_segments] | ["take", *item_key_segments]:
            if not item_key_segments:
                game_state["output_history"].append(
                    "You look around as if you are about to pick something up."
                    + " A haze clouds your mind, it is as if the thing you were about to pick up has fallen out of this world"
                )
                return
            item_key = "_".join(item_key_segments)
            item_management.pick_up_items(item_key, room, game_state, items)

        case ["look"]:
            game_state["output_history"].append("Look at what?")

        # item management
        case ["look", "inside", *container_key_segments]:
            container_key = "_".join(container_key_segments)
            item_management.look_inside_container(container_key, game_state, items)

        case ["check", "inventory"]:
            item_management.check_inventory(game_state, items)
        case ["inventory"]:
            item_management.check_inventory(game_state, items)
        case ["check", "pockets"]:
            item_management.check_inventory(game_state, items)
        case ["pockets"]:
            item_management.check_inventory(game_state, items)

        case ["empty", *container_key_segments]:
            container_key = "_".join(container_key_segments)
            item_management.empty_container(container_key, game_state, items)

        case ["examine", *item_key_segments] | ["look", "at", *item_key_segments]:
            if not item_key_segments:
                game_state["output_history"].append("what are you looking for?")
            display_name = " ".join(item_key_segments)
            item_management.examine_item(display_name, game_state, items)

        case ["eat", *display_name_segments]:
            if not display_name_segments:
                game_state["output_history"].append("what are you looking for?")
            display_name = " ".join(display_name_segments)
            resource_management.eating(game_state, items, display_name)

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
            movement.movement_north(game_state, rooms, items)
        case ["north"]:
            movement.movement_north(game_state, rooms, items)

        case ["go", "south"]:
            movement.movement_south(game_state, rooms, items)
        case ["south"]:
            movement.movement_south(game_state, rooms, items)

        case ["go", "west"]:
            movement.movement_west(game_state, rooms, items)
        case ["west"]:
            movement.movement_west(game_state, rooms, items)

        case ["go", "east"]:
            movement.movement_east(game_state, rooms, items)
        case ["east"]:
            movement.movement_east(game_state, rooms, items)

        case ["help"]:
            help_text = game_state["help"]
            game_state["output_history"].append(help_text)

        case ["quit"]:
            pg.quit()
            sys.exit()

        case _:
            game_state["output_history"].append(
                "You feel that there is something you want to do,"
                + " but the idea isn't strong enough to solidify in your mind"
            )
