FROM python:3.9.10-alpine

RUN mkdir "/usr/src/devman-homework"

WORKDIR /usr/src/devman-homework
COPY requirements.txt /usr/src/devman-homework/

RUN pip install --no-cache-dir -r requirements.txt
COPY . .


ENTRYPOINT ["python"]
CMD ["request_to_devman.py"]
