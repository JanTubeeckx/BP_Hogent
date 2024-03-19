
# This script will read data from a solis inverter through a wifi-stick and write time series to influxdb

# Created by Jan Tubeeckx
# https://github.com/JanTubeeckx/BP_Hogent

import requests
import time
import os
from dotenv import load_dotenv, dotenv_values
from influxdb_client_3 import InfluxDBClient3

# Loading variables from .env file
load_dotenv()

# Define url to server to get inverter data
url = os.getenv("SERVER_URL")
username = os.getenv("USERNAME")
password = os.getenv("WIFI_PASSWORD")

# Add database client for InfluxDB Cloud Serverless
client = InfluxDBClient3(token=os.getenv("ACCESS_TOKEN"),
                         host=os.getenv("DB_HOST"),
                         database=os.getenv("DB_NAME"))


def formatinverterdata(request):
    # Filter the data to get the measurements
    index = request.text.find(',')
    data = request.text[:index]
    temperature = "temperature" + "=" + str(output.split(';')[3]) + ","
    current_power = "current_power" + "=" + str(output.split(';')[4]) + ","
    day_total_power = "day_total_power" + "=" + str(output.split(';')[5])
    # Initialize measurement for InfluxDB
    dbline = "inverter_reading " + temperature + current_power + day_total_power


def main():
    while True:
        try:
            # Get data from server every 10 sec
            time.sleep(10)
            request = requests.get(url, auth = (username, password))
            dbline = formatinverterdata(request)
            # Write time serie to InfluxDB
            client.write(record=dbline)
        except KeyboardInterrupt:
            print("Stopping...")
            break
        except:
            print ("No connection...")

if __name__ == '__main__':
    main()