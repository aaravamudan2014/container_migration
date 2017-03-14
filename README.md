# Container Migration
This project is designed to showcase the new experimental feature added to docker, container migration.

## Container description:
The container is hosting a web server and hosts a continuous stream of jpeg images to the web page. All this while an image processing thread runs in the background. It runs in the background to show the capability of doker checkpoints to save the state of a program (even in something as memory intensive as multithreaded image processing).

## Migration: 
The shell script is designed to start a new container based on the given dockerfile, stops and checkpoints it after a few seconds and creates another container (that was created based on the same dockerfile) conitnuing EXACTLY where the previous container left off.

### Procedure:
1. clone this repository onto a local folder
2. build the image from the dockerfile using the following command: bash sudo docker build -t thread_build 
3. run a docker image to be cloned into (required for move.sh file) using : sudo docker run -p 8000:8000 --name pg2 thread_build
4. stop the container since we need to clone into it later: sudo docker stop pg2
5. change permissions on given move.sh file (since docker runs containers as sudo user): sudo chmod 775
6. run the move.sh file using : ./move.sh

The new container will start and the shell script will automatically open firefox with the webpage streaming images.
