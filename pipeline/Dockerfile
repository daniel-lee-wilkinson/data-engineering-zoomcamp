FROM python:3.13.12-slim

RUN pip install pandas pyarrow

WORKDIR /code

COPY pipeline.py .

ENTRYPOINT ["python", "pipeline.py"]

