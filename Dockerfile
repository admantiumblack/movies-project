FROM python:3.12 as test
RUN apt-get update && apt-get upgrade -y
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY ./ ./
ENTRYPOINT ["python", "manage.py", "startserver"]
CMD []