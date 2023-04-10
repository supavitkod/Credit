FROM python:3.7.12-slim

# RUN pip install pipenv

WORKDIR /app

# COPY ["Pipfile" , "Pipfile.lock" , "./" ]

# RUN pipenv install --deploy --system

COPY ["requirements.txt", "./"]

RUN pip install -r requirements.txt

COPY ["enpoint-fast.py", "Model_C=1.0.bin" , "./"]

EXPOSE 9696

# ENTRYPOINT [ "bash" ]
CMD ["uvicorn", "enpoint-fast:app", "--host", "0.0.0.0", "--port", "9696", "--reload"]
# uvicorn enpoint-fast:app --host 0.0.0.0 --port 9696 --reload
# ENTRYPOINT [ "gunicorn","--bind","0.0.0.0:9696","enpoint-fast:app" ]


