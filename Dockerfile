
FROM ubuntu:18.04
MAINTAINER hyunhankyul@gmail.com

RUN apt-get update && \
    apt-get install -y python3-pip && \
    apt-get install -y python3-dev && \
    apt-get install -y libsm6 && \
    apt-get install -y libxext6 && \
    apt-get install -y libfontconfig1 && \
    apt-get install -y libxrender1 && \
    apt-get install -y build-essential

WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt
RUN pip3 install opencv-python

EXPOSE 5000

ENTRYPOINT [ "python3" ]
CMD ["cc.py"]
