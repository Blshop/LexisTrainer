FROM python:3.10.0b2-alpine3.13
ENV install_path / LexisTrainer
RUN mkdir -p $install_path

WORKDIR $install_path

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD gunicorn -b 0.0.0.0:8000 --access-logfile - 'LexisTrainer.app:create_app()'
