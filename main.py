import logging
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
import threading

app = Flask(__name__)


@app.route('/')
def home():
    return "Bot is running!"


def run_flask():
    app.run(host='0.0.0.0', port=8080)


# Запускаем Flask в отдельном потоке
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# Ваш обычный код бота...
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = "8355837238:AAHGuJ016fgGwrKfqKIvV9w7VXOCgZdh_aY"

groups_data = {
    "команда": [
        {"username": "welIweIIweIl"},
        {"username": "MyNameAbaddon"},
        {"username": "winterwort"},
        {"username": "zhukov_nes"},
        {"username": "SHAHmirozdanie"}
    ],
    "тренер": [
        {"username": "Dedusmlbb"},
        {"username": "Margul95"}
    ],
    "начальник": [
        {"username": "rickreygan"},
        {"username": "qqueasiness"}
    ],
    "аналитик": [
        {"username": "KeepOnDaaancing"},
    ],
    "менеджер": [
        {"username": "PredatoryIrbis"},
    ]
}


class GroupMentionBot:
    def __init__(self, token: str):
        self.application = Application.builder().token(token).build()
        self.setup_handlers()
        # Устанавливаем команды при запуске
        self.application.post_init = self.setup_commands

    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("groups", self.groups_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        welcome_text = f""" Бот запущен

Доступные группы:
@команда - команда
@тренер - тренера
@начальник - начальники
@аналитик - аналитик
@менеджер - менеджер"""
        await update.message.reply_text(welcome_text)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = """Просто напишите:
@команда, @тренер, @начальник, @аналитик, @менеджер"""
        await update.message.reply_text(help_text)

    async def groups_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        groups_text = "👥 Состав групп:\n\n"
        for group_name, members in groups_data.items():
            groups_text += f"{group_name.upper()}:\n"
            for i, member in enumerate(members, 1):
                groups_text += f"{i}. @{member['username']}\n"
            groups_text += "\n"
        await update.message.reply_text(groups_text)

    def create_group_mention(self, group_name: str) -> str:
        if group_name not in groups_data:
            return ""
        members = groups_data[group_name]
        mentions = [f"@{member['username']}" for member in members if member['username']]
        return " ".join(mentions)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.message.text:
            return
        message_text = update.message.text
        for group_name in groups_data.keys():
            if f"@{group_name}" in message_text.lower():
                mention_text = self.create_group_mention(group_name)
                await update.message.reply_text(mention_text)
                break

    async def setup_commands(self, application: Application):
        """Настройка меню команд бота - убираем упоминание бота"""
        commands = [
            BotCommand("start", "Запустить бота"),
            BotCommand("help", "Помощь"),
        ]
        await application.bot.set_my_commands(commands)

        try:
            await application.bot.delete_my_commands()
            await application.bot.set_my_commands(commands)
        except Exception as e:
            print(f"Ошибка при обновлении команд: {e}")

    def run(self):
        print("🚀 Бот запускается на Replit...")
        self.application.run_polling()


# Запуск бота
if __name__ == "__main__":
    bot = GroupMentionBot(BOT_TOKEN)
    bot.run()