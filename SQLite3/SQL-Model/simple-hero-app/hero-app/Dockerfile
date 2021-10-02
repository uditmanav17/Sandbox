# builder stage to install all requirements
FROM python:3.9-slim AS builder
WORKDIR /env
COPY requirements.txt /requirements.txt
# create venv and install requirements
RUN python -m venv local_env && \
    . local_env/bin/activate && \
    # /env/local_env/bin/python -m pip install --upgrade pip && \
    apt-get update && apt-get install python3-dev libpq-dev gcc -y  && \
    pip install --no-cache-dir -r /requirements.txt


# runner stage to actually run application
FROM python:3.9-slim as runner
WORKDIR /app
# copy requirements from builder to runner
COPY --from=builder /env/local_env ./local_env
COPY . .

RUN apt-get update && apt-get install libpq-dev -y && \
    . local_env/bin/activate
# include python in path at beginning
ENV PATH=/app/local_env/bin:$PATH

ENV PORT=8501
EXPOSE ${PORT}
# CMD ["python", "-m" ,"uvicorn", "app:app", "--host=0.0.0.0", "--port=${PORT}"]
CMD python -m uvicorn app:app --host=0.0.0.0 --port=${PORT}
# CMD [ "python", "app.py"]