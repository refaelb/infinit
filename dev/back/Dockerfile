# FROM python:3.8 AS compile-image
# WORKDIR /app
# COPY . /app
# RUN pip install -r requirements.txt
# # ENTRYPOINT ["python"]
# # CMD ["index.py"]

# FROM python:3.7-slim-stretch
# COPY --from=compile-image /app /app
# WORKDIR /app
# # COPY . /app
# EXPOSE 3000
# ENTRYPOINT ["python"]
# CMD ["index.py"]






FROM python:3.10-slim AS build
RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt


FROM python:3.10-slim

COPY --from=build /venv /venv
ENV PATH=/venv/bin:$PATH

COPY . .
ENTRYPOINT ["python"]
CMD ["index.py"]