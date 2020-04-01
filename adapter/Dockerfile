FROM python:3.6
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt
WORKDIR /adapter
COPY . /adapter
EXPOSE 32500
CMD ["python3.6", "adapter.py"]