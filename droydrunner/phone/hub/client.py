__author__ = 'cocoon'
"""

    HTTP api to phone hub

"""

import sys
import json
import requests



# from droydrunner.utils.store import Store as EmbededStore
# from droydrunner.api.server.droyd_relay import DroydRelay
# from droydrunner.uihub import UiHub


# default log_cb
stdout_no_buf = True

def out(msg,nl=True):
    """
        send message to stdout and flush
    """
    if nl:
        # newline : print msg + nl
        print msg
    else:
        # send without new line
        print msg,

    if stdout_no_buf:
        sys.stdout.flush()



# class Store(EmbededStore):
#     """
#
#     """
#
#     def setup(self):
#         pass


class PhoneSession():
    """

    """
    def __init__(self):
        """
        """
        self._store = {
            'accounts' : {},
            'current':  {}
        }



    def add_users(self,**accounts):
        """

        """
        for k,v in accounts.iteritems():
            self._store['accounts'][k]= v
            #self._store.add_entity('main',k,v)


    def current_session(self,data=None):
        """
            current session info
        """
        if not data:
            # read it
            return self._store['current']
        else:
            # set data
            self._store['current'] = data

    def close(self):
        """
        """
        self._store = {
            'accounts' : {},
            'current':  {}
        }








class Client(object):
    """

    """

    def __init__(self,url):
        """

        :param url:
        :return:
        """
        # the base url eg localhost:5000
        self._url = url

        # set the requests session
        self._web_session=requests.Session()
        self._web_session.headers.update({
            'content-type': 'application/json',
            'accept': 'application/json'
            })


        # the phone session
        self._session = None


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        #self._store.close()
        if self._session:
            self._session.close()

    def url(self, uri = None):
        """

        :param complement:
        :return:
        """
        if not uri:
            return self._url
        else:
            #return "/".join(self._url , uri )
            return "%s%s" % (self._url,uri)



    def open_session(self,**accounts):
        """

            open a phone session:
                store accounts
        :param accounts:
        :return:
        """
        if self._session:
            return self._session
        # save session data
        self._session = PhoneSession()
        self._session.add_users(**accounts)

        # request to server
        data = json.dumps(accounts)
        response = self._web_session.post(self.url('/sessions'),data=data)

        response_data = json.loads(response.content)
        #self._session.content = response_data
        # save the session data
        self._session.current_session(response_data)
        return response_data


    def close_session(self):
        """
            close current session

        :param session_id:
        :return:
        """
        session_name = self._session.current_session()['session']
        uri = '/sessions/%s' % session_name
        response = self._web_session.delete(self.url(uri))

        self._session.close()
        return response





    def call_number(self,user,number):
        """

        :param agent:
        :param number:
        :return:
        """
        agent = self._session.current_session()[user]

        uri = '/agents/%s/call_number' % agent
        data = json.dumps(dict( number = number))
        response = self._web_session.post(self.url(uri),data=data)

        return response


    def wait_incoming_call(self,user):
        """

        :param agent:
        :return:
        """
        agent = self._session.current_session()[user]

        uri = '/agents/%s/wait_incoming_call' % agent
        data = json.dumps({})

        response = self._web_session.post(self.url(uri),data=data)

        return response


    def answer_call(self,user):
        """

        :param agent:
        :return:
        """
        agent = self._session.current_session()[user]

        uri = '/agents/%s/answer_call' % agent
        data = json.dumps({})
        response = self._web_session.post(self.url(uri),data=data)

        return response


    def reject_call(self,user):
        """

        :param agent:
        :return:
        """
        agent = self._session.current_session()[user]

        uri = '/agents/%s/reject_call' % agent

        data = json.dumps({})
        response = self._web_session.post(self.url(uri),data=data)

        return response


    def hangup(self,user):
        """

        :param agent:
        :return:
        """
        agent = self._session.current_session()[user]

        uri = '/agents/%s/hangup' % agent

        response = self._web_session.post(self.url(uri))

        return response

    # low level api

    # low levels
     # low levels
    def wait(self,user,action,**kwargs):
        """

        :param user:
        :param action:  idle or update
        :param kwargs:
        :return:
        """
        agent = self._session.current_session()[user]

        uri = '/agents/%s/wait' % agent

        data = dict(action=action)
        data.update(kwargs)
        data = json.dumps(data)
        response = self._web_session.post(self.url(uri),data=data)

        try:
            response_data=response.json()
            return response_data['response']
        except ValueError:
            return None



    def select(self,user,selector=None,action=None,action_args=None,**kwargs):
        """


        :param selector:
        :param action: can be click , text , exists , set_text , wait.update wait.exists , info ...
        :param action_args:
        :param kwargs:  can be any of  text, resourceId, index, instance ,className ,packageName ...
        :return:



        """
        #raise NotImplementedError
        agent = self._session.current_session()[user]

        uri = '/agents/%s/select' % agent

        data = dict(selector=selector,action=action,action_args=action_args)
        data.update(kwargs)
        data = json.dumps(data)
        response = self._web_session.post(self.url(uri),data=data)

        try:
            response_data=response.json()
            return response_data['response']
        except ValueError:
            return None





    def command(self,user,action,**kwargs):
        """


        :param user:
        :param action: one of wait.update ...open.notification
        :param args:
        :return:
        """
        #raise NotImplementedError
        agent = self._session.current_session()[user]

        uri = '/agents/%s/command' % agent

        data = dict(action=action,**kwargs)
        data.update(kwargs)
        data = json.dumps(data)
        response = self._web_session.post(self.url(uri),data=data)

        try:
            response_data=response.json()
            return response_data['response']
        except ValueError:
            return None


HttpClient=Client



