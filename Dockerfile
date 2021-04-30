FROM openjdk:8-jdk-buster
COPY --from=python:2.7.18-buster / /

COPY . /usr/src/id-openie
WORKDIR /usr/src/id-openie

RUN wget https://services.gradle.org/distributions/gradle-6.8.3-bin.zip
RUN unzip gradle-6.8.3-bin.zip -d /gradle
ENV PATH="/gradle/gradle-6.8.3/bin:${PATH}"

RUN gradle clean build
RUN unzip build/distributions/id-openie-1.0.zip
RUN pip install -r scripts/requirements.txt

WORKDIR id-openie-1.0