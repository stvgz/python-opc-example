FROM python:3.7-slim

LABEL auther = 'stvgz'

# pip 
RUN mkdir ~/.pip && \
    cd ~/.pip/  && \
    echo "[global] \ntrusted-host =  mirrors.aliyun.com \nindex-url = http://mirrors.aliyun.com/pypi/simple" >  pip.conf

# install
# COPY ./requirements.txt /requirements.txt
COPY . . 

RUN pip install -r /requirements.txt

EXPOSE 8081

ENTRYPOINT [ "python" , "temperature-opcua-dashboard.py"]