from llm.intent_router import detect_intent
from bot.formatter import format_response


_dispatcher = None


def get_dispatcher():
    """Get or create the dispatcher instance (lazy initialization)"""
    global _dispatcher
    if _dispatcher is None:
        from bot.dispatcher import Dispatcher
        _dispatcher = Dispatcher()
    return _dispatcher


async def handle_start(update, context):
    """Handle /start command"""
    user = update.effective_user
    welcome = (
        f"Hello {user.first_name}!\n\n"
        "I'm SchemaSwift Bot -- your conversational database assistant.\n\n"
        "Here's what I can do:\n"
        "- Register: 'Register me as John'\n"
        "- Products: 'Show all products'\n"
        "- Insert: 'Add laptop to electronics'\n"
        "- Delete: 'Delete product 3'\n"
        "- Role: 'What is my role?'\n"
        "- Access: 'I want admin access'\n\n"
        "Just type naturally and I'll handle the rest!"
    )
    await update.message.reply_text(welcome)


async def handle_help(update, context):
    """Handle /help command"""
    help_text = (
        "SchemaSwift Help\n\n"
        "Available Commands:\n"
        "/start -- Welcome message\n"
        "/help -- This help text\n\n"
        "Natural Language Actions:\n"
        "- 'Register me as [name]' -- Register yourself\n"
        "- 'Show all products' -- View product list\n"
        "- 'Add [product] to [category]' -- Insert product (admin)\n"
        "- 'Delete product [id]' -- Remove product (admin)\n"
        "- 'What is my role?' -- Check your role\n"
        "- 'I want admin access' -- Request access upgrade\n"
    )
    await update.message.reply_text(help_text)


async def handle_message(update, context):
    """Handle incoming text messages"""
    user = update.effective_user
    telegram_id = user.id
    name = user.username or user.first_name
    message = update.message.text

    # Show typing indicator
    await update.message.chat.send_action("typing")

    # Detect intent via LLM
    intent = detect_intent(message, telegram_id, name)
    print(f"[Intent] {intent}")

    # Dispatch to MCP tool
    dispatcher = get_dispatcher()
    result = await dispatcher.dispatch(intent)
    print(f"[Result] {result}")

    # Format and send reply
    formatted = format_response(result)
    await update.message.reply_text(formatted)