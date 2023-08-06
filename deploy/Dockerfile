FROM python:3.11.4

ARG TOKEN
ENV TOKEN=$TOKEN
COPY requirements.txt .
RUN pip install --upgrade pip \
    pip install -r requirements.txt

COPY bot bot
CMD python3 -m bot