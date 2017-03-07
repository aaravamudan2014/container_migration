FROM ubuntu:latest
MAINTAINER Akshay Aravamudan <aaravamudan2014@my.fit.edu>
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential libglib2.0-0 libav-tools
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install opencv-python scipy imutils scikit-image
ENTRYPOINT ["python"]
CMD ["app.py"]
