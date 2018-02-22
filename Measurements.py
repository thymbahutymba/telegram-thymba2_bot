import time as t
import threading
import json
from datetime import datetime

"""
Limit measurements to 6 hours and 15 minutes. 
1 measurement every 30s -> 120 measurements for hours
Limit measurements to 750
"""

class Measurements():

	data = {
		'files':[],
		'times': [],
		'values': []
	}

	tt_sleep = 30
	m_limit = 750

	def __init__(self):
		with open("config.json") as config:
			files = json.load(config).get('files')

		for f in files:
			self.data['files'].append(f)
			self.data['values'].append([])

	def take_info(self, semaphore):
		while True:
			time = datetime.now()
			for index in range(0, len(self.data['files'])):
				with open(self.data['files'][index], "r") as f:
					temp = int(f.readline()[:-1])/1000
				with semaphore:
					self.data['values'][index].append(temp)

			with semaphore:
				self.data['times'].append(time)

			if len(self.data['times']) == self.m_limit:
				with semaphore:
					self.data['times'].pop(0)
					for i in range(0, len(self.data['values'])):
						self.data['values'][i].pop(0)

			t.sleep(tt_sleep)
