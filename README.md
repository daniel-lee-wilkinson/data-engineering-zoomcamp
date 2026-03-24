# Week 1 Notes: Docker & PostgreSQL

## Terminal Setup
```bash
# Shorten terminal prompt
PS1="> "
echo "PS1=">"' > ~/.bashrc
```

---

## Docker Basics

**Key concepts:**
- Sandbox environment, isolated from host machine
- Stateless — does not persist data when container closes
- Can resume a stopped container via `docker ps -a`
```bash
docker run hello-world                                        # test installation
docker run -it ubuntu                                         # run ubuntu interactively
docker run -it python:3.13.11-slim                            # run python image (slim = smaller)
docker run -it --entrypoint=bash python:3.13.11-slim          # enter bash instead of python REPL
docker ps -a                                                  # list all containers including stopped
docker rm `docker ps -aq`                                     # clean up all stopped containers
```

---

## Persisting Data: Volumes

Volumes are accessible on both the host machine and inside the container.
```bash
docker run -it \
    --rm \
    -v $(pwd)/test:/app/test \   # host_path:container_path
    --entrypoint=bash \
    python:3.9.16-slim
```

---

## Data Pipelines

**Pattern:** input data → processing → output data

**This week:** CSV/parquet → pandas → PostgreSQL

Data source: [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

---

## Virtual Environments with uv

Packages live in the venv on the host machine, not inside Docker.
```bash
uv init --python 3.13           # initialise project
uv add pandas pyarrow           # add dependencies
uv run python pipeline.py 12    # run script (12 = December)
uv run jupyter notebook          # run jupyter inside venv
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi  # connect to PostgreSQL
```

---

## Docker + Postgres Workflow
```bash
# Build image
docker build -t test:pandas .

# Run container
docker run -it --entrypoint=bash --rm test:pandas

# pgcli runs inside venv on local machine and connects to postgres container
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

---

## TODO
- [ ] Add Python extension to VSCode for autocomplete
