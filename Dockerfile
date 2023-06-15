FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt -y update && apt -y install make build-essential python3.10 python3.10-venv python3-pip vim

COPY Makefile .
COPY requirements.txt .
COPY setup.py .
COPY src/ .

RUN make setup build

CMD ["make", "run"]
