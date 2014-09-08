FROM cocoon/uiautomator
MAINTAINER cocoon.project@gmail.com
#ENV DEBIAN_FRONTEND noninteractive
#RUN apt-get update -qq
#RUN apt-get install -y  -q git
#CMD git clone https://github.com/cocoon-project/droydrunner.git /tmp/droydrunner
ADD droydrunner/droydrunner/droydrun.py /usr/local/bin/
ADD droydrunner/droydrunner /usr/local/lib/python2.7/dist-packages/droydrunner
#ADD droydrunner /tmp/droydrunner
#WORKDIR /tmp/droydrunner
#CMD python setup.py install
#CMD cp /usr/local/lib/python2.7/dist-packages/droydrunner/droydrun.py /usr/local/bin
#RUN apt-get clean
EXPOSE 5000
CMD python /usr/local/bin/droydrun.py phone hub server start
