import subprocess
import time, sched

class UpdateServer():
    '''Due to server permissions,Engine couldn't schedule a cronjob to update the server on a schedule.
    We can use python though to execute commands which is used to execute a simple script.

    '''
    def check_github(sc):
        process = subprocess.Popen(['updater.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate() #believe this is blocking
        sc.enter(86400, 3600)


if __name__ == '__main__':
    scheder = sched.scheduler(time.time(), time.sleep)
    scheder.enter(86400, 3600, UpdateServer.check_github, (scheder,))
    scheder.run()
