from git import Repo
import os, shutil
import docker
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

        build = subprocess.Popen(['docker', 'build', '-t', f'{DockerImageName}', f'{WorkingDir}/'], 
                        stdout=subprocess.PIPE)
        program = subprocess.Popen(['docker', 'run', f'{DockerImageName}'], 
                        stdout=subprocess.PIPE)

        if debug:
            print(build.stdout)
            print(program.stdout)
        if build.stderr != None or program.stderr != None:
            print('There was a problem...')
            print(f'ERROR: {build.stderr}')
            print(f'STDOUT: {program.stderr}')

        print(f'{DockerImageName} is deployed.')
        print('Checking for new commits...')


