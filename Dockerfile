FROM python:3.10
WORKDIR /code

COPY . .
RUN pip install --no-cache-dir --upgrade pip setuptools
RUN pip install flask yahoo_fin matplotlib scikit-learn pandas joblib numpy requests_html
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=80
EXPOSE 80
CMD ["flask", "run", "--port=80"]