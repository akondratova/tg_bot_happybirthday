import os
import datetime
import pytz
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram.ext import Application, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
SHEET_NAME = os.getenv("SHEET_NAME")


def get_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json",
        scope
    )

    client = gspread.authorize(creds)

    return client.open(SHEET_NAME).sheet1


async def check_birthdays(context: ContextTypes.DEFAULT_TYPE):

    sheet = get_sheet()
    data = sheet.get_all_records()

    today = datetime.datetime.now(pytz.timezone("Europe/Moscow"))

    for row in data:

        name = row.get("ФИО")
        birthday = row.get("День Рождения")

        if not birthday:
            continue

        birth_date = datetime.datetime.strptime(birthday, "%d.%m.%Y")

        if birth_date.day == today.day and birth_date.month == today.month:

            age = today.year - birth_date.year

            message = (
                f"🎉 С Днем Рождения, {name}! 🎂\n"
                f"Сегодня исполняется {age} лет!\n"
                f"Желаем счастья, здоровья и отличного настроения! 🥳"
            )

            await context.bot.send_message(
                chat_id=CHAT_ID,
                text=message
            )

            print(f"Поздравление отправлено: {name}")


async def post_init(application: Application):

    tz = pytz.timezone("Europe/Moscow")

    application.job_queue.run_daily(
        check_birthdays,
        time=datetime.time(hour=9, minute=0, tzinfo=tz)
    )

    print("Бот запущен")


def main():

    application = (
        Application.builder()
        .token(TOKEN)
        .post_init(post_init)
        .build()
    )

    application.run_polling()


if __name__ == "__main__":
    main()
