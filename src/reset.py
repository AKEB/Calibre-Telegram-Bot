"""Reset Functions"""
from telegram.ext import (
    CallbackContext,
    ConversationHandler
)
from config import logger


def reset_last_command(context: CallbackContext) -> int:
    """reset_last_command"""
    logger.debug("reset_last_command() start")
    if 'search_results' in context.user_data:
        del context.user_data['search_results']
    if 'current_page' in context.user_data:
        del context.user_data['current_page']
    if 'search_message_id' in context.user_data:
        del context.user_data['search_message_id']
    if 'selected_book' in context.user_data:
        del context.user_data['selected_book']
    return ConversationHandler.END


def reset_search(context: CallbackContext) -> int:
    """reset_search"""
    logger.debug("reset_search() start")
    if 'search_type' in context.user_data:
        del context.user_data['search_type']
    if 'search_query' in context.user_data:
        del context.user_data['search_query']

    return reset_last_command(context)
