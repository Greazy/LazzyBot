from threading import Thread
import time
import messagesbot
import datetime


from telebot import types
import telebot
import schedule
import sqlite3 as sql
from config import *


def saving_chat_id_from_users(chat_id_for_saving):
	with con:
		cur = con.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS `chat_id` (id INTEGER UNIQUE)")
		try:
			cur.execute(f"INSERT INTO 'chat_id' VALUES ('{chat_id_for_saving}')")
			con.commit()
		except:
			pass

def deleting_chat_id_from_user(chat_id_for_deleting):
	with con:
		cur = con.cursor()
		cur.execute(f"DELETE FROM 'chat_id' where id={chat_id_for_deleting}")
		con.commit()

@bot.message_handler(commands=['start'])
def welcome_message(message):
	bot.send_message(message.chat.id, messagesbot.start_message())
	saving_chat_id_from_users(message.chat.id)
	

def schedule_to_subs(sign = None):
	with con:
		cur = con.cursor()
		cur.execute("SELECT * FROM 'chat_id'")
		rows = cur.fetchall()
		if sign == "water":
			if now.hour < 23 and now.hour > 7:
				for row in rows:
					for chat_id in row:
						try:
							bot.send_message(chat_id=chat_id,text=messagesbot.schedule_to_drink_water())
						except:
							deleting_chat_id_from_user(chat_id)
			else:
				pass
		elif sign == "training":
			if now.hour < 20 and now.hour > 10:
				for row in rows:
					for chat_id in row:
						try:
							bot.send_message(chat_id=chat_id,text=messagesbot.schedule_to_easy_training())
						except:
							deleting_chat_id_from_user(chat_id)
		else:
			pass

@bot.message_handler(commands=['training'])
def training_func(message):
	markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
	but1 = types.KeyboardButton('hard')
	but2 = types.KeyboardButton('easy')
	markup.add(but1,but2)
	bot.send_message(message.chat.id, "Обери режим :", reply_markup=markup)


schedule.every(0.1).minutes.do(schedule_to_subs, "water")
schedule.every(0.1).minutes.do(schedule_to_subs, "training")

def schedule_loop():
	#Цикл для роботи нагадувань
	while True:
		schedule.run_pending()

def botpolling():
	# Цикл для роботи бота, якщо зловить ексепшн, виведе його і через 15с попробує ще раз.
	while True:
		try:
			bot.polling(none_stop=True)
		except Exception as e:
			print(e)
			time.sleep(15)



if __name__ == '__main__':

	thread1 = Thread(target=schedule_loop)
	thread2 = Thread(target=botpolling)
	thread1.start()
	thread2.start()
