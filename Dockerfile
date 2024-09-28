FROM python:3.10-bookworm

WORKDIR /opt

RUN --mount=type=bind,source=requirements.txt,target=requirements.txt pip install -r requirements.txt

COPY main.py /opt

CMD ["python", "main.py"]