if [ $1=='x86' ]
then
	python3.6 -m pip install awsiotsdk-1.0.0.dev0-py3-none-any.whl
else
	python3.6 -m pip install awsiotsdk-1.0.0.dev0-py3-jetson-any.whl
fi
python3.6 -m pip  install psutil boto3 docker

sudo docker pull edgeneural/enapregister:$1
sudo docker run -it -v /etc/:/tmp/ edgeneural/enapregister:$1 $2 $3 $4 $5
#git clone https://github.com/rohitkatakolen/awsiotsdk.git /home/awsiotsdk
#sudo python3 /tmp/enapjobs/cron_start.py --workdir /tmp/enapjobs/workspace/ --hardware $1
if [ $1=='x86' ]
then
        sudo python3.6 samples/jobs_infer.py --config /etc/permanent_cert/perm_config.ini --workdir /tmp/enapjobs/workspace/ --hardware $1
else
	sudo python3.6 samples/jobs_infer.py --config /etc/permanent_cert/perm_config.ini --workdir /tmp/enapjobs/workspace/ --hardware jetson
fi

