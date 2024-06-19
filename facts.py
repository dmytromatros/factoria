import json
import requests
import telebot
from ai import get_info
import threading
import time

TOKEN = "6166389096:AAEpzkodY_mEy150dBO6jahxSrT6rd3_tDs"
CHANEL_ID = "@factoriafact"
bot = telebot.TeleBot(TOKEN, parse_mode=None)


def post_new_fact():
    while True:
        try:
            fact = get_info(
                prompt="""Будь ласка, надайте цікавий, точний та короткий факт про будь-що (без зайвого тексту), не повторюючи попередні факти, щоб було різноманіття тем. Факт має бути українською мовою, а title (назва) - англійською. 

Це може бути щось грандіозне або маленьке, наприклад, для чого маленький карман на джинсах. Факт може бути не лише про Україну, а й про весь світ. 

Важливо: Ваша відповідь має бути у форматі JSON. Якщо відповідь не у форматі JSON, з'явиться повідомлення про помилку. 

Ось приклад структури JSON, яку я очікую:
{
  "fact": "Чи знаєте ви, що на Місяці є пагорби, названі на честь українських науковців? Один з них - пагорб Кобзаря, названий на честь Тараса Шевченка.",
  "title": "Moon Hills"
}

(title - це для факту англійською мовою, що описує та передає суть факту (щоб можна було знайти картинку для цього факту), а якщо йдеться про власну назву, то вказуйте її, наприклад, "Говерла").

Помилка: Якщо ви не надасте відповідь у форматі JSON, я попрошу вас спробувати ще раз з чіткішими інструкціями.

Зверніть увагу:
- Ваша відповідь має бути у форматі JSON.
- Кожен факт має бути унікальним і не повторювати попередні теми.
- Використовуйте чітку та зрозумілу мову.

Приклад неправильної відповіді:
{
  "fact": "Це факт без назви",
  "title": "No Title"
}

Приклад правильної відповіді:
{
  "fact": "Чи знаєте ви, що Говерла - найвища гора України, висота якої становить 2061 метр?",
  "title": "Hoverla"
}
""")

            new_fact = fact.replace('`json', '').replace('`', '')

            data = json.loads(new_fact)
            break

        except json.JSONDecodeError:
            print("Неправильний формат JSON. Спробуйте ще раз.")

    access_key = 'czJxCx6w75YUOwXJSYxvoGuPtxXU6nke0gf8LGDu4wM'  # Заміни на твій справжній токен доступу
    url = 'https://api.unsplash.com/search/photos'
    params = {
        'page': 1,
        'query': data['title']
    }
    headers = {
        'Authorization': f'Client-ID {access_key}'
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        img_json = json.loads(response.content)
        img_link = img_json["results"][0]["urls"]["regular"]
        bot.send_photo(CHANEL_ID, img_link, caption=data["fact"], parse_mode='HTML')

    except Exception as e:
        print(f"Помилка при завантаженні зображення: {e}")


def repeat_every_30_minutes():
    while True:
        post_new_fact()
        time.sleep(1800)  # 30 minutes in seconds


thread1 = threading.Thread(target=repeat_every_30_minutes)
thread1.start()

# post_new_fact()  # Remove this line if you don't want to publish the first fact immediately

bot.infinity_polling()
