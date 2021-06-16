"""
An example of opcua server sending

"""
from opcua import Server
from random import randint
import datetime
import time
from time import sleep

from opcua import Server

server = Server()

url = "opc.tcp://127.0.0.1:4840"
server.set_endpoint(url)

name = "OPC_SIMULATION_SERVER"
addspace = server.register_namespace(name)

node = server.get_objects_node()

Param = node.add_object(addspace, "Parameters")

Temp = Param.add_variable(addspace, "Temperature", 0)
Press = Param.add_variable(addspace, "Pressure", 0)
Time = Param.add_variable(addspace, "Time", 0)

Temp.set_writable()
Press.set_writable()
Time.set_writable()


if __name__ == '__main__':

    server.start()
    print("Server started at {}".format(url))

    while True:
        
        temperature = randint(-10,50)
        pressure = 1000 + randint(0, 100)
        time = datetime.datetime.now()

        print(temperature, pressure, time)

        Temp.set_value(temperature)
        Press.set_value(pressure)
        Time.set_value(time)

        sleep(1)

