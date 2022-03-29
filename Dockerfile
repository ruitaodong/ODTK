FROM	nvcr.io/nvidia/pytorch:20.11-py3 as odtk

RUN	git clone -b 21.06 https://github.com/NVIDIA/retinanet-examples.git

WORKDIR retinanet-examples

#RUN	git checkout 1c3eea7c643c2a486d456c41e3165229ac1217de #v0.25

RUN	python3 setup.py build_ext --inplace

FROM	ubuntu:bionic

RUN	apt-get update && apt-get install -y python3-pip

RUN	pip3 install -U pip &&\
	pip3 install --no-cache-dir torch==1.8.2+cu111 torchvision==0.9.2+cu111 -f https://download.pytorch.org/whl/lts/1.8/torch_lts.html

WORKDIR /opt/odtk/

COPY	--from=odtk /workspace/retinanet-examples/setup.py ./
COPY	--from=odtk /workspace/retinanet-examples/odtk ./odtk/
COPY	--from=odtk /usr/local/cuda /usr/local/cuda

#RUN	python3 setup.py install



