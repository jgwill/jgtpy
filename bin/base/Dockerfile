FROM jgwill/jgt:fx
#jgwill/jgt:base
#FROM jgwill/ubuntu:py3.10.14-ml

#RUN pip install -U pip
#RUN pip install json2bash
#RUN pip install -U jgtfxcon
#RUN pip install -U --index-url https://test.pypi.org/simple/ jgtutils jgtpy
USER root
RUN pip install -U jgtpy

RUN useradd -ms /bin/bash jgi
RUN echo "jgi ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER jgi
WORKDIR /work

