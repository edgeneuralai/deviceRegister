pip3 install --target=/usr/local/lib/python3.6/dist-packages awsiotsdk-1.0.0.dev0-py3-$1-any.whl
pip3 install --target=/usr/local/lib/python3.6/dist-packages psutil boto3
docker pull edgeneural/enapregister:$1
docker run -it -v /etc/:/tmp/ edgeneural/enapregister:$1 $2 $3 $4
#git clone https://github.com/rohitkatakolen/awsiotsdk.git /home/awsiotsdk
sudo python3 /tmp/enapjobs/cron_start.py --workdir /tmp/enapjobs/workspace/ --hardware $1

