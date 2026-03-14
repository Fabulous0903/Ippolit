import utility.pass_time as pass_time


# Function that decreases hunger and adds hunger_effects
def check_hunger(game_state: dict[str, str | int | list[str]]) -> None:
    if 60 < game_state["hunger"] <= 80:
        game_state["hunger_effects"].clear()
        game_state["hunger_effects"].append("peckish")

    elif 40 < game_state["hunger"] <= 60:
        game_state["hunger_effects"].clear()
        game_state["hunger_effects"].append("hungry")

    elif 20 < game_state["hunger"] <= 40:
        game_state["hunger_effects"].clear()
        game_state["hunger_effects"].append("starving")

    elif 0 <= game_state["hunger"] <= 20:
        game_state["hunger_effects"].clear()
        game_state["hunger_effects"].append("famished")
        if game_state["hunger"] == 0:
            if game_state["physical_condition"] == 0:
                game_state["output_history"].append("Du er DØD")
            else:
                game_state["physical_condition"] -= 2


# A function for eating, uses a temprorary dictionary to search for item_key using display name
def eating(
    game_state: dict[str, str | int | list[str]],
    items: dict[str, dict[str, str | bool | list[str] | dict[str, int]]],
    display_name,
) -> None:
    display_name_to_item_key = {
        items[item_key].get("display_name", item_key): item_key for item_key in items
    }

    inventory = game_state["inventory"]
    hunger = game_state["hunger"]
    item_key = display_name_to_item_key.get(display_name, None)

    if item_key is None:
        invalid_food_item = "You cant eat that."
        game_state["output_history"].append(invalid_food_item)
        return

    item = items[item_key]
    item_saturation = item.get("saturation", None)

    if item_saturation is None:
        food_provides_no_saturation = "This isn't edible"
        game_state["output_history"].append(food_provides_no_saturation)

    elif item_key not in inventory:
        no_food = f"You dream of {display_name}. If only you had some left your day would be a whole lot better."
        game_state["output_history"].append(no_food)
        return

    else:
        inventory.remove(item_key)
        new_hunger = hunger + item_saturation
        game_state["hunger"] = min(100, hunger + item_saturation)

    return
