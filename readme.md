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


# 一个OPC UA监控的case

1. OPC UA Server 服务器
1. OPC UA Client 客户端
1. 一个数据库
1. OPC UA到数据库 
1. 展示dashboard
1. 预测模型
1. 信息发送

### OPC 服务器

cd opc-ua-temperature-server

temperature-opcua-server.py



### OPC Client

cd opc-ua-temperature-client

temperature-opcua-client.py


--- 
###  DB

使用MongoDB作为一个例子，使用docker的版本

> docker search mongodb

下载最新的版本
> docker pull mongo:latest

看一下是否拿到了
> docker ps

开始运行
> docker run -itd --name mongo -p 27017:27017 mongo

查看运行状态
> docker ps

进入并且配置一下账号密码
docker exec -it mongo mongo admin

> db.createUser({ user:'admin',pwd:'IoTadmin!',roles:[ { role:'userAdminAnyDatabase', db: 'admin'},"readWriteAnyDatabase"]});
Successfully added user: {
        "user" : "admin",
        "roles" : [
                {
                        "role" : "userAdminAnyDatabase",
                        "db" : "admin"
                },
                "readWriteAnyDatabase"
        ]
}

> db.auth('admin','IoTadmin!')
1


### Mongo DB的使用



### 模型

规则建立的模型是最常见的
建立一个规则的部分
1. 获取历史数据
1. 特征提取（optional）
1. 分析历史数据找到区分OK/NOK的规则
1. 追溯历史数据进行影响的确认
1. 应用规则

应用规则的部分
1. 提醒
1. 需要可查看
1. 可以修改


### 