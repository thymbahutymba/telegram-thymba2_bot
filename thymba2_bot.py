#!/usr/bin/python

import telebot
import threading
import json
import os
import logging
import sys
from Measurements import *
from logging.handlers import RotatingFileHandler

###################################################
##################### LOGGING #####################
###################################################
logger = telebot.logger
logger.removeHandler(logger.handlers[0])

LOG_FILENAME = "thymbahutymba_bot.log"
LOG_FORMAT = '[%(asctime)s] %(levelname)s: "%(message)s"'
DATE_FMT = "%Y-%m-%d %H:%M:%S"

if not os.path.exists("logs"):
	os.mkdir("logs")

fh = RotatingFileHandler("logs/"+LOG_FILENAME, maxBytes=104857600, backupCount=7)
formatter = logging.Formatter(LOG_FORMAT, DATE_FMT)
fh.setFormatter(formatter)
logger.addHandler(fh)

logger.setLevel(logging.INFO)

###################################################

if not os.path.exists("/tmp/thymba2_bot"):
	os.mkdir("/tmp/thymba2_bot")

create_image = "./create.gnuplot"
image = "/tmp/thymba2_bot/temperature"
f_meas = "/tmp/thymba2_bot/measurements.dat"
BOT_RESTART = 30

try:
	with open('config.json') as config:
		cfg = json.load(config)
		token = cfg.get('token')
		user = cfg.get('user')
except Exception as e:
	logger.error(str(e))
	sys.exit(0)

bot = telebot.TeleBot(token)
information = Measurements()

semaphore = threading.Semaphore(value=1)
threading.Thread(target=information.take_info, args=(semaphore,)).start()

def are_you(username):
	if username == user:
		return True
	return False

@bot.message_handler(regexp="^ping$")
def on_ping(message):
	if are_you(message.from_user.username):
		bot.reply_to(message, "pong")

@bot.message_handler(commands=['graph'])
def on_graph(message):
	if not are_you(message.from_user.username):
		return
	
	with semaphore:
		with open(f_meas, 'w') as data:
			how_much = len(information.data['times'])
			data.write("# File generated on {}\n# Date\tTemperature\n".format(datetime.now()))

			for i, t in enumerate(information.data['times']):
				append = "\"{}\"".format(t)
				for ind_f in range(0, len(information.data['files'])):
					append += "\t{}".format(information.data['values'][ind_f][i])

				append += "\n"
				data.write(append)

	os.system(create_image)
	bot.send_photo(message.chat.id, open(image, "rb"))

while True:
	try:
		#bot = telebot.TeleBot(token)
		bot.polling()
	except Exception as e:
		logger.error("Bot polling failed, restarting in {}sec. Error: {}".format(BOT_RESTART,str(e)))
		bot.stop_polling()
		sleep(BOT_RESTART)
		bot = telebot.TeleBot(token)
		#sys.exit(15)

# vim: set ts=4 sw=4 tw=120 noet :
