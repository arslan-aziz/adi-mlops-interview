FROM python:3.8

# install jdk
RUN apt install -y wget apt-transport-https && \
    mkdir -p /etc/apt/keyrings && \
    wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | tee /etc/apt/keyrings/adoptium.asc && \
    echo "deb [signed-by=/etc/apt/keyrings/adoptium.asc] https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | tee /etc/apt/sources.list.d/adoptium.list && \
    apt update && apt install -y temurin-8-jdk

ENV JAVA_HOME=/usr/lib/jvm/temurin-8-jdk-amd64

# download jars for spark
RUN wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.349/aws-java-sdk-bundle-1.12.349.jar && \
    wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.2/hadoop-aws-3.3.2.jar && \
    mkdir -p /opt/spark/jars && \
    mv aws-java-sdk-bundle-1.12.349.jar /opt/spark/jars/ && \
    mv hadoop-aws-3.3.2.jar /opt/spark/jars/

ENV APP_DIR=/opt/application
WORKDIR ${APP_DIR}

COPY requirements.txt .
RUN pip3 install -r requirements.txt && \
    mkdir -p /usr/local/lib/python3.8/site-packages/pyspark/conf
COPY spark-defaults.conf /usr/local/lib/python3.8/site-packages/pyspark/conf/

COPY data_ingestion data_ingestion

COPY docker-entrypoint.sh .

ENTRYPOINT [ "./docker-entrypoint.sh" ]
