FROM cocoon/uiautomator
MAINTAINER cocoon.project@gmail.com

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -qq
RUN apt-get install -y  -q git
RUN git clone https://github.com/cocoon-project/droydrunner.git /tmp/droydrunner

WORKDIR /tmp/droydrunner
RUN python setup.py install

RUN apt-get clean
EXPOSE 5000
CMD python /usr/local/bin/droydrun.py phone hub server start
