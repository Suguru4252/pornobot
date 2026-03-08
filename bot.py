"""
Telegram бот для взрослых (18+) - МЕГА ВЕРСИЯ С ЧАТОМ
Функции:
- 4 персонажа для виртуального секса (девушка/парень/гей/лесби)
- ОНЛАЙН ЧАТ с разными комнатами (гей/лесби/микс/все)
- Анонимное общение, фото, видео, голосовые
- Виртуальный секс с подсчетом возбуждения
"""

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import re
import time
from datetime import datetime

# ==================== НАСТРОЙКИ ====================
TOKEN = '8442213004:AAFgM1lchfhZmh5SxzrumH9nCR2TQzvCEos'
bot = telebot.TeleBot(TOKEN)

# ==================== ХРАНИЛИЩА ДАННЫХ ====================
# Для виртуального секса
user_character = {}  # 'girl', 'boy', 'gay', 'lesbian'
user_arousal = {}  # {chat_id: {'level': 0, 'actions': []}}

# ==================== НОВОЕ: ОНЛАЙН ЧАТ ====================
# Комнаты чата
CHAT_ROOMS = {
    'gay': '🏳️‍🌈 Гей чат (только парни)',
    'lesbian': '👩‍❤️‍👩 Лесби чат (только девушки)',
    'mixed': '💑 Смешанный чат (парни + девушки)',
    'everyone': '🌍 Общий чат (все подряд)'
}

# Пользователи в чатах: {room: {user_id: {'username': '...', 'gender': '...'}}}
chat_users = {
    'gay': {},
    'lesbian': {},
    'mixed': {},
    'everyone': {}
}

# История сообщений в чатах (последние 50 сообщений)
chat_history = {
    'gay': [],
    'lesbian': [],
    'mixed': [],
    'everyone': []
}

# Временные пары для приватного чата (1-на-1)
private_pairs = {}  # {user1: user2, user2: user1}

# ==================== НОВЫЕ ПЕРСОНАЖИ: ГЕЙ И ЛЕСБИ ====================
gay_responses = {
    'привет': [
        'Привет, сладкий. Я уже готов встать раком...',
        'Здарова, парень. Хочешь мой член?',
        'Привет, красавчик. Раздевайся давай...',
        'Ооо, привет, я уже голый, жду тебя...'
    ],
    'как дела': [
        'Член стоит, жду когда ты его возьмешь в рот...',
        'Хорошо, только яйца болят, спустить бы в тебя...',
        'Возбужденный, жду когда ты войдешь в меня...',
        'Отлично, только попка скучает по члену...'
    ],
    'член': [
        'Соси мой член, глубже, в самое горло...',
        'Какой у тебя большой, войди в меня...',
        'Дай я возьму твой член в рот и оближу головку...',
        'Я кончу на твой член, залью его спермой...'
    ],
    'попа': [
        'Раздвинь мою попку и войди в дырочку...',
        'Я уже смазал свою попку, входи глубже...',
        'Трахай мою попку жестко, разорви меня...',
        'Моя попка узкая, но для тебя я расслаблюсь...'
    ],
    'кончить': [
        'Кончи в мою попку, залей меня спермой...',
        'Я кончаю на твой член, чувствуешь как горячо...',
        'Кончи мне в рот, я все проглочу...',
        'Мы кончаем вместе, да, еще, глубже...'
    ],
    'сосать': [
        'Я беру твой член в рот и сосу до конца...',
        'Соси мой член, нежно, язычком по головке...',
        'Мы сосем друг другу, это так возбуждающе...'
    ]
}

lesbian_responses = {
    'привет': [
        'Привет, моя сладкая. Я уже мокрая...',
        'Здарова, киска. Хочешь попробовать меня?',
        'Привет, я голая, трогаю себя пальчиком...',
        'Ооо, привет, моя писька ждет тебя...'
    ],
    'как дела': [
        'Мокренько, пальчик в киске, тебя жду...',
        'Хорошо, только клитор хочет ласки...',
        'Возбужденная, трусь о подушку...',
        'Отлично, трусики уже сняла...'
    ],
    'киска': [
        'Полижи мою киску, я такая мокрая...',
        'Введи пальчики в мою киску, глубже...',
        'Я трусь клитором о твою киску...',
        'Моя киска пульсирует, хочу тебя...'
    ],
    'клитор': [
        'Полижи мой клитор, он такой чувствительный...',
        'Я тру клитор о твой пальчик...',
        'Массируй мой клитор язычком, я кончаю...'
    ],
    'палец': [
        'Введи пальцы в меня, два сразу...',
        'Я массирую твою киску пальцами...',
        'Пальцы внутри меня, я почти кончаю...'
    ],
    'кончить': [
        'Мы кончаем вместе, обнимая друг друга...',
        'Я кончаю на твои пальцы, не останавливайся...',
        'Кончи в меня, залей мою киску...'
    ]
}

