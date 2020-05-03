FROM python:3.6
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt
WORKDIR /admin_interface
COPY . /admin_interface
EXPOSE 32501
CMD ["python3.6", "admin_interface.py"]