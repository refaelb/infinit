FROM python:3.8 AS compile-image
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["index.py"]

FROM compile-image 
WORKDIR /app
COPY . /app
EXPOSE 3000
ENTRYPOINT ["python"]
CMD ["index.py"]




