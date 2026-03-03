import os
import datetime
import pytz
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Bot
from telegram.ext import Application
from telegram.ext import ContextTypes
from telegram.ext import JobQueue

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
SHEET_NAME = os.getenv("SHEET_NAME")

bot = Bot(token=TOKEN)

def get_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scope
    )
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).sheet1

async def check_birthdays(context: ContextTypes.DEFAULT_TYPE):
    sheet = get_sheet()
    data = sheet.get_all_records()

    today = datetime.datetime.now(pytz.timezone("Europe/Moscow"))
    today_day = today.day
    today_month = today.month

    for row in data:
        name = row["ФИО"]
        birthday = row["День Рождения"]

        if not birthday:
            continue

        birth_date = datetime.datetime.strptime(birthday, "%d.%m.%Y")

        if birth_date.day == today_day and birth_date.month == today_month:
            age = today.year - birth_date.year

            message = (
                f"🎉 С Днем Рождения, {name}! 🎂\n"
                f"Желаю счастья, здоровья, побольше положительных моментов в жизни! 🥳"
            )

            await context.bot.send_message(chat_id=CHAT_ID, text=message)

async def main():
    application = Application.builder().token(TOKEN).build()

    # Запуск каждый день в 09:00 по Москве
    job_queue: JobQueue = application.job_queue
    job_queue.run_daily(
        check_birthdays,
        time=datetime.time(hour=9, minute=0, tzinfo=pytz.timezone("Europe/Moscow"))
    )

    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
