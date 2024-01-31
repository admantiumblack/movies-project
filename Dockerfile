FROM python:3.12 as test
RUN apt-get update && apt-get upgrade -y
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY ./ ./
ENTRYPOINT ["pytest", "--doctest-modules", "--junitxml=junit/test-results.xml", "--cov=.", "--cov-report=xml", "--cov-report=html"]
CMD ["."]

FROM python:3.12 as build
RUN apt-get update && apt-get upgrade -y
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY ./src ./
RUN chmod +x ./main.py
ENTRYPOINT ["python", "./src/main.py"]
CMD []