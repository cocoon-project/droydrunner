__author__ = 'cocoon'

import random

from flask import Flask ,url_for ,request
from flask import json

from droydrunner.utils.store import Store as BaseStore
from droydrunner.lib.facets.rest_collections import CollectionWithOperationApi




#from droydrunner.phone.hub.server.droyd_relay import DroydRelay

from droydrunner.phone.hub.api import NativeClient



class Store(BaseStore):
    """

    """
    collections = [ 'main','sessions', 'users' ]


db = Store()

#relay = DroydRelay()

api= NativeClient()

app= Flask(__name__)


@app.route('/')
def index():
    """

    :return:
    """
    return "hello there "



class PhoneOperation(object):
    """
        a relay between http operation and droyd_relay
    """
    op = 'phone.call_destination'
    # request input
    input = {
        'number' : { 'type': str }
    }
    # relay operation input
    output = {
        'destination': {'type': str}
    }

    def extract_parameters(self,request,**kwargs):
        """
        """
        r = request
        data = r.json
        agent = kwargs['item']
        number = data['number']

        return dict(agent=agent,number=number)

    def response(self,response):
        """
        """

        return "call_number: %s" % request.url


    def __call__(self,request,**kwargs):
        """

        """
        # extract request info agent and number
        args = self.extract_parameters(request,**kwargs)

        # r = request
        # data = r.json
        # agent = kwargs['item']
        # number = data['number']



        user,session_id = args['agent'].split('-')

        # fetch the session
        session=db.get('sessions',session_id)

        ## CALL the interface  phone.call  number
        #rs = relay.execute(user,'phone.call_destination', destination = args['number'])
        rs = api.call_number(user,number=args['number'])


        ## return the response
        return self.response(rs)



class DroydAgents(CollectionWithOperationApi):
    """

    """
    def agent_to_user_session(self,agent_name):
        """
            convert agent_name to username and session Alice-123  (Alice,123)
        """
        return agent_name.split('-')


    def op_call_number(self,**kwargs):
        """

        """
        r = request
        data = r.json
        agent = kwargs['item']
        number = data['number']
        user,session_id = self.agent_to_user_session(agent)
        session=db.get('sessions',session_id)


        ## CALL the interface  phone.call  number
        #rs = relay.execute(user,'phone.call_destination', destination = number)
        rs = api.call_number(user,number=number)



        return "call_number: %s" % request.url


    def op_wait_incoming_call(self,**kwargs):
        """

        """
        r = request
        data = r.json
        agent = kwargs['item']

        user,session_id = self.agent_to_user_session(agent)
        session=db.get('sessions',session_id)


        ## CALL the interface  phone.call  number
        #rs = relay.execute(user,'phone.wait_incoming_call')
        rs = api.wait_incoming_call(user)


        return "wait_incoming_call: %s" % request.url



    def op_answer_call(self,**kwargs):
        """

        """
        r = request
        data = r.json
        agent = kwargs['item']


        user,session_id = self.agent_to_user_session(agent)
        session=db.get('sessions',session_id)


        ## CALL the interface  phone.call  number
        #rs = relay.execute(user,'phone.answer_call')
        res = api.answer_call(user)


        return "answer_call: %s" % request.url


    def op_hangup(self,**kwargs):
        """

        """
        r = request
        data = r.json
        agent = kwargs['item']

        user,session_id = self.agent_to_user_session(agent)
        session=db.get('sessions',session_id)


        ## CALL the interface  phone.call  number
        #rs = relay.execute(user,'phone.hangup')
        rs = api.hangup(user)

        print
        return "hangup_call: %s" % request.url


class DroydSessions(CollectionWithOperationApi):
    """

    """

    @classmethod
    def random(cls):
        """
            return a random session

        :return:
        """
        r = "%06x" % random.randint(0,256**3-1)
        return r


    def get(self,item = None):
        return "list session"

    def post(self,**kwargs):
        """
            create a session
        """
        return self.op_open_session(**kwargs)

    def delete(self,item=None):
        """
            delete session
        """
        return self.op_close_session(item=item)


    def op_open_session(self,**kwargs):
        """
            open session
        """
         # create a dummy session
        r =request
        data = request.json
        session_id = self.random()

        # create session
        db.add_entity('sessions',session_id,data)

        r = db.get('sessions',session_id)

        ### CALL the open session
        #rs = relay.open_session(session_id, ** data)
        api.open_session(**data)


        # create response the session id and the agent ids
        response = { 'session': session_id }
        for user_name in data.keys():
            agent_name = "%s-%s" %( user_name,session_id)
            response[user_name]= agent_name


        #s = { 'session': session_id, 'Alice': 'Alice-123' , 'Bob': 'Bob-123' }
        return json.dumps(response)

    def op_close_session(self,**kwargs):
        """
            close session
        """
        session_id = kwargs['item']

        ### close the CALL session
        #relay.close_session()
        api.close_session()


        db.delete('sessions',session_id)
        return "session closed"



# create and register collections : sessions , agents ..
sessions = DroydSessions.create( app ,'sessions', '/sessions' )
agents = DroydAgents.create(app,'agents','/agents')


# session_collection = DroydSessions.as_view('sessions')
# DroydSessions.register(app,session_collection,'/sessions')
#
# agent_collection = DroydAgents.as_view('agents')
# DroydAgents.register(app,agent_collection,'/agents')




def start():
    """

    :return:
    """

    app.debug =True

    app.run(host="127.0.0.1",port = 5001)


def test_random():


    for i in xrange(0,5):

        print DroydSessions.random()




if __name__=="__main__":


    # test
    test_random()


    with app.test_request_context():

        print url_for('index')




    # start the server
    start()
