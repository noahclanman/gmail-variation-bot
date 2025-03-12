import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# File to store registered user IDs
USER_FILE = "user.txt"

# Function to load registered users from the file
def load_registered_users():
    try:
        with open(USER_FILE, "r") as file:
            return {int(line.strip()) for line in file if line.strip().isdigit()}
    except FileNotFoundError:
        return set()

# Function to save a new user ID to the file
def save_user(user_id):
    with open(USER_FILE, "a") as file:
        file.write(f"{user_id}\n")

# Load registered users on startup
registered_users = load_registered_users()

def generate_dot_variations(username: str, include_original: bool = False) -> list:
    variations = []
    n = len(username)
    total_combinations = 2 ** (n - 1)

    for i in range(total_combinations):
        variation = ""
        for j in range(n):
            variation += username[j]
            if j < n - 1 and (i >> j) & 1:
                variation += "."
        if not include_original and variation == username:
            continue
        variations.append(variation)

    return variations

def generate_plus_variations(username: str, suffixes: list) -> list:
    return [f"{username}+{suffix}@gmail.com" for suffix in suffixes]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Command handler for /start. Sends a welcome message when the user starts the bot. """
    welcome_message = (
        "Welcome to the Gmail Variation Bot!\n\n"
        "You must register to use the following commands:\n"
        "/gendot [yes] - Generate Gmail dot variations.\n"
        "/genplus ... - Generate Gmail '+' variations.\n"
        "/register - Register your account."
    )
    await update.message.reply_text(welcome_message)

async def gendot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.from_user.id not in registered_users:
        await update.message.reply_text("You must register first using the /register command.")
        return

    args = context.args
    if not args:
        await update.message.reply_text("Usage: /gendot [include_original: yes/no]")
        return

    username = args[0]
    include_original = False
    if len(args) > 1 and args[1].lower() in ["yes", "y"]:
        include_original = True

    variations = generate_dot_variations(username, include_original)
    if not variations:
        await update.message.reply_text("No variations generated.")
        return

    response_lines = [f"{var}@gmail.com" for var in variations]
    response = "\n".join(response_lines)

    if len(response) > 4000:
        response = response[:4000] + "\n... (truncated)"

    await update.message.reply_text(response)

async def genplus(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.from_user.id not in registered_users:
        await update.message.reply_text("You must register first using the /register command.")
        return

    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Usage: /genplus ...")
        return

    username = args[0]
    suffixes = args[1:]

    variations = generate_plus_variations(username, suffixes)
    if not variations:
        await update.message.reply_text("No variations generated.")
        return

    response = "\n".join(variations)

    if len(response) > 4000:
        response = response[:4000] + "\n... (truncated)"

    await update.message.reply_text(response)

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Command handler for /register. Registers the user. """
    user_id = update.message.from_user.id
    if user_id in registered_users:
        await update.message.reply_text("You are already registered!")
    else:
        registered_users.add(user_id)
        save_user(user_id)  # Save the new user ID to the file
        await update.message.reply_text("You have been registered successfully! Now you can use /gendot and /genplus to generate variations.")

def main():
    # Replace with your actual bot token.
    application = Application.builder().token("Your_Token_Here").build()

    # Register the command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("gendot", gendot))
    application.add_handler(CommandHandler("genplus", genplus))
    application.add_handler(CommandHandler("register", register))  # Add the register command handler

    # Run the bot using long polling
    application.run_polling()

if __name__ == '__main__':
    main()
