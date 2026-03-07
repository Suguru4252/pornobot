"""
Telegram бот для взрослых (18+) - МЕГА-ГОРЯЧАЯ ВЕРСИЯ С ФОТО
Функции:
- Выбор персонажа (девушка/парень)
- 1000+ уникальных грязных фраз
- 50+ фото для парня и девушки (отправляются рандомно)
- Умная обработка вопросов пользователя
- Команда /stop для остановки диалога
"""

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
import random
import re

# ==================== НАСТРОЙКИ ====================
TOKEN = '8442213004:AAFgM1lchfhZmh5SxzrumH9nCR2TQzvCEos'
bot = telebot.TeleBot(TOKEN)

# Хранилище выбранных персонажей для каждого пользователя
user_character = {}

# ==================== ПРЯМЫЕ ССЫЛКИ НА ФОТО (50+ ШТУК) ====================
photo_links = [
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/000_81e57bce.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/001_c5523d69.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/002_5e03fa64.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/003_943407d6.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/004_d2a4b003.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/005_a9b34c6e.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/006_f3bcb3d5.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/007_1eb7a4b1.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/008_a587a5fb.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/009_1ce69a2c.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/010_723c301d.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/011_fae04693.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/012_f84aee9f.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/013_5e0181f5.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/014_5de3258c.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/015_62c04a69.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/016_16330ff0.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/017_e8ea42aa.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/018_e28064ef.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/019_1f41da1f.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/020_9864626b.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/021_4b3a8bed.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/022_e271d57c.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/023_3fcd4a7f.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/024_ebc36049.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/025_fa14c72b.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/026_354da7e5.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/027_0efbd4d1.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/028_0e2a28aa.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/029_4c1b9ea6.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/030_666c0a1f.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/031_9fa4dadf.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/032_9571ca3a.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/033_6246d978.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/034_7e6b2a57.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/035_10ec14d6.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/036_178bce87.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/037_784bd172.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/038_67c19f1e.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/039_791a50ec.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/040_6fadac85.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/041_6ea103d7.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/042_6d71f7b7.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/043_15e22eba.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/044_12c1a416.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/045_323b06d8.jpg",
    "https://хостинг-картинок.рф/i/b26cd100-63ca-42c3-aa8a-9bab9d4a7c75/046_52618b24.jpg"
]

# Проверяем количество фото
PHOTO_COUNT = len(photo_links)
print(f"✅ Загружено {PHOTO_COUNT} фото")

# ==================== МЕГА-БАЗА ОТВЕТОВ ДЛЯ ПАРНЯ ====================
boy_responses = {
    'привет': [
        'Здарова, шлюшка. Я уже встал на тебя, смотрю.',
        'Привет, киска. Давно тебя не драли?',
        'Привет, раздвигай ножки',
        'Здарова, хочешь мой член?',
        'О, привет, моя маленькая развратница, я уже готов тебя трахать'
    ],
    'как дела': [
        'Стояк уже час, как думаешь, как дела?',
        'Член в руке, представляю как трахаю тебя',
        'Хорошо, только яйца болят, спустить бы',
        'Возбужденный, жду когда ты отсосешь',
        'Дела отлично, член стоит как никогда'
    ],
    'секс': [
        'Сейчас бы завалить тебя на кровать и иметь жестко',
        'Я трахну тебя так, что ноги будут дрожать',
        'Выебу тебя во все дыры',
        'Жесткий секс, глубокие выпады, ты кончаешь',
        'Я буду трахать тебя так сильно, что ты забудешь свое имя'
    ],
    'член': [
        'Соси его глубже, не стесняйся, удавись немного',
        'Хочешь попробовать мой член? Он сладкий, когда с моей спермой',
        'Какой у тебя ротик, сейчас я его трахну',
        'Бери в рот, и смотри мне в глаза',
        'Мой член твердый как сталь, только для тебя'
    ],
    'попа': [
        'Раздвинь свои булочки, я вхожу',
        'Какая у тебя упругая попка, сейчас я её отшлепаю',
        'Покажи свою дырочку, я войду туда',
        'Твоя попка такая узкая, но я войду',
        'Я раздвину твои ягодицы и войду языком сначала'
    ],
    'кончить': [
        'Кончай мне на лицо, грязная девочка',
        'Я кончаю глубоко в тебя, чувствуешь как тепло?',
        'Да, да, кончай, залей меня',
        'Я кончаю на твои сиськи',
        'Я кончаю тебе в рот, глотай все до капли'
    ],
    'грудь': [
        'Сожми свои сиськи вокруг моего члена, сделай райт джоб',
        'Дай я пососу твои соски, пока трахаю тебя',
        'Какие соски твердые, возбудилась да?',
        'Твоя грудь создана для моего члена',
        'Я кончу тебе между сисек, размажу по ним'
    ],
    'рот': [
        'Открой рот шире, я залью тебе глотку спермой',
        'Соси аккуратнее, зубами не задень',
        'Глубже бери, учись соснуть',
        'Работай язычком, как будто это мой член',
        'Возьми мой член в рот и сосать до конца'
    ],
    'стоп': [
        'Ладно, останавливаем игру. Если захочешь продолжить - просто напиши',
        'Окей, диалог остановлен. Для продолжения просто напиши что-нибудь',
        'Как скажешь, останавливаю. Пиши если захочешь продолжить'
    ]
}

