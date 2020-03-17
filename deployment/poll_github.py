import subprocess
import time, sched
from datetime import datetime


class UpdateServer():
    '''Due to server permissions,Engine couldn't schedule a cronjob to update the server on a schedule.
    We can use python though to execute commands which is used to execute a simple script.
    '''

    def check_github(sc):
        '''
        Runs the script to pull from master and updates server.

        Args:
            sc(sched):Scheduler registers and runs the given function.
        Returns:
            None: Scripts runs until terminated.
        '''
        process = subprocess.Popen(['updater.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()  # believe this is blocking
        curr_date = datetime.today().strftime('%Y-%m-%d')
        file_name = str(curr_date) + '.log'
        with open(file_name, 'w+') as f:
            f.write(stderr)
        sc.enter(43200, 3600)


if __name__ == '__main__':
    scheder = sched.scheduler(time.time, time.sleep)
    scheder.enter(43200, 3600, UpdateServer.check_github, (scheder,))
    scheder.run()
