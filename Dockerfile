FROM python:3.12

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir
RUN pip install gunicorn --no-cache-dir

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg

COPY . .

ENV SECRET_KEY="your_secret_key"
ENV INFERENCE_API_URL="INFERENCE_API_URL"
ENV SQLALCHEMY_DATABASE_URI="sqlite:///database.db"

EXPOSE 5000
CMD ["python", "app.py"]
# CMD ["gunicorn", "-w", "1", "--preload", "--access-logfile", "-", "--error-logfile", "-", "-b", "0.0.0.0:5000", "app:create_app()"]