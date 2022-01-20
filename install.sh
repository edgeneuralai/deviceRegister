pip3 install --target=/usr/local/lib/python3.6/dist-packages awsiotsdk-1.0.0.dev0-py3-none-any.whl
pip3 install --target=/usr/local/lib/python3.6/dist-packages psutil boto3
docker pull edgeneural/enapregister:$2
docker run -it -v /etc/:/tmp/ edgeneural/enapregister:$2 $1
git clone https://github.com/rohitkatakolen/awsiotsdk.git /home/awsiotsdk
sudo python3 /home/awsiotsdk/cron_start.py --workdir $1 --hardware $2

