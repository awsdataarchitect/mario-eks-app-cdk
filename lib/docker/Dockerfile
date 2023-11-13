FROM python:3-buster

# Expose the necessary port
EXPOSE 8501

# Set environment variables
ENV DIRPATH=/app

# Install required dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive  && apt-get install -y \
    build-essential \
    libcurl3-dev \
    libfreetype6-dev \
    libpng-dev \
    libzmq3-dev \
    pkg-config \
    python3 \
    python3-dev \
    rsync \
    software-properties-common \
    unzip \
    wget

RUN pip install --no-cache-dir tensorflow
RUN pip install streamlit
RUN apt-get install -y python3-opencv
RUN pip install opencv-python
RUN pip install Pillow


# Set the working directory
WORKDIR $DIRPATH

COPY . /app

# Download and unzip the required models and data
RUN wget https://grfia.dlsi.ua.es/primus/models/PrIMuS/Semantic-Model.zip
RUN unzip Semantic-Model.zip -d ${DIRPATH}/Semantic-Model
RUN rm Semantic-Model.zip

RUN wget https://raw.githubusercontent.com/OMR-Research/tf-end-to-end/master/Data/vocabulary_semantic.txt -q -O ${DIRPATH}/vocabulary_semantic.txt

# Download the required font
RUN wget https://www.fontsquirrel.com/fonts/download/Aaargh -O Aaargh.zip
RUN unzip Aaargh.zip 
RUN rm Aaargh.zip

RUN chmod 512 ${DIRPATH}/vocabulary_semantic.txt

# Set the command to run the Streamlit app
CMD ["streamlit", "run", "app.py"]
