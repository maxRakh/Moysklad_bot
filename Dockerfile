FROM python:3.9-alpine3.17

COPY requirements.txt /temp/requirements.txt

COPY main /main

WORKDIR /main

EXPOSE 8000

RUN pip install -r /temp/requirements.txt

CMD ["python", "bot.py"]