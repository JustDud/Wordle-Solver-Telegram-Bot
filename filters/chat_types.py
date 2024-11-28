from aiogram.filters import Filter
from aiogram import types, Bot


# Custom filter to check the type of chat (e.g., private, group, supergroup, etc.)
class ChatTypesFilter(Filter):

    def __init__(self, chat_types: list[str]) -> None:
        """
        Initializes the filter with a list of allowed chat types.

        :param chat_types: List of allowed chat types (e.g., ['private', 'group']).
        """
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        """
        Checks whether the chat type of the incoming message matches the allowed chat types.

        :param message: The incoming message object.
        :return: True if the chat type is in the allowed list, False otherwise.
        """
        return message.chat.type in self.chat_types
