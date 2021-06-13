from opcua import Server

if __name__=='__main__':
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:48400/")

    server.start()    
