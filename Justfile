setup:
    yarn install
    cd apps/api && conda env create -f environment.yml

format:
    cd apps && yarn format && black ./*

dev:
    docker-compose up