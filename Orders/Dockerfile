FROM python:3.10
RUN apt-get update && apt-get install -y
RUN pip install --upgrade pip
RUN pip install pipenv
RUN groupadd -r appuser
RUN useradd -r -m -g appuser appuser
WORKDIR /home/appuser/app
COPY ["Pipfile", "Pipfile.lock", "./"]
COPY src/. /home/appuser/app
EXPOSE 5000
RUN pipenv install --system --deploy
USER appuser
CMD ["gunicorn", "--bind", ":5000", "main:app"]