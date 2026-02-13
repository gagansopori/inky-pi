import subprocess

class SystemManager:
    @staticmethod
    def shutdown():
        subprocess.Popen("sleep 2 && sudo shutdown -h now", shell=True)