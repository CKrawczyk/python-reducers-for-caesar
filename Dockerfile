FROM python:3.5-stretch

ENV LANG=C.UTF-8

WORKDIR /usr/src/aggregation

RUN wget "https://extras.wxpython.org/wxPython4/extras/linux/gtk3/debian-9/wxPython-4.0.3-cp35-cp35m-linux_x86_64.whl"
RUN apt-get update
RUN apt-get -y install \
 libwebkitgtk-dev \
 libjpeg-dev \
 libtiff-dev \
 libgtk-3-dev \
 libsdl1.2-dev \
 libgstreamer-plugins-base1.0-dev \
 freeglut3 \
 freeglut3-dev \
 libnotify-dev \
RUN pip install --upgrade pip
RUN pip install wxPython-4.0.3-cp35-cp35m-linux_x86_64.whl

# install dependencies
COPY setup.py .
RUN pip install .[online,test,doc]

# install package
COPY . .
RUN pip install -U .[online,test,doc]

# make documentation
RUN /bin/bash -lc ./make_docs.sh

CMD python routes.py
