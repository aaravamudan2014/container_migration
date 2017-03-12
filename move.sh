cd /tmp && sudo rm -r checkpoint*
sudo docker stop pg2
sudo docker rm pg1
sudo docker run -p 8000:8000 --name pg1 thread_build &
echo"\n\n web server built and running"
sleep 2s
read -p "Press any key to checkpoint image and continue in another container..." -n1 -s


sudo docker checkpoint create --leave-running --checkpoint-dir=/tmp pg1 checkpoint_new
echo "\n\ncheckpoint created"
echo "\n\n main container stopped... starting new container"
sleep 0.5
sudo docker stop pg1
sudo docker start --checkpoint-dir=/tmp --checkpoint=checkpoint_new pg2 &
firefox --new-window http://127.0.0.1:8000/
echo "\n\n clone started"
