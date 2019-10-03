# DeployToPi:
Python script to check and deploy your code onto a raspberry pi (can work on any computer with python installed).

#### Set-up:
Make sure you clone to your raspberry pi(or other computer) 

`git clone https://github.com/smartsnake/DeployToPi.git`

#### Requirments:

`pip3 install -r requirments.txt`

#### Running:

`python3 main.py`

## TODO:
* Improve the README.md
* Change the method of checking the latest commit to a web-hook method.
* Add support for checking more than one repo.
* Change how the program starts the docker image, so it can run on a new process.

## Built With
[Docker](https://github.com/docker/docker-py) - Used to build and run docker images.

[gitpython](https://github.com/gitpython-developers/GitPython) - Used to get and check git repo's
