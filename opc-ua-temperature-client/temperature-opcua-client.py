from opcua import Client
import time
import pymongo

url = "opc.tcp://127.0.0.1:4840"

client = Client(url)

client.connect()
print("Client Connected")

# mongodb connection
mongo_client = pymongo.MongoClient("mongodb://admin:IoTadmin!@101.200.42.133:27017/")

# db
db = mongo_client["opc"]

# collection
col_temperature = db['temperature']

while True:
    node_temp = client.get_node("ns=2;i=2")
    node_pressure = client.get_node("ns=2;i=3")
    node_time = client.get_node("ns=2;i=4")

    Temperature = node_temp.get_value()
    Pressure =  node_pressure.get_value()
    Time =  node_time.get_value()

    print(Temperature,Pressure,Time)
    time.sleep(1)
            
    values ={'timestamp':Time,
    'temperature':Temperature,
    'pressure':Pressure
    }

    # insert
    col_temperature.insert_one(values)