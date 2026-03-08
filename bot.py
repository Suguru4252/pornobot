"""
Telegram бот для взрослых (18+)
Функции:
- Выбор персонажа (девушка/парень) через инлайн-кнопки
- Развратные ответы на сообщения пользователя
- Эмуляция "ИИ" на основе ключевых слов
- Команда /stop для остановки диалога
"""

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import re

# ==================== НАСТРОЙКИ ====================
TOKEN = '8442213004:AAFgM1lchfhZmh5SxzrumH9nCR2TQzvCEos'
bot = telebot.TeleBot(TOKEN)

# Хранилище выбранных персонажей для каждого пользователя
user_character = {}

# ==================== БАЗЫ ОТВЕТОВ ====================
# Ответы для парня
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
        'Я раздвину твои ягодицы и войду'
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
        'Я кончу тебе между сисек'
    ],
    'рот': [
        'Открой рот шире, я залью тебе глотку спермой',
        'Соси аккуратнее, зубами не задень',
        'Глубже бери, учись соснуть',
        'Работай язычком, как будто это мой член',
        'Возьми мой член в рот'
    ],
    'стоп': [
        'Ладно, останавливаем игру. Если захочешь продолжить - просто напиши',
        'Окей, диалог остановлен. Для продолжения просто напиши что-нибудь',
        'Как скажешь, останавливаю. Пиши если захочешь продолжить'
    ]
}

# Ответы для девушки
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
        'Выеби меня так, чтобы я кричала'
    ],
    'член': [
        'Оближи его для меня, а потом войди в мою мокрую киску',
        'Какой у тебя размер? Люблю, когда глубоко и больно',
        'Хочу взять его в ротик и сосать'
    ],
    'попа': [
        'Засунь его в мою попку, я сегодня хочу погорячее',
        'Оттрахай меня в попу, как последнюю шлюху',
        'Моя попка сжата и ждет тебя'
    ],
    'кончить': [
        'Кончай в меня... залей мою матку своей спермой',
        'Я хочу чувствовать, как ты пульсируешь внутри меня',
        'На лицо кончи, я открою ротик'
    ],
    'стоп': [
        'Ладно, останавливаем игру. Если захочешь продолжить - просто напиши',
        'Окей, диалог остановлен. Для продолжения просто напиши что-нибудь',
        'Как скажешь, останавливаю. Пиши если захочешь продолжить'
    ]
}

# Универсальные ответы (если ключевое слово не найдено)
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
        "Здесь ты можешь общаться с развратными персонажами.\n\n"
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
        "*Как это работает:*\n"
        "1. Напиши /start и выбери персонажа\n"
        "2. Просто пиши любые сообщения\n"
        "3. Бот отвечает как выбранный персонаж\n"
        "4. /stop - остановить диалог\n\n"
        "*Примеры:* привет, как дела, хочу секс"
    )
    bot.send_message(chat_id, help_text, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    
    if call.data == "char_girl":
        user_character[chat_id] = 'girl'
        bot.edit_message_text(
            "✅ Ты выбрал *Развратную девушку*\n"
            "Она горяча, игрива и всегда готова.\n\n"
            "💡 *Чтобы остановить диалог, напиши /stop*",
            chat_id,
            message_id,
            parse_mode="Markdown"
        )
    
    elif call.data == "char_boy":
        user_character[chat_id] = 'boy'
        bot.edit_message_text(
            "✅ Ты выбрал *Пошлого парня*\n"
            "Он груб, доминантен и знает как заставить тебя кончить.\n\n"
            "💡 *Чтобы остановить диалог, напиши /stop*",
            chat_id,
            message_id,
            parse_mode="Markdown"
        )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    
    if chat_id not in user_character:
        if message.text.lower() in ['стоп', 'хватит', 'stop']:
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
        bot.send_message(chat_id, f"{emoji} {response}")
        
        del user_character[chat_id]
        
        bot.send_message(
            chat_id,
            "⏸️ *Диалог остановлен*\nЧтобы начать заново, напиши /start",
            parse_mode="Markdown"
        )
        return
    
    response = get_response(chat_id, message.text)
    emoji = '💋' if user_character[chat_id] == 'girl' else '🍆'
    bot.send_message(chat_id, f"{emoji} {response}")

# ==================== ЗАПУСК ====================
if __name__ == "__main__":
    print("=" * 50)
    print("✅ Бот ЗАПУЩЕН!")
    print("📝 Токен: 8442213004:AAFgM1lchfhZmh5SxzrumH9nCR2TQzvCEos")
    print("👥 Персонажи: Девушка 💋 и Парень 🍆")
    print("🛑 Нажми Ctrl+C для остановки")
    print("=" * 50)
    
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        print("\n❌ Бот остановлен")
