FROM python:3.10
WORKDIR /code

COPY . .
RUN pip install --no-cache-dir --upgrade pip setuptools
RUN pip install -r requirements.txt
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
CMD ["flask", "run"]