import random
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput


def scroll_vertical_percentage(driver, start_percent=0.8, end_percent=0.3, x_percent=0.5, duration_range=(300, 800)):
    size = driver.get_window_size()
    width = size['width']
    height = size['height']

    start_x = int(width * x_percent)
    start_y = int(height * start_percent)
    end_y = int(height * end_percent)

    duration = random.randint(*duration_range)
    finger = PointerInput("touch", "finger")
    actions = ActionBuilder(driver, mouse=finger)

    actions.pointer_action.move_to_location(start_x, start_y)
    actions.pointer_action.pointer_down()
    actions.pointer_action.pause(duration / 1000)
    actions.pointer_action.move_to_location(start_x, end_y)
    actions.pointer_action.pointer_up()
    print("Scoll scroll_vertical_percentage")
    actions.perform()


def scroll_vertical(driver, start_x, start_y, end_y, duration_range=(300, 800)):
    duration = random.randint(*duration_range)
    finger = PointerInput("touch", "finger")
    actions = ActionBuilder(driver, mouse=finger)

    actions.pointer_action.move_to_location(start_x, start_y)
    actions.pointer_action.pointer_down()
    actions.pointer_action.pause(duration / 1000)
    actions.pointer_action.move_to_location(start_x, end_y)
    actions.pointer_action.pointer_up()

    actions.perform()


def scroll_horizontal(driver, start_x, start_y, end_x, duration_range=(300, 800)):
    duration = random.randint(*duration_range)
    finger = PointerInput("touch", "finger")
    actions = ActionBuilder(driver, mouse=finger)

    actions.pointer_action.move_to_location(start_x, start_y)
    actions.pointer_action.pointer_down()
    actions.pointer_action.pause(duration / 1000)
    actions.pointer_action.move_to_location(end_x, start_y)
    actions.pointer_action.pointer_up()

    actions.perform()


def scroll_to_coordinate_vertical(driver, start_x, start_y, end_x, end_y, duration_range=(300, 800)):
    duration = random.randint(*duration_range)
    finger = PointerInput("touch", "finger")
    actions = ActionBuilder(driver, mouse=finger)

    actions.pointer_action.move_to_location(start_x, start_y)
    actions.pointer_action.pointer_down()
    actions.pointer_action.pause(duration / 1000)
    actions.pointer_action.move_to_location(end_x, end_y)
    actions.pointer_action.pointer_up()

    actions.perform()


def scroll_to_coordinate_horizontal(driver, start_x, start_y, end_x, end_y, duration_range=(300, 800)):
    duration = random.randint(*duration_range)
    finger = PointerInput("touch", "finger")
    actions = ActionBuilder(driver, mouse=finger)

    actions.pointer_action.move_to_location(start_x, start_y)
    actions.pointer_action.pointer_down()
    actions.pointer_action.pause(duration / 1000)
    actions.pointer_action.move_to_location(end_x, end_y)
    actions.pointer_action.pointer_up()

    actions.perform()
