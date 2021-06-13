# Python OPCua

## 关于OPC UA

OPC UA是一种协议 
https://opcfoundation.org/

被”誉为”是工业4.0的基础，现在工业通信的基础

一些参考信息

https://www.novotek.com/uk/solutions/kepware-communication-platform/opc-and-opc-ua-explained/
https://www.paessler.com/it-explained/opc-ua
https://blog.csdn.net/yaojiawan/article/details/88990351
https://www.zhihu.com/question/57073931

OPC UA Compare with MQTT
https://www.zhihu.com/question/57073931


---

## Python Installation

pip install opcua

---

## 连接到OPC UA服务器

本地服务器
-> uadiscover

某个特定地址服务器，比如
-> uadiscover -u opc.tcp://10.122.000.66:4840 

### 如果没有的话可以先建立一个本地服务器


```

from opcua import Server

if __name__=='__main__':
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:48400/")

    server.start()    
```

可以看到
```
Endpoints other than open requested but private key and certificate are not set.
Listening on 0.0.0.0:48400
```


Try 

```
uadiscover -u 0.0.0.0:48400


Server 1:
  Application URI: urn:freeopcua:python:server
  Product URI: urn:freeopcua.github.io:python:server
  Application Name: FreeOpcUa Python Server
  Application Type: ApplicationType.ClientAndServer
  Discovery URL: opc.tcp://0.0.0.0:48400/

Endpoint 1:
  Endpoint URL: opc.tcp://127.0.0.1:48400/
  Application URI: urn:freeopcua:python:server
  Product URI: urn:freeopcua.github.io:python:server
  Application Name: FreeOpcUa Python Server
  Application Type: ApplicationType.ClientAndServer
  Discovery URL: opc.tcp://0.0.0.0:48400/
  Server Certificate: [no certificate]

```
