FROM python:3.6
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt
WORKDIR /client_interface
COPY . /client_interface
EXPOSE 32502
CMD ["python3.6", "client_interface.py"]