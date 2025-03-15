ARG base_img

FROM $base_img
WORKDIR /

USER 0

RUN mkdir ${SPARK_HOME}/python
RUN apt-get update && \
    apt-get install -y curl && \
    apt install -y python3 python3-pip && \
    pip install --upgrade pip setuptools && \
    rm -r /root/.cache && rm -rf /var/cache/apt/*

RUN curl https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.563/aws-java-sdk-bundle-1.11.563.jar -o ${SPARK_HOME}/jars/aws-java-sdk-bundle-1.11.563.jar
RUN curl https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.2.0/hadoop-aws-3.2.0.jar -o ${SPARK_HOME}/jars/hadoop-aws-3.2.0.jar

COPY python/pyspark ${SPARK_HOME}/python/pyspark
COPY python/lib ${SPARK_HOME}/python/lib
COPY python_main/ ${SPARK_HOME}/python_main

WORKDIR /opt/spark/work-dir
ENTRYPOINT [ "/opt/entrypoint.sh" ]

ARG spark_uid=185
USER ${spark_uid}