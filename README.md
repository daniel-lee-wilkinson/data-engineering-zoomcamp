# data-engineering-zoomcamp
Codespaces

# terminal prompt "address" shortening
PS1= "> "
# configure bash
echo "PS1=">"' > ~/.bashrc

# Introduction to Docker
- sandbox
- isolated from host machine
- stateless (does not save your stuff when you close it)

# docker installed?
docker
docker run hello-world # downloads image hello-world

docker run ubuntu
docker run -it ubuntu # get inside the image
apt update
apt install python3
exit

# use python docker image
docker run -it python:3.13.11 # on a debian system
exit
docker run -it python:3.13.11-slim # image_name:tag -> docker image

# enter bash instead of python but still in docker image
docker run -it --entrypoint=bash python:3.13.11-slim

python -V # version of python in this image

stateless but can resume a state from "docker ps -a"
docker rm `docker ps -aq` # to clean environment

# how to preserve state?
## volumes
accessible on host machine and in the docker container

docker run -it \
    --rm \
    -v $(pwd)/test:/app/test \  #volume mapping with -v, host_machine_location:docker_image_location
    --entrypoint=bash \
    python:3.9.16-slim

# --------

# Data Pipelines

input data from source --> processing --> output data to destination

csv --> e.g. parquet, postgresQL database, data warehouse

New York Trip Data
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

1. download csv file
2. 
3. save into postgresQL database

#TODO: add "python" extension to VSCode see autocomplete options

# create virtual environment
- packages not on local computer, not on docker machine per se
- virtual machine is on my host
- isolate projects from each other

use `uv `
@daniel-lee-wilkinson ➜ /workspaces/data-engineering-zoomcamp/pipeline (main) $ ls
pipeline.py
@daniel-lee-wilkinson ➜ /workspaces/data-engineering-zoomcamp/pipeline (main) $ uv init --python 3.13
Initialized project `pipeline`
@daniel-lee-wilkinson ➜ /workspaces/data-engineering-zoomcamp/pipeline (main) $ which python
/home/codespace/.python/current/bin/python
@daniel-lee-wilkinson ➜ /workspaces/data-engineering-zoomcamp/pipeline (main) $ pyton -v
bash: pyton: command not found
@daniel-lee-wilkinson ➜ /workspaces/data-engineering-zoomcamp/pipeline (main) $ python -V
Python 3.12.1
@daniel-lee-wilkinson ➜ /workspaces/data-engineering-zoomcamp/pipeline (main) $ uv run python -V
Using CPython 3.13.12
Creating virtual environment at: .venv
Python 3.13.12

# add depndencies
uv add pandas pyarrow

# run script in terminal
uv run python pipeline.py 12 # 12th month



# create Dockerfile

# build the docker container

# run docker container. Use "--rm" to clean up remaining files.
docker run -it --entrypoint=bash --rm  test:pandas