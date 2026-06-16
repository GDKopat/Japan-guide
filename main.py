import requests,re,random,time,os,json
from bs4 import BeautifulSoup
from urllib.parse import quote


###
###
###
GITHUB_RAW_URL = "https://raw.githubusercontent.com/Nikitoskaaa/Japan-facts/refs/heads/main/japan_facts.txt"
BOT_EMAIL = "your_email@example.com"  # <-- СЮДА ВСТАВИТЬ СВОЮ ПОЧТУ! ! !
###
###
###

def get_random_fact_from_github():
    clear_console()
    try:
        response = requests.get(GITHUB_RAW_URL,timeout=10)
        response.raise_for_status()
        facts = response.text.strip().split("\n")
        facts = [fact.strip() for fact in facts if fact.strip()]
        fact = random.choice(facts)
        print(f"\n🌸 Случайный факт о Японии: {fact}\n")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка соединения: {e}. Проверьте интернет или ссылку.")


def get_first_paragraph(city):
    clear_console()

    url = f"https://ru.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro&explaintext&titles={quote(city)}"
    headers = {
    'User-Agent': f'MyJapanGuideBot/1.0 (https://github.com/GDKopat/Japan-guide; {BOT_EMAIL})'
}
    session = requests.Session()

    for attempt in range(3):  # 3 попытки с задержкой
        try:
            resp = session.get(url, headers=headers, timeout=10)

            # Если статус не 200, пробуем с другим User-Agent
            if resp.status_code != 200:
                print(f"⚠️ Статус {resp.status_code}. Повтор через 5 сек...")
                time.sleep(5)
                continue

            # Проверяем, что пришёл именно JSON
            content_type = resp.headers.get('Content-Type', '')
            if 'application/json' not in content_type:
                # Возможно, вернулась капча или HTML
                if 'captcha' in resp.text.lower() or 'block' in resp.text.lower():
                    print("❌ Википедия запросила капчу. Попробуйте позже или используйте VPN.")
                    return None
                print("❌ Сервер вернул не JSON. Проверьте название города.")
                return None

            data = resp.json()
            pages = data.get('query', {}).get('pages', {})
            for page_id, page in pages.items():
                if 'extract' in page:
                    text = page['extract'].strip()
                    if text:
                        print(f"\n📖 📖 📖 {city}:\n{text}\n")
                        return text
                    else:
                        print(f"❌ Для города {city} нет текста.")
                        return None
            print(f"❌ Город {city} не найден в Википедии.")
            return None

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Ошибка соединения: {e}. Повтор через 5 сек...")
            time.sleep(5)
        except json.JSONDecodeError:
            print("⚠️ Ответ не является JSON. Возможно, блокировка. Повтор через 10 сек...")
            time.sleep(10)
        except Exception as e:
            print(f"⚠️ Неизвестная ошибка: {e}")
            return None

    print("❌ Не удалось получить данные после 3 попыток.")
    return None


def get_temperature(city):
    clear_console()
    try:
        print("парсим...")
        link = f"https://wttr.in/{city}?format=%t&lang=ru"
        x = requests.get(link).text
        if "location not found" in x.lower() or not x:
            print(f"Ненашлось города |-> {city} <-| попробуйте скопировать название города и вставить")
            return
        x = x.replace("°C", "")
        x = x.replace("Â", "")
        print(f"В городе {city} {x} градусов 🌡️")
    except(requests.exceptions.RequestException) as e:
        print(f"Не удалось узнать погоду в {city} ошибка: '{e}'")


def get_daily_quote():
    clear_console()
    print("парсим...")
    try:
        url = "https://meowfacts.herokuapp.com/?lang=rus"
        response = requests.get(url)
        data = response.json()
        fact = data["data"][0]
        print(f"Факт про кошек: {fact}")
    except Exception as e:
        print(f"Не удалось получить факт о кошках: {e}")


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def exit_program():
    print("До свидания! Спасибо, что пользуешься гидом.")
    exit(0)


menu = {
    "1": get_random_fact_from_github,
    "2": lambda: get_first_paragraph(input("Введите название города или места (например, Токио, Осака, Киото, Гора Фудзи): ")),
    "3": get_daily_quote,
    "4": lambda: get_temperature(input("Введите название города (например, Токио, Осака, Киото): ")),
    "0": exit_program
}


def main():
    while True:
        print("\n" + "🌸"*10)
        print("    ГИД ПО ЯПОНИИ ")
        print("🌸"*10)
        print("""
1 - Случайный факт о Японии ⛩️
2 - Узнать о городе/месте 🔍
3 - Случайный факт про кошек 🐱
4 - Погода в городе 🌦️
0 - Выход 💔💔💔""")
        choice = input("Твой выбор: ")
        if choice in menu:
            menu[choice]()
        else:
            print("Некорректный ввод, попробуй ещё раз.")


if __name__ == "__main__":
    main()
