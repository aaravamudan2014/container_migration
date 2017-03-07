FROM ubuntu:latest
MAINTAINER Akshay Aravamudan <aaravamudan2014@my.fit.edu>
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install opencv-python scipy s
ENTRYPOINT ["python"]
CMD ["app.py"]
