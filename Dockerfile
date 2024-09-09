FROM python:3.10
WORKDIR /code

COPY . .
RUN pip install --no-cache-dir --upgrade pip setuptools
RUN pip install flask numpy pandas matplotlib scikit-learn yahoo_fin requests_html
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
CMD ["flask", "run"]