import subprocess


def main():
    cmd = ['python3', 'app.py']
    rsp = subprocess.Popen(cmd)
    while True:
        if rsp.poll() == None:
            pass
        else:
            break