from crontab import CronTab
import argparse
import sys

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--workdir', required=False, help='Infer config params file path')
    parser.add_argument('--hardware', required=False, help='hardware x86 or jetson')
    return parser.parse_args(argv)


def main(args):
    my_cron = CronTab(user='root')
    job = my_cron.new(command='sudo python3 samples/jobs_infer.py --config /etc/permanent_cert/perm_config.ini --workdir args.workdir --hardware args.hardware', comment='infer_job_listener')
    job.every_reboot()
    my_cron.write()

if __name__=="__main__":
    main(parse_arguments(sys.argv[1:]))


