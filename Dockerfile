FROM ubuntu:latest
MAINTAINER Akshay Aravamudan <aaravamudan2014@my.fit.edu>
#installing python and other required dependencies
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential libglib2.0-0 libav-tools
# copying directory and changin working directory
COPY /web /web
WORKDIR /web
# python local web server framework
RUN pip install flask
#installing opencv and video/image processing tools 
RUN pip install numpy opencv-python scipy imutils sk-video 
RUN pip install scikit-video
# when container are started using this dockerfile, a webserver will be started 
ENTRYPOINT ["python"]
CMD ["app.py"]
