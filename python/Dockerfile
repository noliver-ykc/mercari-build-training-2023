FROM alpine

RUN addgroup -S mercari && adduser -S trainee -G mercari
# RUN chown -R trainee:mercari /path/to/db
RUN apk update && apk add --no-cache python3 py3-pip && python3 --version && pip3 --version

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY main.py main.py

COPY ./db/mercari.sqlite3 /db/mercari.sqlite3

VOLUME /db
USER trainee

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
CMD ["python", "-V"]
