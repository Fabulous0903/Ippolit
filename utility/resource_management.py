import utility.pass_time as pass_time


# Function that decreases hunger and adds hunger_effects
def check_hunger(game_state):
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


# Function that updates walking speed.
# def update_walking_speed(game_state):