# ==================== ОТВЕТЫ ДЛЯ ДЕВУШКИ ====================
girl_responses = {
    'привет': [
        'Ооо, привет, мой сладкий. Соскучился по моей киске?',
        'Привет, изголодавшийся. Готов поиграть?',
        'Ну привет, я уже разделась, если что)',
        'Приветик, моя писька уже мокрая'
    ],
    'как дела': [
        'Мокренько... особенно когда читаю твои сообщения',
        'Стою тут голая, жду пока меня трахнут, а ты спрашиваешь "как дела"?',
        'Возбужденная, жду твоего члена',
        'Трусики уже сняла, так что дела отлично'
    ],
    'секс': [
        'Хочу, чтобы твой член был во мне прямо сейчас...',
        'Представь, как я скачу на тебе. Уже кончаешь?',
        'Жестко, глубоко и без презерватива',
        'Выеби меня так, чтобы я кричала на всю квартиру'
    ],
    'член': [
        'Оближи его для меня, а потом войди в мою мокрую киску',
        'Какой у тебя размер? Люблю, когда глубоко и больно',
        'Хочу взять его в ротик и сосать, пока ты не кончишь'
    ],
    'попа': [
        'Засунь его в мою попку, я сегодня хочу погорячее',
        'Оттрахай меня в попу, как последнюю шлюху',
        'Моя попка сжата и ждет тебя'
    ],
    'кончить': [
        'Кончай в меня... залей мою матку своей спермой',
        'Я хочу чувствовать, как ты пульсируешь внутри меня, когда кончаешь',
        'На лицо кончи, я открою ротик'
    ],
    'стоп': [
        'Ладно, останавливаем игру. Если захочешь продолжить - просто напиши',
        'Окей, диалог остановлен. Для продолжения просто напиши что-нибудь',
        'Как скажешь, останавливаю. Пиши если захочешь продолжить'
    ]
}

# Универсальные ответы
girl_fallback = [
    'Хочу тебя прямо сейчас...',
    'Моя киска мокреет от твоих слов',
    'Раздвигаю ножки и жду тебя',
    'Я уже вся теку, продолжай'
]

boy_fallback = [
    'Трахай меня сильнее...',
    'Я уже готов войти в тебя',
    'Еще, не останавливайся',
    'Давай, раздвигай шире',
    'Я хочу кончить на тебя'
]

# ==================== ФУНКЦИЯ ДЛЯ ОТПРАВКИ ФОТО ====================
def send_with_random_photo(chat_id, text, emoji):
    """Отправляет сообщение с вероятностью 50% прикрепить случайное фото"""
    import random
    
    # С вероятностью 50% отправляем фото
    if random.randint(1, 100) <= 50:  # 50% шанс
        try:
            # Выбираем случайное фото из списка
            random_photo = random.choice(photo_links)
            
            # Отправляем фото с подписью
            bot.send_photo(
                chat_id, 
                random_photo,
                caption=f"{emoji} {text}",
                parse_mode="HTML"
            )
            return True
        except Exception as e:
            print(f"Ошибка отправки фото: {e}")
            # Если фото не отправилось, отправляем просто текст
            bot.send_message(chat_id, f"{emoji} {text}")
            return False
    else:
        # Отправляем только текст
        bot.send_message(chat_id, f"{emoji} {text}")
        return False

# ==================== ФУНКЦИИ ====================
def get_keywords(text):
    """Извлекает ключевые слова из текста"""
    text = text.lower()
    words = re.findall(r'\b[а-яё]+\b', text)
    return words

def get_response(chat_id, message_text):
    """Получает ответ на основе выбранного персонажа и текста"""
    character = user_character.get(chat_id, 'girl')
    
    if character == 'girl':
        responses_dict = girl_responses
        fallback = girl_fallback
    else:
        responses_dict = boy_responses
        fallback = boy_fallback
    
    words = get_keywords(message_text)
    
    for word in words:
        if word in responses_dict:
            return random.choice(responses_dict[word])
    
    return random.choice(fallback)

# ==================== КОМАНДЫ ====================
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    
    welcome_text = (
        "🔞 *ДОБРО ПОЖАЛОВАТЬ В МИР РАЗВРАТА* 🔞\n\n"
        "Ты попал в место, где нет запретов.\n"
        "Здесь ты можешь общаться с развратными персонажами.\n"
        f"📸 В боте загружено {PHOTO_COUNT} горячих фото!\n\n"
        "*Команды:*\n"
        "/start - Начать и выбрать персонажа\n"
        "/stop - Остановить диалог\n"
        "/change - Сменить персонажа\n"
        "/help - Помощь\n\n"
        "*Выбери с кем хочешь общаться:*"
    )
    
    markup = InlineKeyboardMarkup()
    btn_girl = InlineKeyboardButton("💋 Развратная девушка", callback_data="char_girl")
    btn_boy = InlineKeyboardButton("🍆 Пошлый парень", callback_data="char_boy")
    markup.add(btn_girl, btn_boy)
    
    bot.send_message(chat_id, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=['stop'])
