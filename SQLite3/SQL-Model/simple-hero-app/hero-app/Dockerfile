# builder stage to install all requirements
FROM python:3.8-slim AS builder
WORKDIR /env
COPY requirements.txt /requirements.txt
# create venv and install requirements
RUN python -m venv local_env && \
    . local_env/bin/activate && \
    pip install --no-cache-dir -r /requirements.txt


# runner stage to actually run application
FROM python:3.8.7-alpine3.12 as runner
WORKDIR /app
# copy requirements from builder to runner
COPY --from=builder /env/local_env ./local_env
COPY . .

RUN . local_env/bin/activate
# include python in path at beginning
ENV PATH=/app/local_env/bin:$PATH

ENV PORT=8501
EXPOSE ${PORT}
# CMD ["python", "-m" ,"uvicorn", "app:app", "--host=0.0.0.0", "--port=${PORT}"]
CMD python -m uvicorn app:app --host=0.0.0.0 --port=${PORT}
# CMD [ "python", "app.py"]