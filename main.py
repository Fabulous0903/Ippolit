# /// script
# dependencies = [
#   "pygame~=2.6",
# ]
# requires-python = ">=3.13"
# ///

# Imports libraries
import pygame as pg
import sys
import tomllib
from pathlib import Path

# Imports functions and data other game files
import utility.item_management as item_management
import utility.movement as movement
import utility.clock as time
import input.input as input
import gui.text_and_textbox as text

# Loades toml files and parses them
data_path = Path(__file__).parent / "data" / "game_state.toml"
with data_path.open("rb") as file:
    toml_game_state = tomllib.load(file)

data_path = Path(__file__).parent / "data" / "rooms.toml"
with data_path.open("rb") as file:
    toml_rooms = tomllib.load(file)

data_path = Path(__file__).parent / "data" / "items.toml"
with data_path.open("rb") as file:
    toml_items = tomllib.load(file)

rooms = toml_rooms["rooms"]
items = toml_items["items"]
game_state = toml_game_state["game_state"]


### Pygame start
pg.init()
pg.key.set_repeat(400, 50)
pg.font.init()
clock = pg.time.Clock()

### DIV variabler
screen = pg.display.set_mode((1920, 1200))

user_text = ""

active_input = False
active_output = False

# Caller viktige funksjoner
movement.enter_room(game_state["current_room"], game_state, rooms, items)

### Game loop
is_running = True
while is_running:
    # If user writes QUIT then game closes
    for event in pg.event.get():
        # Checks if mouse is pressing in input box
        if event.type == pg.MOUSEBUTTONDOWN:
            if text.input_rect.collidepoint(event.pos):
                active_input = True
            else:
                active_input = False

        if not game_state["output_history"]:
            active_output = False
        else:
            active_output = True

        # Event that activates only when key is pressed, if backspace remove last symbol in string,
        # else print symbol pressed.
        if event.type == pg.KEYDOWN and active_input:
            if event.key == pg.K_BACKSPACE:
                user_text = user_text[:-1]
            if event.key == pg.K_RETURN:
                input.handle_command(user_text, game_state, rooms, items)
                user_text = ""
            elif event.key != pg.K_BACKSPACE:
                user_text += event.unicode

    screen.fill((20, 16, 18))
    #dt = clock.tick(60)
    #text.tick_output(dt)

    # Changes color if mousebutton pressed input box
    if active_input:
        text.color_input = text.color_active_input
    else:
        text.color_input = text.color_passive_input

    if active_output:
        text.color_output = text.color_active_output
    else:
        text.color_output = text.color_passive_output

    # Functions from text_and_textbox
    text.update_output(game_state, screen.get_width())
    input_lines = text.update_input(user_text)
    hunger_bar = text.update_hunger_bar(game_state)
    physical_condition_bar = text.update_physical_dondition_bar(game_state)
    inventory_box_lines = text.update_inventory_box(game_state, items)

    # Draws output box
    pg.draw.rect(screen, text.color_output, text.output_rect)
    y_offset_output = text.output_rect.y + text.PADDING

    for line in text.visible_lines:
        text_surface = text.base_font.render(line, True, (230, 216, 211))
        screen.blit(text_surface, (text.output_rect.x + text.PADDING, y_offset_output))
        y_offset_output += text.LINE_HEIGHT

    # Draws input box
    pg.draw.rect(screen, text.color_input, text.input_rect)
    y_offset_input = text.input_rect.y + text.PADDING

    for line in input_lines:
        text_surface = text.base_font.render(line, True, (230, 216, 211))
        screen.blit(text_surface, (text.input_rect.x + text.PADDING, y_offset_input))
        y_offset_input += text.LINE_HEIGHT

    # Draws physical condition bar
    pg.draw.rect(screen, text.color_input, text.physical_condition_rect)
    text_surface = text.base_font.render(physical_condition_bar, True, (196, 69, 54))
    screen.blit(
        text_surface,
        (
            text.physical_condition_rect.x + text.PADDING,
            text.physical_condition_rect.y + text.PADDING,
        ),
    )

    # Draws hunger box bar
    pg.draw.rect(screen, text.color_input, text.hunger_rect)
    text_surface = text.base_font.render(hunger_bar, True, (196, 69, 54))
    screen.blit(
        text_surface,
        (text.hunger_rect.x + text.PADDING, text.hunger_rect.y + text.PADDING),
    )

    # Draws inventory box
    pg.draw.rect(screen, text.color_input, text.inventory_rect)

    for line in inventory_box_lines:
        text_surface = text.base_font.render(inventory_box_lines, True, (196, 69, 54))
        screen.blit(
            text_surface,
            (text.inventory_rect.x + text.PADDING, text.inventory_rect.y + text.PADDING),
        )

    # Updates the display
    pg.display.flip()
    clock.tick(60)
pg.display.quit()
