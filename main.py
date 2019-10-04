from git import Repo
import os, shutil
#import docker
import subprocess

DIR_NAME = "Test"

#Change this to whatever docker repo on github
REMOTE_URL = 'https://github.com/smartsnake/DeploymentTest.git'
latestCommitFile = 'latest.commit'
WorkingDir = 'Deploy'
DockerImageName = 'program'

debug = True

if os.path.isdir(DIR_NAME):
    shutil.rmtree(DIR_NAME)
os.mkdir(DIR_NAME)

latestCommit = None

if os.path.exists(latestCommitFile):
    latestCommit = open(latestCommitFile, 'r').read()
else:
    repo = Repo.clone_from(REMOTE_URL, DIR_NAME)#Location of git project that needs
    latestCommit = repo.head.commit
    thing= open(latestCommitFile, 'w')
    thing.write(str(latestCommit))
    thing.close()

print(str(latestCommit))
print('Checking for new commits...')
while True:
    if os.path.isdir(DIR_NAME):
        shutil.rmtree(DIR_NAME)
    os.mkdir(DIR_NAME)
    repo = Repo.clone_from(REMOTE_URL, DIR_NAME)#Location of git project that needs
    newCommit = repo.head.commit
    if str(newCommit) != str(latestCommit):
        print('Updating Program!')
        print(f'newCommit: {newCommit}, latestCommit: {latestCommit}')
        if os.path.isdir(WorkingDir):
            shutil.rmtree(WorkingDir)
        os.mkdir(WorkingDir)
        Repo.clone_from(REMOTE_URL, WorkingDir)
        thing= open(latestCommitFile, 'w')
        thing.write(str(newCommit))
        thing.close()
        latestCommit = repo.head.commit

        if debug:
            print('Deleting old container')
        deletingContainer = subprocess.call(['docker', 'rm', '-f', f'{DockerImageName}'])

        if debug:
            print('Building image...')
        build = subprocess.call(['docker', 'build', '-t', f'{DockerImageName}', f'{WorkingDir}/'])
        
        if debug:
            print('Running image...')
        program = subprocess.call(['docker', 'run', f'--name={DockerImageName}', f'{DockerImageName}'])

        logs = subprocess.Popen(['docker', 'logs', '-f', f'{DockerImageName}'],
                        stdout=subprocess.PIPE)

        print(f'{DockerImageName} is deployed.')
        print('Checking for new commits...')


