#NAME    : MOHNISH AGRAWAL
#SECTION : A
#ROLL NO : 2018053
#GROUP NO: 5

import urllib.request 
import datetime 
import sys

# function to get weather response
def weather_response(location, API_key):
	''' It returns the json data as a string, to be used further ahead.

	Parameter location: The city name
	Parameter API_key: Valid key

	We open the url using usllib.request module and read it. It gets stored as bytes, from which
	it is decoded and converted into a string and returned. '''
	x="http://api.openweathermap.org/data/2.5/forecast?q="+location+"&APPID="+API_key
	y=urllib.request.urlopen(x,timeout=600).read()
	return y.decode("utf-8")
	
# function to check for valid response 
def has_error(location,json):
	'''This function checks whether the location the user has entered and the city name that we get
	from the json data is same or not.'''
	real_location=json[json.find('name')+7:json.find(',',json.find('name'))-1]
	
	if location.lower()==real_location.lower():
		return False
	else:
		return True

#A generalised function that returns modified substring according to the data given
def parsed_string_json(json,n=0,t="21:00:00"):
	#cur_datetime=(datetime.datetime.now()+datetime.timedelta(days=n)).strftime("%Y-%m-%d %H:%M:%S")
	'''
	We first get the current datetime string from json string returned from the weather response,
	which is then converted into date time format, and n(day from the current day) is added to it using 
	deltatime method. Then it is again converted to string format.

	We get the substring from json string that lies between the current datetime and datetime 3 hours 
	before the current datetime
	'''
	cur_datetime=(datetime.datetime.strptime(json[json.find("dt_txt")+9:json.find("}",json.find("dt_txt"))-1],"%Y-%m-%d %H:%M:%S")+datetime.timedelta(days=n)).strftime("%Y-%m-%d")
	if(int(t[0:2])<15):
		date_time1=cur_datetime[0:11]+" 0"+str(int(t[0:2])-3)+":00:00"
	else:
		date_time1=cur_datetime[0:11]+" "+str(int(t[0:2])-3)+":00:00"

	date_time2=cur_datetime[0:11]+" "+t

	z=json[0:json.find(date_time2)]	
	if date_time1 in z:
		return(json[json.find(date_time1):json.find(date_time2)])
	else:
		return(json[0:json.find(date_time2)])

#function to get the temperature of a city at particular datetime
def get_temperature (json, n=0,t="21:00:00"):
	parsed_json=parsed_string_json(json,n,t)
	
	if 'temp' in parsed_json:
		return float(parsed_json[parsed_json.find('temp')+6:parsed_json.find('temp')+(parsed_json.find(',',parsed_json.find('temp'))-parsed_json.find('temp'))])

#function to get the humidity of a city at particular datetime
def get_humidity(json, n=0,t="21:00:00"):
	parsed_json=parsed_string_json(json,n,t)
	if 'humidity' in parsed_json:
		return int(parsed_json[parsed_json.find('humidity')+10:parsed_json.find('humidity')+(parsed_json.find(',',parsed_json.find('humidity'))-parsed_json.find('humidity'))])


#function to get the pressure of a city at particular datetime
def get_pressure(json, n=0, t="21:00:00"):
	parsed_json=parsed_string_json(json,n,t)
	
	if 'pressure' in parsed_json:
		return float(parsed_json[parsed_json.find('pressure')+10:parsed_json.find('pressure')+(parsed_json.find(',',parsed_json.find('pressure'))-parsed_json.find('pressure'))])

#function to get the wind speed of a city at particular datetime
def get_wind(json, n=0,t="21:00:00"):
	parsed_json=parsed_string_json(json,n,t)

	if 'speed' in parsed_json:
		return float(parsed_json[parsed_json.find('speed')+7:parsed_json.find('speed')+(parsed_json.find(',',parsed_json.find('speed'))-parsed_json.find('speed'))])

#function to get the sea level of a city at particular datetime
def get_sealevel(json, n=0,t="21:00:00"):
	parsed_json=parsed_string_json(json,n,t)

	if 'sea_level' in parsed_json:
		return float(parsed_json[parsed_json.find('sea_level')+11:parsed_json.find('sea_level')+(parsed_json.find(',',parsed_json.find('sea_level'))-parsed_json.find('sea_level'))])
	

location = input()
API_key = "2ab136be1543b5789451a5994364c0d3"
try:
	data = weather_response(location,API_key)
except:
	print("location not found")
	sys.exit()
current_time = datetime.datetime.now().strftime("%H:%M:%S")

time = ["00:00:00","03:00:00","06:00:00","09:00:00","12:00:00","15:00:00","18:00:00","21:00:00"]
try:
	if not(has_error(location,data)):
		for i in range(5):
			print("\nDay",i,"\n")
			for x in time:
				print("\ttime",x,":")
				print("\tTemperature:",get_temperature(data,i,x),"\n\tHumidity:",get_humidity(data,i,x),"\n\tPressure:",get_pressure(data,i,x),"\n\tWind:",get_wind(data,i,x),"\n\tSea Level:",get_sealevel(data,i,x))
				print()
except:
	print("Error")