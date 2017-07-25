FROM python:3.5.3

RUN pip install --upgrade \
    numpy \
    scipy \
    scikit-learn \
    flask

RUN mkdir /code
WORKDIR /code

COPY data /code/data
COPY service.py /code/

ENV FLASK_APP=service.py
ENV FLASK_DEBUG=0

CMD ["flask", "run", "--host=0.0.0.0"]

# docker build -t tipoftheday-service .
# docker run -it --rm -p 5000:5000 tipoftheday-service
