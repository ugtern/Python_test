FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /python_test
WORKDIR /python_test
ADD requirements.txt /python_test/
RUN pip install -r requirements.txt
ADD . /python_test/