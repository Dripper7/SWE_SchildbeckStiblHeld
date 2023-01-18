# pull the python image
FROM python:3.7.3-alpine

# set working directory
WORKDIR /multiple_file_upload

# copy the requirements file into the image
COPY requirements.txt /multiple_file_upload

# install the dependencies
RUN pip install -r requirements.txt

RUN apt-get update && \
    apt-get install -y ffmpeg
# copy content from local directory to the image
COPY . /multiple_file_upload

# configure the container
ENTRYPOINT [ "python" ]

CMD ["main.py"]

LABEL Authors="Held, Schildbeck, Stibl"

