# Space invaders 👾

<div>
    <h4>The classic space invaders game, but in terminal!</h4>
    <img src="https://github.com/Devkeystuff/space-invaders/blob/main/docs/game.png" alt="Game showcase" />
</div>

## Git clone

    git clone https://github.com/Devkeystuff/space-invaders.git

## Running locally

It's recommended to run this project in Linux environment

### [Docker](https://www.docker.com/get-started)

The database and backend runs in containers, so it's easier to develop in actual database, but locally.

Usually it's a good practice to containerize backend.

### [Python](https://www.python.org/downloads/)

Use python v3.10.x

## Actions

For code formatting and more concise dependency installation we're using `Makefile`

### Install dependencies
    
    make setup

and then install python dependencies to automatically generated virtualenv

    pip install -r requirements.txt

### Start project

    make dev
    
### Format code
    
    make format

## Git rules

Commit messages [follow conventional commits](https://www.conventionalcommits.org/en/v1.0.0-beta.2/)
