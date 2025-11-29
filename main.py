import logging
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, request
import threading
import os

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токен бота
BOT_TOKEN = os.getenv('BOT_TOKEN', '8355837238:AAHGuJ016fgGwrKfqKIvV9w7VXOCgZdh_aY')

print("🚀 Запуск бота на Koyeb...")

groups_data = {
    "команда": [
        {"username": "welIweIIweIl"},
        {"username": "Viper_DQ"},
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
    ],
    "психолог": [
        {"username": "Rygen_ml"},
    ],
    "смм": [
        {"username": "KystVDele"},
    ],
    "хуёжник": [
        {"username": "TaiBurs"},
    ]
}

class GroupMentionBot:
    def __init__(self, token: str):
        self.token = token
        self.application = Application.builder().token(token).build()
        self.setup_handlers()
        self.application.post_init = self.setup_commands

    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("groups", self.groups_command))
        
        self.application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, 
            self.handle_message
        ))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        welcome_text = f"""👋 Привет, {user.first_name}!

Доступные группы:
@команда - команда
@тренер - тренера
@начальник - начальники
@аналитик - аналитик
@менеджер - менеджер
@психолог - психолог
@смм - смм специалист
@хуёжник - дизайнер"""
        await update.message.reply_text(welcome_text)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = """Просто напишите:
@команда, @тренер, @начальник, @аналитик, @менеджер, @психолог, @смм, @хуёжник"""
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
            
        message_text = update.message.text.lower()
        print(f"📨 Получено сообщение: {message_text}")
        
        for group_name in groups_data.keys():
            trigger_word = f"@{group_name}"
            if trigger_word in message_text:
                print(f"🔔 Найден триггер: {trigger_word}")
                mention_text = self.create_group_mention(group_name)
                await update.message.reply_text(mention_text)
                break

    async def setup_commands(self, application: Application):
        commands = [
            BotCommand("start", "Запустить бота"),
            BotCommand("help", "Помощь"),
            BotCommand("groups", "Показать состав групп")
        ]
        await application.bot.set_my_commands(commands)

    def run_polling(self):
        """Запуск бота с polling"""
        print("🤖 Бот запущен и готов к работе!")
        self.application.run_polling()

def start_health_check():
    """Запуск простого HTTP сервера для health checks"""
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def health_check():
        return "🤖 Bot is running!"
    
    @app.route('/health')
    def health():
        return {"status": "ok", "bot": "running"}
    
    port = int(os.environ.get('PORT', 8000))
    print(f"🏥 Health check server started on port {port}")
    app.run(host='0.0.0.0', port=port)

def main():
    # Запускаем health check в отдельном потоке
    health_thread = threading.Thread(target=start_health_check, daemon=True)
    health_thread.start()
    
    # Запускаем бота
    bot = GroupMentionBot(BOT_TOKEN)
    bot.run_polling()

if __name__ == "__main__":
    main()
