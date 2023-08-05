# Embrion

Embrion is a project aimed at isolating development environments of repositories. It creates a docker container
to jump start development. Currently environment has a Jupyterlab UI, Visual Studio Code UI and SSH access. You can also
develop using PyCharm connecting through SSH to the docker.

## Requirements

You need to have docker and docker-compose installed on your computer. 

## Limitations

This project only supports conda environment files (environment.yml) with a name. Support for requirements.txt
will be added later. For now you can list all your requirements as a pip dependency in your environment.yml file.
See https://stackoverflow.com/questions/35245401/combining-conda-environment-yml-with-pip-requirements-txt for more info.

## Installation

Go to your main project directory.

Run:
    
    pip install embrion


Then only if you do not have an environment.yml file in your directory run:

    embrion init

Then start the development server using:

    embrion up

Then open Jupyterlab UI using,

    embrion jupyter

or Visual Studio Code using,

    embrion vscode
    
## Usage   

To remove everything run:
   
    embrion down

To refresh the environment run:

    embrion refresh
    
To temporarily stop run:

    embrion stop

To start again run:

    embrion start

To restart run:
    
    embrion restart

To open jupyter notebook run:

    embrion jupyter

To open vs code run:

    embrion vscode
    
To open terminal run:

    embrion shell
    
To rebuild the image run:

    embrion build

To show base command for docker-compose run:

    embrion base

To show port mapping:

    embrion port
    
To run any docker-compose command run:

    embrion eval --arg '["..", "..", ...]'

To create an environment.yml in an empty directory run:

    embrion init
    
To create an environment.yml in an empty directory with a specific python version run:

    embrion init --version=3.X
    
To connect through ssh run:
    
    embrion port

Then take the ssh port and run:

    ssh root@localhost -p SSH_PORT (Password is embrion)

## About the scope

The directory that you run embrion is the project name for the docker-compose. That means that you can run many embrion
instances as long as the folder name that you run on is different. If the folder names are the same, then the previous
setup will be overridden.