import sys
import asyncio
from bot.main import create_bot
from bot.handlers import get_dispatcher

# Force unbuffered stdout for Windows
sys.stdout.reconfigure(line_buffering=True)


async def main():
    print("=" * 50)
    print("  SchemaSwift - MCP Database Bot")
    print("=" * 50)

    # Initialize dispatcher and connect MCP client
    print("\n[1/3] Creating dispatcher...")
    dispatcher = get_dispatcher()

    print("[2/3] Connecting to MCP server...")
    await dispatcher.mcp_client.connect()
    print("      MCP server connected successfully!")

    print("[3/3] Starting Telegram bot...")
    app = create_bot()

    # Initialize the application
    await app.initialize()
    await app.start()

    # Start polling in background
    await app.updater.start_polling()
    print("\n[OK] Bot is running! Send messages on Telegram.")
    print("     Press Ctrl+C to stop.\n")

    # Keep running until interrupted
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
    finally:
        print("\n[STOP] Shutting down...")
        await app.updater.stop()
        await app.stop()
        await app.shutdown()
        await dispatcher.mcp_client.close()
        print("       Goodbye!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped.")