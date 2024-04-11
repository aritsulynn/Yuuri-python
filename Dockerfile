# run by 
# docker build -t anith .
# docker run -p 5173:5173 anith

FROM python:3.9-alpine3.18

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

CMD [ "python", "src/main.py" ]