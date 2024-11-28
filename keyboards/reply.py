from aiogram.types import KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_keyboard(
        *btns: str,
        placeholder: str = None,
        request_contact: int = None,
        request_location: int = None,
        sizes: tuple[int] = (2,),
):
    """
    Generates a dynamic reply keyboard with customizable buttons.

    :param btns: Variable number of button texts to include in the keyboard.
    :param placeholder: Placeholder text for the input field (optional).
    :param request_contact: Index of the button that requests the user's contact information (optional).
    :param request_location: Index of the button that requests the user's location (optional).
    :param sizes: Tuple specifying the row size(s) for the keyboard layout (default is 2 per row).
    :return: A configured reply keyboard markup.
    """
    keyboard = ReplyKeyboardBuilder()

    # Add buttons to the keyboard.
    for index, text in enumerate(btns, start=0):
        if request_contact and request_contact == index:
            # Add a button that requests the user's contact information.
            keyboard.add(KeyboardButton(text=text, request_contact=True))
        elif request_location and request_location == index:
            # Add a button that requests the user's location information.
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            # Add a regular button.
            keyboard.add(KeyboardButton(text=text))

    # Adjust the keyboard layout based on the provided sizes and return the markup.
    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True,  # Automatically resize the keyboard for better usability.
        input_field_placeholder=placeholder  # Set the placeholder for the input field.
    )
