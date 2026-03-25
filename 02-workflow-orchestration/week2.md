# Week 2: Workflow Orchestration

Tools: Kestra
- open source
- even-driven orchestration platform

Goal:
- build a ETL pipeline with Kestra for orchestration


# Vocabulary

1. Orchestration:
- orchestrator lets tools interact/communicate with each other
- provides logging information
- allow parallel or looping
- automation

2. Kestra
- orchestration platform
- workflow as code, no code or with AI
- many plug-ins e.g. postgres, GCP
- language agnostic --> e.g. python or C
- logging of workflows and errors --> good overview
- scheduled and event-based triggers

# Installing Kestra

-  update docker-compose.yaml with kestra container and service
-   run docker compose up in pipeline/ --> 4 ports
--> Log into Kestra via 8080


can execute python directly in Kestra but only suitable for very small code. It spins up a Docker container to run python --> no dependencies conflicts with other tasks in workflow. If were running Kestra locally, could run the Python in a virtual environment to keep dependencies straight.
else access python files

