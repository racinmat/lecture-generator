FROM maven:3-jdk-8

RUN mkdir /app && \
    cd /app && \
    git clone https://github.com/marytts/marytts.git . && \
    git checkout 5.x

RUN mvn install && \
    ./marytts install && \
    ./marytts install voice-cmu-slt

ENV PATH="${PATH}:/app/target/marytts-builder-5.3-SNAPSHOT/bin"
