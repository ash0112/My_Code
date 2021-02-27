FROM python:3.7
COPY . /aws_app_deployment
WORKDIR /aws_app_deployment
RUN pip install -r requirements.txt
CMD ["echo", "starting the application"]
ENTRYPOINT ["python"]
CMD ["aws_app_hello_world.py"]
