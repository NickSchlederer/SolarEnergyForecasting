import csv
import os, json, requests

def readCsvFile(filename):
  #module reads the CSV file and returns a list of all data
  Data = []
  with open(filename, mode='r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
      Data.append(row)

  return Data

# Function gets 5 year average on solar radiation data for any pair of coords
# return average (MJ/m²/month) !!!!

def GetSolarData(Latitude,Longitude):
  base_url = r"https://power.larc.nasa.gov/api/temporal/monthly/point?parameters=ALLSKY_SFC_SW_DWN&community=SB&longitude={longitude}&latitude={latitude}&start=2017&end=2022&format=JSON"

  api_request_url = base_url.format(longitude=Longitude, latitude=Latitude)
  response = requests.get(url=api_request_url, verify=True, timeout=30.00)
  if response.status_code == 200:
    print("Loading data....")
  else:
    return 0

  data = json.loads(response.content.decode('utf-8'))

  SolarRadTotal = 0
  Months = 0

  path = data['properties']['parameter']['ALLSKY_SFC_SW_DWN']
  for element in path:
    #solar radiation per month
    SolarRadTotal += path[element]
    Months +=1


  AVG = SolarRadTotal / Months
  print(SolarRadTotal, Months, AVG)
  return AVG


Data = readCsvFile("Temp_test.csv")

x=1
y=2
for i in range(len(Data)):
  Average = GetSolarData(Data[i][x],Data[i][y])
  Data[i].append(Average)
  print(Data[i])
  with open("TempSolar5YearAVG_short", 'a', newline='') as output:
    csv_write = csv.writer(output)
    csv_write.writerow(Data[i])



#file_name = "TempSolar5YearAVG_short.csv"

#with open(file_name, 'w', newline='') as csvfile:
#    csv_writer = csv.writer(csvfile)
#    for row in Data:
#        csv_writer.writerow(row)