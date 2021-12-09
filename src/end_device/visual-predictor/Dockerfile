# Dockerfile to build a connection to the SQL server
# and get the sensor data to show on the web server
# Written by Parsa Yousefi

FROM python:3.6.6

WORKDIR /visualization

COPY . /visualization

RUN pip3 install --user -r requirements.txt

CMD [ "python3", "visual.py" ]

