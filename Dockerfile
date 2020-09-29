## CODE WRITTEN WITH HELP FROM A FRIEND

FROM python:3
WORKDIR /code
ENV PORT=8000 \
    PYTHONUNBUFFERED=1 \
    GOOGLE_APPLICATION_CREDENTIALS=/code/serviceaccount.json
RUN pip install uwsgi
COPY requirements.txt /code
RUN pip install -r requirements.txt
COPY . /code
CMD /code/run.sh

