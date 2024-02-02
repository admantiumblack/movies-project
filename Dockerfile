FROM python:3.12
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get upgrade -y
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY ./ ./
RUN python manage.py migrate
Run python manage.py seeddatabase
ENTRYPOINT ["python", "manage.py", "runserver"]
CMD ["0.0.0.0:8000"]