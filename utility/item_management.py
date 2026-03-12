# For picking up items in a given room
def pick_up_items(
    item_key: str,
    room,
    game_state: dict[str, str | int | list[str]],
    items: dict[str, dict[str, str | bool | list[str] | dict[str, int]]],
) -> None:
    # Checks if item is in room
    if "current_room_items" not in room or item_key not in room["current_room_items"]:
        game_state["output_history"].append(
            "You grasp at the empty air, like an idiot."
        )
        return

    # Adds item to inventory list
    game_state["inventory"].append(item_key)
    # Removes item from room
    room["current_room_items"].remove(item_key)

    display_name = items[item_key]["display_name"]
    game_state["output_history"].append(f"you picked up {display_name}.")


# Function that runs when player wants to take a specific item from a container
def take_from_container(
    item_key: str,
    container_key,
    game_state: dict[str, str | int | list[str]],
    items: dict[str, dict[str, str | bool | list[str] | dict[str, int]]],
) -> None:
    # Checks for the container in inventory
    if container_key not in game_state["inventory"]:
        game_state["output_history"].append(
            "You reach your hand into the void of your pockets, you return nothing. Did you mean to reach for something else?"
        )
        return

    container = items[container_key]

    if not container.get("container"):
        game_state["output_history"].append(
            "This does obviously not have anything in it."
        )
        return

    contents = container.get("contents", [])

    if item_key not in contents:
        game_state["output_history"].append("You dont find what you were looking for.")
        return

    contents.remove(item_key)
    game_state["inventory"].append(item_key)

    display_name = items[item_key]["display_name"]
    game_state["output_history"].append(
        f"You take {display_name} from the {container['display_name']}"
    )


# Function that runs when player wants to put a spesific item into a container item
def put_in_container(
    item_key: str,
    container_key,
    game_state: dict[str, str | int | list[str]],
    items: dict[str, dict[str, str | bool | list[str] | dict[str, int]]],
) -> None:
    # Checks for the container in inventory
    if item_key not in game_state["inventory"]:
        game_state["output_history"].append("You grab air.")
        return

    container = items[container_key]

    if container_key not in game_state["inventory"]:
        game_state["output_history"].append("You dont find what you were looking for.")
        return

    contents = container.get("contents", [])

    if not container.get("container"):
        game_state["output_history"].append("You cant fit anything in this.")
        return

    game_state["inventory"].remove(item_key)
    contents.append(item_key)

    display_name = items[item_key]["display_name"]
    game_state["output_history"].append(
        f"You put {display_name} into {container['display_name']}"
    )


# Empty list for empty container function
earlier_contents = []


# Function for emptying all contents of a container into player inventory
def empty_container(
    item_key: str,
    container_key,
    game_state: dict[str, str | int | list[str]],
    items: dict[str, dict[str, str | bool | list[str] | dict[str, int]]],
) -> None:
    # Checks for the container in inventory
    if container_key not in game_state["inventory"]:
        game_state["output_history"].append(
            "You reach your hand into nothingness with the intention of pulling something out. It doesn't work..."
        )
        return

    container = items[container_key]

    if not container.get("container"):
        game_state["output_history"].append(
            "This does obviously not have anything in it."
        )
        return

    contents = container.get("contents", [])

    if item_key not in contents:
        game_state["output_history"].append("It's empty")
        return

    contents.remove(item_key)
    game_state["inventory"].append(item_key)
    item_name = items[item_key]["display_name"]
    earlier_contents.append(item_name)

    game_state["output_history"].append(
        "You take "
        + ", ".join(earlier_contents)
        + " from the "
        + container["display_name"]
    )


# Function for listing items that are in a container
def look_inside_container(
    container_key,
    game_state: dict[str, str | int | list[str]],
    items: dict[str, dict[str, str | bool | list[str] | dict[str, int]]],
) -> None:
    if container_key not in game_state["inventory"]:
        game_state["output_history"].append(
            "You stretch your hand into the void of your pockets, you return nothing. Did you mean to reach for something else?"
        )
        return

    container = items[container_key]

    if not container.get("container"):
        game_state["output_history"].append(
            "This obviously doens't have anything in it."
        )
        return

    contents = container.get("contents", [])

    names = [items[k]["display_name"] for k in contents]
    game_state["output_history"].append(
        " you look inside and see... " + ", ".join(names)
    )


# Function for checking inventory
def check_inventory(game_state: dict[str, str | int | list[str]], items) -> None:
    if not game_state["inventory"]:
        game_state["output_history"].append("your pockets are empty.")
        return

    game_state["output_history"].append(
        "you have... "
        + ", ".join(items[item]["display_name"] for item in game_state["inventory"])
    )


# Function for displaying item description
def examine_item(
    item_key,
    game_state: dict[str, str | int | list[str]],
    items: dict[str, dict[str, str | bool | list[str] | dict[str, int]]],
) -> None:
    if item_key not in game_state["inventory"]:
        game_state["output_history"].append(
            "You stretch your hand into the void of your pockets, you return nothing. Did you mean to reach for something else?"
        )
        return
    game_state["output_history"].append(items[item_key]["item_description"])


def pick_up_instant(
    game_state: dict[str, str | int | list[str]],
    rooms: dict[str, dict[str, str | list[str] | dict[str, str]]],
    items: dict[str, dict[str, str | bool | list[str] | dict[str, int]]]
) -> None:
    room_name = game_state["current_room"]
    room = rooms[room_name]
    instant_room_contents = room.get("instant_room_items", [])
    earlier_room_contents = []

    if not "instant_room_items":
        return
    else:
        for item_key in instant_room_contents[:]:
            instant_room_contents.remove(item_key)
            game_state["inventory"].append(item_key)
            item_name = items[item_key]["display_name"]
            earlier_room_contents.append(item_name)

    if earlier_room_contents:
        game_state["output_history"].append(
            "You get " + ", ".join(earlier_room_contents)
        )
