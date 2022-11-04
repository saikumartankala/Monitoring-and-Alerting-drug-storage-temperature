import requests
import json
import time, math, statistics
from boltiot import Bolt
import conf

mybolt_device = Bolt(conf.bolt_api_key, conf.device_id)

def compute_bound(history_data,frame_size,factor): 
	if len(history_data) < frame_size: 
		return None 
	if len(history_data) > frame_size:
	 	del history_data[0: len(history_data)-frane_size]
	mn = statistics.mean(history_data)
	variance = 0
	for data in history_data:
 		variance += math.pow((data-mn),2)
	zn = factor * math.sqrt(variance / frame_size)
	high_bound = history_data[frame_size-1]+zn
	return high_bound

def get_sensor_value_from_AO_pin(pin):
	try:
		response = mybolt_device.analogRead(pin)
		data= json.loads(response)
		if data["success"] != 1:
			print("Request not successfull.\n")
			print("This is the response-->", data)
			return -999
		sensor_value = int(data["value"])
		return sensor_value
	except Exception as e:
		print ("Something went wrong while returning the sensor value.")
		print(e)		
		return -999
def send_telegram_message(message):
	url = "https://api.telegram.org/" + conf.telegram_bot_id + "/sendMessage"
	data = {"chat_id": conf.telegram_chat_id,"text": message}
	try:
		response = requests.request("POST", url, params=data)
		print("\nThis is the Telegram URL:")
		print(url)
		print("\nThis is the telegram response:")
		print (response.text)
		telegram_data = json.loads(response.text)
		return telegram_data["ok"]
	except Exception as e:
		print("An error occured in sending the alert message via Telegram")
		print(e)
		return False

history_data = []

while True:
	print("\n\n\n\n")
	sensor_value = get_sensor_value_from_A0_pin("0")
	print("\nThe current temperature is:", int(sensor_value/10.24), "degrees.")

	if sensor_value == -999:
		print("\nRequest was unsuccessfull.")
		time.sleep(10)
		continue

	if int(sensor_value/10.24) >= conf.high_threshold_value or int(sensor_value/10.24) <= conf.$
		print("\nSensor value is out of threshold")
		if int(sensor_value/10.24) >=conf.high_threshold_value:
			message = "Alert! Temperature is above" + str(conf.high_threshold_value) + $
				  ". The current temperature is " + str(int (sensor_value/10.24)) + "$
		else:
			message = "Alert! Temperature is below" + str(conf.low_threshold_value) + "$
				  ". The current temperature is " + str(int (sensor_value/10.24)) + "$
		telegram_status = send_telegram_message(message)
		print("\nTelegram status:", telegram_status)

	bound = compute_bound(history_data, conf.frame_size,conf.mul_factor)

	if bound == None:
		required_data_points = conf.frame_size - len(history_data)
		print("\nData insufficient. Need", required_data_points, "more data points to compute$
		history_data.append(sensor_value)
		time.sleep(10)
		continue
	try:
		if sensor_value> bound:
			message = "Alert! Door has been opened by some one."
			telegram_status = send_telegram_message(message)
			print("\nTelegram status:", telegram_status)
		history_data.append(sensor_value)
	except Exception as e:
		print("Error:",e)
	time.sleep(10)
