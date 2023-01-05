FROM python:3.8 AS compile-image
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 3000
ENTRYPOINT ["python"]
CMD ["index.py"]

FROM python:3.7-slim AS build-image
COPY --from=compile-image /app /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["index.py"]




