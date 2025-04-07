FROM pypy:latest

WORKDIR /house-expense-app

COPY . /house-expense-app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD python manage.py runserver 0.0.0:8080 
