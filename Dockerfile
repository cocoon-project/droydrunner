FROM cocoon/uiautomator
MAINTAINER cocoon.project@gmail.com

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -qq
RUN apt-get install -y  -q git
RUN git clone https://github.com/cocoon-project/droydrunner.git /tmp/droydrunner

WORKDIR /tmp/droydrunner

# install dependancies
#ADD ./requirements.txt /tmp/droydrunner/
RUN pip install -r requirements.txt

# install droydrunner
#ADD ./README.md /tmp/droydrunner/
RUN python setup.py install

# setup script for pyrun
#ADD droydrunner/droydrun.py /opt/python/bin/droydrun
#RUN chmod +x /opt/python/bin/droydrun
#ENV PATH /opt/python/bin:$PATH

# setup script for official python
ADD droydrunner/droydrun.py /usr/bin/droydrun
RUN chmod +x /usr/bin/droydrun



RUN apt-get clean
EXPOSE 5000
#CMD python /usr/local/bin/droydrun.py phone hub server start
