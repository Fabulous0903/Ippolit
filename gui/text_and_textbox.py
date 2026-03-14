from pathlib import Path
from collections import Counter
import pygame as pg

### Text/GUI
pg.font.init()
font_path = Path(__file__).parent.parent / "data" / "ShareTechMono-Regular.ttf"
base_font = pg.font.Font(font_path, 20)

# color_active stores color which gets activated when input box is clicked by user
# color_passive stores the color of the input box
color_active_input = pg.Color(36, 28, 30)
color_passive_input = pg.Color(31, 23, 25)
color_active_output = pg.Color(36, 28, 30)
color_passive_output = pg.Color(31, 23, 25)

color_input = color_passive_input
color_output = color_passive_output

user_text = ""

# For wrapping text
def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "

        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "

    lines.append(current_line)
    return lines

# Rectangle to be used for user input and output
input_rect = pg.Rect(10, 100, 140, 32)
output_rect = pg.Rect(10, 100, 140, 32)
hunger_rect = pg.Rect(10, 100, 140, 32)
physical_condition_rect = pg.Rect(10, 100, 140, 32)
inventory_rect = pg.Rect(10, 100, 140, 32)

PADDING = 10
LINE_HEIGHT = base_font.get_height()
MAX_VISIBLE_LINES = 40

# Output box
def update_output(game_state: dict[str, str | int | list[str]], screen_width) -> None:
    global visible_lines, output_height, max_text_width

    max_text_width = screen_width - 600
    output_lines = ["-" * 120]

    for paragraph in game_state["output_history"]:
        # SPLITT PÅ LINJESKIFT (avsnitt)
        parts = paragraph.split("\n")

        for part in parts:
            wrapped = wrap_text(part, base_font, max_text_width)
            output_lines.extend(wrapped)

        output_lines.append("-" * 120)

    visible_lines = output_lines[-MAX_VISIBLE_LINES:]
    output_height = PADDING * 2 + LINE_HEIGHT * len(visible_lines)

    output_rect.x = 20
    output_rect.y = 20
    output_rect.w = max_text_width + PADDING * 2
    output_rect.h = output_height

# Input box
def update_input(user_text):
    input_lines = wrap_text(user_text, base_font, max_text_width)
    input_height = PADDING * 2 + LINE_HEIGHT
    character_width, character_height = base_font.size("A")

    input_width_addition = character_width * len(user_text)

    input_rect.x = 20
    input_rect.y = output_rect.bottom + PADDING
    input_rect.w = max(100, input_width_addition + PADDING * 2)
    input_rect.h = input_height

    return input_lines

# Updates the positionn of the physical condition bar relative to the input bar
def update_physical_dondition_bar(game_state: dict[str, str | int | list[str]]):
    physical_condition = game_state["physical_condition"]
    physical_condition_bar = "Physical condition: " + str(physical_condition)

    physical_condition_rect.x = input_rect.right + PADDING
    physical_condition_rect.y = output_rect.bottom + PADDING
    physical_condition_rect.w = 270
    physical_condition_rect.h = PADDING * 2 + LINE_HEIGHT

    return physical_condition_bar

# Updates the positionn of the hunger bar relative to the physical condition bar relative
def update_hunger_bar(game_state: dict[str, str | int | list[str]]):
    hunger = game_state["hunger"]
    hunger_bar = "Hunger: " + str(hunger)

    hunger_rect.x = physical_condition_rect.right + PADDING
    hunger_rect.y = output_rect.bottom + PADDING
    hunger_rect.w = 140
    hunger_rect.h = PADDING * 2 + LINE_HEIGHT

    return hunger_bar

# inventory on the right part of the screen
def update_inventory_box(
    game_state: dict[str, str | int | list[str]],
    items: dict[str, dict[str, str | bool | list[str] | dict[str, int]]],
):
    inventory = game_state["inventory"]
    inventory_box_lines = []
    display_lines = []
    display_lines_list = []

    if not inventory:
        inventory_text = "Pockets: (empty)"
        inventory_box_lines.append(inventory_text)
    else:
        header = "Pockets:"
        inventory_box_lines.append(header)

        for item in inventory:
            display_lines.append(items[item]["display_name"])

        counts = list(Counter(display_lines).items())
        
        for item, count in counts:
            if count > 1:
                display_lines_list.append(f"- {item} x {count}")

            else:
                display_lines_list.append("- " + item)

        for line in display_lines_list:
            wrapped = wrap_text(line, base_font, 550 - PADDING * 2)
            inventory_box_lines.extend(wrapped)

    inventory_height = PADDING * 2 + LINE_HEIGHT * len(inventory_box_lines)

    inventory_rect.x = output_rect.right + PADDING
    inventory_rect.y = 20
    inventory_rect.w = 550 - PADDING * 2
    inventory_rect.h = inventory_height

    return inventory_box_lines
