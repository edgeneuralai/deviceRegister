import os
from subprocess import run
import requests
from aws_utils import aws_util
import psutil
import subprocess
import signal
import yaml

def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

def kill_proc_tree(pid, including_parent=True):    
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    for child in children:
        child.kill()
    gone, still_alive = psutil.wait_procs(children, timeout=5)
    if including_parent:
        parent.kill()
        parent.wait(5)

class create_process:
    def __init__(self, workdir):
        self.WorkDir = workdir
        print("Process created")
    def create(self,cfg_file, dockerurl):
        global p 
        p = subprocess.Popen(["sudo" ,"docker" ,"run" ,"--name","infer","--runtime" ,"nvidia" ,"--rm" ,"--network" ,"host" ,"--gpus" ,"all" ,"-v" ,"{}:/input_models".format(self.WorkDir) , dockerurl, '/input_models/infer_config.yaml'] , stdout=subprocess.PIPE)
        print(p)
    
    def create_watch(self,session_id):
        global p1 
        p1 = subprocess.Popen(["sudo","python3","/tmp/watchandpush.py","--sessionid",session_id] , stdout=subprocess.PIPE)
        print(p1)

    def killjob(self):
        return
        print("killing job for: ",p)
        os.system("sudo docker stop infer")
        os.system("sudo kill -9 "+str(p1.pid))

class InferenceDocker:
    def __init__(self, workdir, hardware):
        self.WorkDir = workdir
        self.log_base_dir = "/var/log"
        self.hardware = hardware
        self.pjob = create_process(self.WorkDir)
        self.p1job = create_process(self.WorkDir)

    def download_data_from_url(self, url, save_path):
        r = requests.get(url,stream = True)
        print(save_path)
        with open (save_path, 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            downloaded = 0
            done = 0
            old_done = 0
            for chunk in r.iter_content(chunk_size=1024):
                downloaded += len(chunk)
                if chunk:
                    f.write(chunk)
                    done = int(100*downloaded/total_length)
                    if old_done!=done:
                        print("Download_Progress: "+str(done))
                    old_done = done
                    f.flush()
            print("Download Completed")

        #Unzip artifacts and remove zip file
        os.system('unzip -o ' + save_path + ' -d ' + self.WorkDir)
        os.system('rm {}'.format(save_path))

    def create_yaml_file(self, job_document, workdir):
        data = dict()
        data['modelname'] = job_document["modelname"]
        data['camera'] = job_document["config"]
        data['img-size'] = [256,256]
        data['show'] = False
        with open(r'{}'.format(os.path.join(workdir, 'infer_config.yaml')), 'w') as file:
            documents = yaml.dump(data, file)

    def start_inference_docker(self, job_document):
        print("Starting Inference docker")
        sessionid = job_document['sessionid']
        modelurl = job_document['files']['url']
        self.fileName = job_document['files']['fileName']
        self.modelname = job_document['modelname']
        self.dockerurl = job_document['dockerurl']
        self.session_id = job_document["sessionid"]
        self.vid = job_document["config"]["camera"]

        #Clearn the directory first and then download artifacts 
        os.system("rm -rf {}/*".format(self.WorkDir))
        self.download_data_from_url(modelurl, os.path.join(self.WorkDir ,'artifacts.zip'))
        aws_access_key_id=job_document['aws_access_key_id']
        aws_secret_access_key=job_document['aws_secret_access_key']
        aws_session_token=job_document['aws_session_token']

        self.create_yaml_file(job_document, self.WorkDir)

        os.system("export AWS_ACCESS_KEY_ID="+aws_access_key_id)
        os.system("export AWS_SECRET_ACCESS_KEY="+aws_secret_access_key)
        os.system("export AWS_SESSION_TOKEN="+aws_session_token)

        os.system("sudo aws ecr get-login-password --region ap-south-1 |  sudo docker login --username AWS --password-stdin 713356161935.dkr.ecr.ap-south-1.amazonaws.com")        
        self.pjob.create(self.vid, self.dockerurl)
        self.pjob.create_watch(self.session_id)
        print("Inferece Engine Started\n")
    
    def killjob(self):
        self.pjob.killjob()