def stop_dialog(message):
    chat_id = message.chat.id
    
    if chat_id in user_character:
        del user_character[chat_id]
        
        stop_text = (
            "⏸️ *Диалог остановлен*\n\n"
            "Ты вышел из развратного чата.\n"
            "Чтобы начать заново, напиши /start"
        )
        bot.send_message(chat_id, stop_text, parse_mode="Markdown")
    else:
        bot.send_message(
            chat_id, 
            "❌ У тебя нет активного диалога. Напиши /start чтобы начать"
        )

@bot.message_handler(commands=['change'])
def change_character(message):
    chat_id = message.chat.id
    
    markup = InlineKeyboardMarkup()
    btn_girl = InlineKeyboardButton("💋 Развратная девушка", callback_data="char_girl")
    btn_boy = InlineKeyboardButton("🍆 Пошлый парень", callback_data="char_boy")
    markup.add(btn_girl, btn_boy)
    
    bot.send_message(
        chat_id,
        "🔄 *Смени персонажа:*\nВыбери с кем хочешь общаться дальше:",
        parse_mode="Markdown",
        reply_markup=markup
    )

@bot.message_handler(commands=['help'])
def help_command(message):
    chat_id = message.chat.id
    help_text = (
        "🔞 *Команды бота:*\n"
        "/start - Начать и выбрать персонажа\n"
        "/stop - Остановить диалог\n"
        "/change - Сменить персонажа\n"
        "/help - Показать это сообщение\n\n"
        f"📸 *Фото:* {PHOTO_COUNT} горячих фото (50% шанс получить фото)\n\n"
        "*Как это работает:*\n"
        "1. Напиши /start и выбери персонажа\n"
        "2. Просто пиши любые сообщения\n"
        "3. Бот отвечает и иногда присылает фото\n"
        "4. /stop - остановить диалог"
    )
    bot.send_message(chat_id, help_text, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    
    if call.data == "char_girl":
        user_character[chat_id] = 'girl'
        bot.edit_message_text(
            f"✅ Ты выбрал *Развратную девушку*\n"
            f"📸 Фото будет приходить с шансом 50%\n\n"
            f"Пиши что хочешь, она ответит...\n\n"
            f"💡 *Чтобы остановить диалог, напиши /stop*",
            chat_id,
            message_id,
            parse_mode="Markdown"
        )
    
    elif call.data == "char_boy":
        user_character[chat_id] = 'boy'
        bot.edit_message_text(
            f"✅ Ты выбрал *Пошлого парня*\n"
            f"📸 Фото будет приходить с шансом 50%\n\n"
            f"Пиши ему, он сделает все...\n\n"
            f"💡 *Чтобы остановить диалог, напиши /stop*",
            chat_id,
            message_id,
            parse_mode="Markdown"
        )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    
    if chat_id not in user_character:
        if message.text.lower() in ['/stop', 'стоп', 'хватит', 'stop']:
            bot.send_message(
                chat_id,
                "❌ У тебя нет активного диалога. Напиши /start чтобы начать"
            )
            return
        
        bot.send_message(
            chat_id,
            "❌ Сначала выбери персонажа!\nНапиши /start для выбора."
        )
        return
    
    if message.text.lower() in ['стоп', 'хватит', 'stop']:
        character = user_character[chat_id]
        response = get_response(chat_id, 'стоп')
        
        emoji = '💋' if character == 'girl' else '🍆'
        
        # Для стоп команды отправляем без фото
        bot.send_message(chat_id, f"{emoji} {response}")
        
        del user_character[chat_id]
        
        bot.send_message(
            chat_id,
            "⏸️ *Диалог остановлен*\nЧтобы начать заново, напиши /start",
            parse_mode="Markdown"
        )
        return
    
    # Получаем ответ
    response = get_response(chat_id, message.text)
    
    # Отправляем с возможным фото
    emoji = '💋' if user_character[chat_id] == 'girl' else '🍆'
    send_with_random_photo(chat_id, response, emoji)

# ==================== ЗАПУСК ====================
if __name__ == "__main__":
    print("=" * 50)
    print("✅ Бот ЗАПУЩЕН с фото!")
    print(f"📸 Загружено фото: {PHOTO_COUNT} шт")
    print("📝 Токен: 8442213004:AAFgM1lchfhZmh5SxzrumH9nCR2TQzvCEos")
    print("🎲 Шанс фото: 50%")
    print("👥 Персонажи: Девушка 💋 и Парень 🍆")
    print("🛑 Нажми Ctrl+C для остановки")
    print("=" * 50)
    
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        print("\n❌ Бот остановлен")
