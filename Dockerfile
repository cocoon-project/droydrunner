FROM cocoon/uiautomator
MAINTAINER cocoon.project@gmail.com

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -qq
RUN apt-get install -y  -q git
RUN git clone https://github.com/cocoon-project/droydrunner.git /tmp/droydrunner

WORKDIR /tmp/droydrunner

# install dependancies
ADD ./requirements.txt /tmp/droydrunner/
RUN pip install -r requirements.txt

# install droydrunner
ADD ./README.md /tmp/droydrunner
RUN python setup.py install

RUN apt-get clean
EXPOSE 5000
#CMD python /usr/local/bin/droydrun.py phone hub server start
