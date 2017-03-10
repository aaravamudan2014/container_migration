FROM ubuntu:latest
MAINTAINER Akshay Aravamudan <aaravamudan2014@my.fit.edu>
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential libglib2.0-0 libav-tools
COPY /web /web
WORKDIR /web
RUN pip install flask
RUN pip install numpy opencv-python scipy imutils sk-video 
RUN pip install scikit-video
ENTRYPOINT ["python"]
CMD ["app.py"]
