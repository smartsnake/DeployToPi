from git import Repo
import os, shutil
import logging
import subprocess
import threading
import json
import sys
import time

def setup(config):
    DIR_NAME = "Test"
    logging.info(f"Thread {config['DockerImageName']}    : Started thread.")
    #Change this to whatever docker repo on github
    REMOTE_URL = config['REMOTE_URL']#'https://github.com/smartsnake/DeploymentTest.git'
    latestCommitFile = config['DockerImageName'] + config['latestCommitFile']#'latest.commit'
    WorkingDir = config['WorkingDir']#'Deploy'
    DockerImageName = config['DockerImageName']#'program'
    latestCommit = config['latestCommit']#None

    debug = True

    if os.path.isdir(DIR_NAME):
        shutil.rmtree(DIR_NAME)
    os.mkdir(DIR_NAME)

    # if os.path.exists(latestCommitFile):
    #     latestCommit = open(latestCommitFile, 'r').read()
    if latestCommit == 'None':
        repo = Repo.clone_from(REMOTE_URL, DIR_NAME)#Location of git project that needs
        latestCommit = repo.head.commit
        thing = open(latestCommitFile, 'w')
        thing.write(str(latestCommit))
        thing.close()
    else:
        pass

    logging.info(f"Thread {config['DockerImageName']}    : latest commit = {str(latestCommit)}")
    logging.info(f"Thread {config['DockerImageName']}    : Checking for new commits...")

    while True:
        if os.path.isdir(DIR_NAME):
            shutil.rmtree(DIR_NAME)
        os.mkdir(DIR_NAME)
        repo = Repo.clone_from(REMOTE_URL, DIR_NAME)#Location of git project that needs
        newCommit = repo.head.commit
        if str(newCommit) != str(latestCommit):
            logging.info(f"Thread {config['DockerImageName']}    : Updating Program!")
            logging.info(f"Thread {config['DockerImageName']}    : newCommit: {newCommit}, latestCommit: {latestCommit}")
            if os.path.isdir(WorkingDir):
                shutil.rmtree(WorkingDir)
            os.mkdir(WorkingDir)
            Repo.clone_from(REMOTE_URL, WorkingDir)
            thing= open(latestCommitFile, 'w')
            thing.write(str(newCommit))
            thing.close()
            latestCommit = repo.head.commit

            if debug:
                logging.info(f"Thread {config['DockerImageName']}    : Deleting old container")
            deletingContainer = subprocess.call(['docker', 'rm', '-f', f'{DockerImageName}'])

            if debug:
                logging.info(f"Thread {config['DockerImageName']}    : Building image...")
            build = subprocess.call(['docker', 'build', '-t', f'{DockerImageName}', f'{WorkingDir}/'])
            
            if debug:
                logging.info(f"Thread {config['DockerImageName']}    : Running image...")
            program = subprocess.call(['docker', 'run', f'--name={DockerImageName}', f'{DockerImageName}'])

            logs = subprocess.Popen(['docker', 'logs', '-f', f'{DockerImageName}'],
                            stdout=subprocess.PIPE)

            logging.info(f"Thread {config['DockerImageName']}    : {DockerImageName} is deployed.")
            logging.info(f"Thread {config['DockerImageName']}    : Checking for new commits...")


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Main    : before loading config")

    with open('config.json') as json_data_file:
        config = json.load(json_data_file)

    if config == None:
        logging.info('Main    : Please create a config.json file.')
        sys.exit()
    else:
        logging.info("Main    : loaded config.")
        for thing in config:
            x = threading.Thread(target=setup, args=(thing,))

            logging.info("Main    : Starting thread.")
            x.start()