# Добавляем новые словари в общий список
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
    ]
}

boy_responses = {
    'привет': [
        'Здарова, шлюшка. Я уже встал на тебя, смотрю.',
        'Привет, киска. Давно тебя не драли?',
        'Привет, раздвигай ножки',
        'Здарова, хочешь мой член?'
    ],
    'как дела': [
        'Стояк уже час, как думаешь, как дела?',
        'Член в руке, представляю как трахаю тебя',
        'Хорошо, только яйца болят, спустить бы',
        'Возбужденный, жду когда ты отсосешь'
    ],
    'секс': [
        'Сейчас бы завалить тебя на кровать и иметь жестко',
        'Я трахну тебя так, что ноги будут дрожать',
        'Выебу тебя во все дыры',
        'Жесткий секс, глубокие выпады'
    ],
    'член': [
        'Соси его глубже, не стесняйся, удавись немного',
        'Хочешь попробовать мой член? Он сладкий, когда с моей спермой',
        'Какой у тебя ротик, сейчас я его трахну'
    ],
    'попа': [
        'Раздвинь свои булочки, я вхожу',
        'Какая у тебя упругая попка, сейчас я её отшлепаю',
        'Покажи свою дырочку, я войду туда'
    ],
    'кончить': [
        'Кончай мне на лицо, грязная девочка',
        'Я кончаю глубоко в тебя, чувствуешь как тепло?',
        'Я кончаю на твои сиськи'
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

gay_fallback = [
    'Войди в мою попку...',
    'Я хочу твой член в себе...',
    'Соси меня, я люблю это...',
    'Трахай меня жестко...'
]

lesbian_fallback = [
    'Я мокрая для тебя...',
    'Пальчики в моей киске...',
    'Поцелуй мой клитор...',
    'Я кончаю от твоих рук...'
]

# ==================== ФУНКЦИИ ДЛЯ ЧАТА ====================
def get_user_gender(user_id):
    """Определяет пол пользователя по выбранному персонажу"""
    char = user_character.get(user_id, 'unknown')
    if char in ['boy', 'gay']:
        return 'male'
    elif char in ['girl', 'lesbian']:
        return 'female'
    return 'unknown'

def add_to_chat(user_id, username, room):
    """Добавляет пользователя в комнату чата"""
    # Удаляем из всех комнат сначала
    for r in chat_users:
        if user_id in chat_users[r]:
            del chat_users[r][user_id]
    
    # Добавляем в новую комнату
    gender = get_user_gender(user_id)
    chat_users[room][user_id] = {
        'username': username,
        'gender': gender,
        'joined': time.time()
    }
    
    # Уведомление в чат
    welcome_msg = f"👤 Пользователь {username} присоединился к чату!"
    chat_history[room].append({
        'type': 'system',
        'text': welcome_msg,
        'time': datetime.now().strftime("%H:%M")
    })
    
    return True

def remove_from_chat(user_id):
    """Удаляет пользователя из всех чатов"""
    for room in chat_users:
        if user_id in chat_users[room]:
            username = chat_users[room][user_id]['username']
            del chat_users[room][user_id]
            
            # Уведомление
            leave_msg = f"👋 Пользователь {username} покинул чат"
            chat_history[room].append({
                'type': 'system',
                'text': leave_msg,
                'time': datetime.now().strftime("%H:%M")
            })
            return room

def broadcast_to_room(room, user_id, message_text, message_type='text', file_id=None):
    """Отправляет сообщение всем в комнате"""
    sender = chat_users[room].get(user_id, {})
    if not sender:
        return False
    
    username = sender['username']
    gender_emoji = '👨' if sender['gender'] == 'male' else '👩' if sender['gender'] == 'female' else '👤'
    
    # Сохраняем в историю
    msg_data = {
        'type': message_type,
        'user': username,
        'gender': sender['gender'],
        'time': datetime.now().strftime("%H:%M"),
        'text': message_text if message_type == 'text' else None,
        'file_id': file_id
    }
    chat_history[room].append(msg_data)
    
    # Ограничиваем историю до 50 сообщений
    if len(chat_history[room]) > 50:
        chat_history[room] = chat_history[room][-50:]
    
    # Рассылаем всем в комнате
    for uid in chat_users[room]:
        if uid != user_id:  # Не отправляем себе
            try:
                if message_type == 'text':
                    bot.send_message(
                        uid, 
                        f"{gender_emoji} [{msg_data['time']}] {username}: {message_text}"
                    )
                elif message_type == 'photo':
                    bot.send_photo(
                        uid, 
                        file_id,
                        caption=f"{gender_emoji} [{msg_data['time']}] {username} отправил фото"
                    )
                elif message_type == 'video':
                    bot.send_video(
                        uid, 
                        file_id,
                        caption=f"{gender_emoji} [{msg_data['time']}] {username} отправил видео"
                    )
                elif message_type == 'voice':
                    bot.send_voice(
                        uid, 
                        file_id,
                        caption=f"{gender_emoji} [{msg_data['time']}] {username} отправил голосовое"
                    )
            except:
                pass
    
    return True

# ==================== ФУНКЦИИ ДЛЯ СЕКСА ====================
def get_sex_action(character, action_type):
    """Возвращает случайное грязное действие"""
    if character == 'boy':
        # Для парня с девушкой
        actions = {
            'член': sex_actions['male']['член'],
            'палец': sex_actions['male']['палец'],
            'язык': sex_actions['male']['язык'],
            'рак': sex_actions['male']['рак'],
            'сосать': sex_actions['male']['сосать'],
            'кончить': sex_actions['male']['кончить']
        }
    elif character == 'gay':
        # Для гея
        actions = {
            'член': sex_actions['male']['член'],
            'попа': sex_actions['male']['попа'],
            'сосать': sex_actions['male']['сосать'],
            'кончить': sex_actions['male']['кончить']
        }
    elif character == 'lesbian':
        # Для лесбиянки
        actions = {
            'киска': sex_actions['female']['киска'],
            'клитор': sex_actions['female']['клитор'],
            'палец': sex_actions['female']['палец'],
            'язык': sex_actions['female']['язык'],
            'кончить': sex_actions['female']['кончить']
        }
    else:  # girl
        actions = {
            'киска': sex_actions['female']['киска'],
            'клитор': sex_actions['female']['клитор'],
            'сосать': sex_actions['female']['сосать'],
            'кончить': sex_actions['female']['кончить']
        }
    
    if action_type in actions:
        return random.choice(actions[action_type])
    return None

def update_arousal(chat_id):
    """Обновляет уровень возбуждения"""
    arousal_levels = [
        "😈 Ты только начинаешь возбуждаться...",
        "🔥 Уже горячо, тело горит...",
        "💦 Ты весь мокрый, еще немного...",
        "🌊 Ты на грани, еще чуть-чуть...",
        "💥 ТЫ КОНЧАЕШЬ! Сильно и глубоко!"
    ]
    
    if chat_id not in user_arousal:
        user_arousal[chat_id] = {'level': 0, 'actions': []}
    
    user_arousal[chat_id]['level'] += random.randint(1, 3)
    
    if user_arousal[chat_id]['level'] >= len(arousal_levels):
        user_arousal[chat_id]['level'] = 0
        return "💦 ТЫ КОНЧИЛ! Офигенно! Давай еще?"
    
    return arousal_levels[user_arousal[chat_id]['level']]

# ==================== ОСНОВНЫЕ ФУНКЦИИ ====================
def get_keywords(text):
    """Извлекает ключевые слова из текста"""
    text = text.lower()
    words = re.findall(r'\b[а-яё]+\b', text)
    return words

def get_response(chat_id, message_text):
    """Получает ответ на основе выбранного персонажа"""
    character = user_character.get(chat_id, 'girl')
    
    # Выбираем словарь
    if character == 'girl':
        responses_dict = girl_responses
        fallback = girl_fallback
    elif character == 'boy':
        responses_dict = boy_responses
        fallback = boy_fallback
    elif character == 'gay':
        responses_dict = gay_responses
        fallback = gay_fallback
    elif character == 'lesbian':
        responses_dict = lesbian_responses
        fallback = lesbian_fallback
    else:
        responses_dict = girl_responses
        fallback = girl_fallback
    
    words = get_keywords(message_text)
    
    # Проверяем слова
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
        "🎮 *Режимы:*\n"
        "1️⃣ Виртуальный секс (4 персонажа)\n"
        "2️⃣ ОНЛАЙН ЧАТ (анонимный)\n\n"
        "*Команды:*\n"
        "/sex - Выбрать для виртуального секса\n"
        "/chat - Войти в онлайн чат\n"
        "/stop - Выйти отовсюду\n"
        "/help - Помощь"
    )
    
    markup = InlineKeyboardMarkup()
    btn_sex = InlineKeyboardButton("🎮 Виртуальный секс", callback_data="mode_sex")
    btn_chat = InlineKeyboardButton("💬 Онлайн чат", callback_data="mode_chat")
    markup.add(btn_sex, btn_chat)
    
    bot.send_message(chat_id, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    
    # ===== ВЫБОР РЕЖИМА =====
    if call.data == "mode_sex":
        markup = InlineKeyboardMarkup()
        btn_girl = InlineKeyboardButton("💋 Девушка", callback_data="char_girl")
        btn_boy = InlineKeyboardButton("🍆 Парень", callback_data="char_boy")
        btn_gay = InlineKeyboardButton("🏳️‍🌈 Гей", callback_data="char_gay")
        btn_les = InlineKeyboardButton("👩‍❤️‍👩 Лесбиянка", callback_data="char_lesbian")
        btn_back = InlineKeyboardButton("🔙 Назад", callback_data="back_to_start")
        markup.add(btn_girl, btn_boy)
        markup.add(btn_gay, btn_les)
        markup.add(btn_back)
        
        bot.edit_message_text(
            "🎮 *Выбери персонажа для виртуального секса:*",
            chat_id,
            message_id,
            parse_mode="Markdown",
            reply_markup=markup
        )
    
    elif call.data == "mode_chat":
        show_chat_rooms(chat_id, message_id)
    
    elif call.data == "back_to_start":
        start(call.message)
    
    # ===== ВЫБОР ПЕРСОНАЖА =====
    elif call.data in ["char_girl", "char_boy", "char_gay", "char_lesbian"]:
        if call.data == "char_girl":
            user_character[chat_id] = 'girl'
            text = "✅ Ты выбрал *Девушку*\n💋 Развратная, готовая на всё\n\n/sex - начать виртуальный секс\n/chat - в чат"
        elif call.data == "char_boy":
            user_character[chat_id] = 'boy'
            text = "✅ Ты выбрал *Парня*\n🍆 Грубый, пошлый, готовый трахать\n\n/sex - начать виртуальный секс\n/chat - в чат"
        elif call.data == "char_gay":
            user_character[chat_id] = 'gay'
            text = "✅ Ты выбрал *Гей*\n🏳️‍🌈 Горячий, готовый на всё с парнями\n\n/sex - начать виртуальный секс\n/chat - в чат"
        elif call.data == "char_lesbian":
            user_character[chat_id] = 'lesbian'
            text = "✅ Ты выбрала *Лесбиянку*\n👩‍❤️‍👩 Нежная, страстная, любит девушек\n\n/sex - начать виртуальный секс\n/chat - в чат"
        
        bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown")
    
    # ===== ВЫБОР КОМНАТЫ ЧАТА =====
    elif call.data.startswith("room_"):
        room = call.data.replace("room_", "")
        username = call.from_user.username or f"User_{chat_id % 10000}"
        
        if add_to_chat(chat_id, username, room):
            room_name = CHAT_ROOMS[room]
            text = f"✅ Ты вошел в *{room_name}*\n\n👥 В чате: {len(chat_users[room])} чел.\n\nПиши сообщения, отправляй фото/видео!\n/leave - выйти из чата"
            
            bot.edit_message_text(text, chat_id, message_id, parse_mode="Markdown")
            
            # Показываем последние сообщения
            show_recent_messages(chat_id, room)
    
    elif call.data == "chat_back":
        show_chat_rooms(chat_id, message_id)

def show_chat_rooms(chat_id, message_id):
    """Показывает комнаты чата"""
    markup = InlineKeyboardMarkup()
    
    for room_id, room_name in CHAT_ROOMS.items():
        count = len(chat_users[room_id])
        btn = InlineKeyboardButton(
            f"{room_name} (👥 {count})", 
            callback_data=f"room_{room_id}"
        )
        markup.add(btn)
    
    btn_back = InlineKeyboardButton("🔙 Назад", callback_data="back_to_start")
    markup.add(btn_back)
    
    bot.edit_message_text(
        "💬 *Выбери комнату для анонимного чата:*\n\n"
        "• Можно писать текст\n"
        "• Отправлять фото/видео\n"
        "• Голосовые сообщения\n"
        "• Полная анонимность",
        chat_id,
        message_id,
        parse_mode="Markdown",
        reply_markup=markup
    )

def show_recent_messages(chat_id, room):
    """Показывает последние сообщения в чате"""
    history = chat_history[room][-10:]  # Последние 10
    if history:
        bot.send_message(chat_id, "📜 *Последние сообщения:*", parse_mode="Markdown")
        for msg in history[-5:]:  # Показываем только 5 последних
            if msg['type'] == 'system':
                bot.send_message(chat_id, f"⚙️ [{msg['time']}] {msg['text']}")
            elif msg['type'] == 'text':
                gender_emoji = '👨' if msg['gender'] == 'male' else '👩' if msg['gender'] == 'female' else '👤'
                bot.send_message(chat_id, f"{gender_emoji} [{msg['time']}] {msg['user']}: {msg['text']}")

@bot.message_handler(commands=['sex'])
def sex_command(message):
    chat_id = message.chat.id
    
    if chat_id not in user_character:
        bot.send_message(chat_id, "❌ Сначала выбери персонажа!\n/start → Виртуальный секс")
        return
    
    character = user_character[chat_id]
    names = {'girl': 'Девушка', 'boy': 'Парень', 'gay': 'Гей', 'lesbian': 'Лесбиянка'}
    
    sex_text = (
        f"🔥 *Виртуальный секс с {names[character]}* 🔥\n\n"
        "Пиши действия:\n"
    )
    
    if character in ['girl', 'lesbian']:
        sex_text += "• киска, клитор, палец, язык, сосать, кончить\n"
    else:
        sex_text += "• член, попа, палец, язык, рак, сосать, кончить\n"
    
    sex_text += "\nЧем больше пишешь - тем выше возбуждение!\n/arousal - проверить уровень"
    
    user_arousal[chat_id] = {'level': 0, 'actions': []}
    bot.send_message(chat_id, sex_text, parse_mode="Markdown")

@bot.message_handler(commands=['chat'])
def chat_command(message):
    chat_id = message.chat.id
    
    if chat_id not in user_character:
        bot.send_message(chat_id, "❌ Сначала выбери персонажа!\n/start → Выбрать персонажа")
        return
    
    show_chat_rooms(chat_id, None)

@bot.message_handler(commands=['leave'])
def leave_chat(message):
    chat_id = message.chat.id
    
    room = remove_from_chat(chat_id)
    if room:
        bot.send_message(chat_id, "✅ Ты вышел из чата.\n/chat - войти снова")
    else:
        bot.send_message(chat_id, "❌ Ты не в чате.")

@bot.message_handler(commands=['arousal'])
def arousal_command(message):
    chat_id = message.chat.id
    
    if chat_id not in user_arousal:
        bot.send_message(chat_id, "❌ Нет активного секса. Напиши /sex")
        return
    
    level = user_arousal[chat_id]['level']
    arousal_levels = ["😈", "🔥", "💦", "🌊", "💥"]
    level_text = [
        "только начинаешь",
        "уже горячо",
        "весь мокрый",
        "на грани",
        "КОНЧАЕШЬ"
    ]
    
    current_level = min(level, 4)
    bot.send_message(
        chat_id,
        f"📊 *Уровень возбуждения:* {level}/5\n{arousal_levels[current_level]} {level_text[current_level]}"
    )

@bot.message_handler(commands=['stop'])
def stop_dialog(message):
    chat_id = message.chat.id
    
    # Удаляем из чата если был
    remove_from_chat(chat_id)
    
    # Очищаем данные
    if chat_id in user_character:
        del user_character[chat_id]
    if chat_id in user_arousal:
        del user_arousal[chat_id]
    
    bot.send_message(
        chat_id,
        "⏸️ *Диалог остановлен*\nЧтобы начать заново, напиши /start",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "🔞 *ПОМОЩЬ*\n\n"
        "*Основные команды:*\n"
        "/start - Главное меню\n"
        "/sex - Виртуальный секс\n"
        "/chat - Онлайн чат\n"
        "/leave - Выйти из чата\n"
        "/arousal - Уровень возбуждения\n"
        "/stop - Выйти отовсюду\n\n"
        "*В чате можно:*\n"
        "• Писать текст\n"
        "• Отправлять фото\n"
        "• Отправлять видео\n"
        "• Голосовые сообщения\n\n"
        "*Секс-команды:*\n"
        "Для девушек: киска, клитор, палец, язык, сосать, кончить\n"
        "Для парней: член, попа, палец, язык, рак, сосать, кончить\n"
        "Для геев: член, попа, сосать, кончить\n"
        "Для лесбиянок: киска, клитор, палец, язык, кончить"
    )
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

# ==================== ОБРАБОТКА СООБЩЕНИЙ ====================
@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    
    # Проверяем, в чате ли пользователь
    for room, users in chat_users.items():
        if chat_id in users:
            # Отправляем сообщение в комнату
            broadcast_to_room(room, chat_id, message.text)
            return
    
    # Если не в чате - виртуальный секс
    if chat_id in user_character:
        if message.text.lower() in ['стоп', 'хватит', 'stop']:
            stop_dialog(message)
            return
        
        response = get_response(chat_id, message.text)
        emojis = {'girl': '💋', 'boy': '🍆', 'gay': '🏳️‍🌈', 'lesbian': '👩‍❤️‍👩'}
        emoji = emojis.get(user_character[chat_id], '💋')
        bot.send_message(chat_id, f"{emoji} {response}")
        
        # Обновляем возбуждение если есть секс-слова
        words = get_keywords(message.text)
        sex_words = ['член', 'киска', 'клитор', 'попа', 'сосать', 'кончить', 'палец', 'язык', 'рак']
        if any(word in sex_words for word in words):
            arousal_msg = update_arousal(chat_id)
            bot.send_message(chat_id, f"🔥 {arousal_msg}")
    else:
        bot.send_message(chat_id, "❌ Напиши /start для начала")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    chat_id = message.chat.id
    
    for room, users in chat_users.items():
        if chat_id in users:
            file_id = message.photo[-1].file_id
            broadcast_to_room(room, chat_id, None, 'photo', file_id)
            return
    
    bot.send_message(chat_id, "❌ Ты не в чате. /chat чтобы войти")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    chat_id = message.chat.id
    
    for room, users in chat_users.items():
        if chat_id in users:
            file_id = message.video.file_id
            broadcast_to_room(room, chat_id, None, 'video', file_id)
            return
    
    bot.send_message(chat_id, "❌ Ты не в чате. /chat чтобы войти")

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    chat_id = message.chat.id
    
    for room, users in chat_users.items():
        if chat_id in users:
            file_id = message.voice.file_id
            broadcast_to_room(room, chat_id, None, 'voice', file_id)
            return
    
    bot.send_message(chat_id, "❌ Ты не в чате. /chat чтобы войти")

# ==================== ЗАПУСК ====================
if __name__ == "__main__":
    print("=" * 60)
    print("🔥 Бот ЗАПУЩЕН с МЕГА ЧАТОМ!")
    print("📝 Токен: 8442213004:AAFgM1lchfhZmh5SxzrumH9nCR2TQzvCEos")
    print("👥 Персонажи: Девушка 💋 | Парень 🍆 | Гей 🏳️‍🌈 | Лесби 👩‍❤️‍👩")
    print("💬 Комнаты: Гей | Лесби | Смешанный | Общий")
    print("🎮 Функции: Секс | Чат | Фото | Видео | Голосовые")
    print("🛑 Нажми Ctrl+C для остановки")
    print("=" * 60)
    
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        print("\n❌ Бот остановлен")
