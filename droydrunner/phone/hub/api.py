__author__ = 'cocoon'
"""

    native API to phone hub



"""

import sys
import time
import json
import requests
from droydrunner.utils.store import Store as EmbededStore

#from droydrunner.api.server.droyd_relay import DroydRelay



from droydrunner.uihub import UiHub


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



class Store(EmbededStore):
    """

    """

    def setup(self):
        pass


class PhoneSession():
    """

    """
    def __init__(self,store,**accounts):
        """
        """
        self._store = store
        self.add_users(**accounts)


    def add_users(self,**accounts):
        """

        """
        for k,v in accounts.iteritems():
            self._store.add_entity('main',k,v)


    def close(self):
        """
        """



class IClient(object):
    """

    """



    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self._store.close()


    def open_session(self,**accounts):
        """

            open a phone session:
                store accounts
        :param accounts:
        :return:
        """
        raise NotImplementedError


    def close_session(self):
        """
            close current session

        :param session_id:
        :return:
        """
        raise NotImplementedError


    def call_number(self,user,number):
        """

        :param agent:
        :param number:
        :return:
        """
        raise NotImplementedError


    def wait_incoming_call(self,user):
        """

        :param agent:
        :return:
        """
        raise NotImplementedError


    def answer_call(self,user):
        """

        :param agent:
        :return:
        """
        raise NotImplementedError


    def reject_call(self,user):
        """

        :param agent:
        :return:
        """
        raise NotImplementedError


    def hangup(self,user):
        """

        :param agent:
        :return:
        """
        raise NotImplementedError




class NativeClient(IClient):
    """
        Native Client to DroyRunner Phone application via api.server.droyd_relay

    """

    def __init__(self,log_cb=None):
        """

        :param url:
        :return:
        """
        self.title = 'uiphone'


        if log_cb is None:
            # no gven log callbck use the module default out() function
            self.out = out
        else:
            # use the given callback for output
            self.out=log_cb

        self._store = Store()


        # the phone session
        self._session = None



        # the relay
        #self.relay = DroydRelay()

        self.hub = UiHub()
        self.agents = {}



    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self._store.close()


    def log(self,msg):
        """

        """
        self.out("pilot: %s" %  msg)


    def open_session(self,**accounts):
        """

            open a phone session:
                store accounts
        :param accounts:
        :return:
        """
        #if self._session:
        #    return self._session
        # save session data
        self._session = PhoneSession(self._store,**accounts)


        # request to server
        #return  self.relay.open_session(**accounts)


        for device_id , device_data in accounts.iteritems():

            serial = device_id
            alias  = device_data.get('alias',serial)

            # create and launch agent
            self.log("Start Agent: %s with role: %s" % (device_id,alias))


            # create an agent
            agent = self.hub.add_device(alias=alias ,serial=serial,applications=None)

            # update internal indexes
            self.agents[serial]= agent


            # open phone app
            self.log("open phone for user %s" % serial)

            self.agents[device_id].phone.open()

            #self.execute(alias,'phone.open')

        return True


    def close_session(self,result=0,error=0):
        """
            close current session

        :param session_id:
        :return:
        """
        #session_name = self._session.content['session']

        #return self.relay.close_session()

        time.sleep(1)
        self.shutdown()


        if result == 0:
            self.log( "<*> Test " + self.title + " completed successfully")
        else:
            self.log("<*> Test " + self.title + " completed with errors " + str(error) )

        del self.agents
        self.agents={}

        return result

    def shutdown(self):
        """

        """
        # Shutdown all instances
        self.log("shutdown ...")
        #time.sleep(2)
        for agent in self.agents.values():
            self.log("shutdown agent")
            #agent.shutdown()
            agent.close()
        self.log("shutdown completed")
        return



    def call_number(self,user,number):
        """

        :param agent:
        :param number:
        :return:
        """
        #agent = self._session.content[user]


        #return self.relay.execute(user,'phone.call_destination', destination = number)

        return self.agents[user].phone.call_destination(destination=number)



    def wait_incoming_call(self,user):
        """

        :param agent:
        :return:
        """
        #agent = self._session.content[user]

        #return self.relay.execute(user,'phone.wait_incoming_call')
        return self.agents[user].phone.wait_incoming_call()


    def answer_call(self,user):
        """

        :param agent:
        :return:
        """
        #agent = self._session.content[user]

        #return self.relay.execute(user,'phone.answer_call')
        return self.agents[user].phone.answer_call()


    def reject_call(self,user):
        """

        :param agent:
        :return:
        """
        #agent = self._session.content[user]

        #return  self.relay.execute(user,'phone.reject_call')
        return self.agents[user].phone.reject_call


    def hangup(self,user):
        """

        :param agent:
        :return:
        """
        #agent = self._session.content[user]

        #return  self.relay.execute(user,'phone.hangup')
        return self.agents[user].phone.end_call()



    # low levels
    def wait(self,user,action,**kwargs):
        """

        :param user:
        :param action:  idle or update
        :param kwargs:
        :return:
        """
        agent =  self.agents[user]

        if action == 'update':
            return agent.device.wait.update(**kwargs)
        elif action == 'idle':
            return agent.device.wait.idle(**kwargs)
        else:
            raise RuntimeError("unkwown command device.wait.%s" % action)






    def select(self,user,selector=None,action=None,action_args=None,**kwargs):
        """


        :param selector:
        :param action: can be click , text , exists , set_text , wait.update wait.exists , info ...
        :param action_args:
        :param kwargs:  can be any of  text, resourceId, index, instance ,className ,packageName ...
        :return:



        """
        if selector != None:
            raise NotImplementedError('selection by custom selector not available')
        # get the selector
        selected =  self.agents[user].device(**kwargs)
        if not selected.exists:
            raise ValueError('selector does not exists: %s' , str(kwargs))
        # determine action
        if not action:
            # not an action : return selector.info
            action = 'info'

        if not '.' in action:
            # simple action
            #if action in ['text','info','exists']:
            # attributes :
            try:
                action_attribute = getattr(selected,action)
            except AttributeError:
                raise AttributeError('unkwown selector action: %s ' % action)
            if callable(action_attribute):
                # a method
                if action_args :
                    # call with args
                    return action_attribute(*action_args)
                else:
                    # call withour args
                    return action_attribute()
            else:
                # an attribute
                return action_attribute
        else:
            # composite action eg wait.update wait.exists
            first,second = action.split('.')
           # extract first
            try:
                first_attr = getattr(selected,first)
            except:
                raise ValueError('unkwown action:%s' % action)
            # extract second
            try:
                second_attr = getattr(first_attr,second)
            except:
                raise ValueError('unkwown action:%s' % action)
            # determine kind of action (attribute , method , method with args
            action_attribute = second_attr
            if callable(action_attribute):
                # a method
                if action_args :
                    # call with args
                    return action_attribute(*action_args)
                else:
                    # call withour args
                    return action_attribute()
            else:
                # an attribute
                return action_attribute

    def command(self,user,action,*args,**kwargs):
        """


        :param user:
        :param action: one of wait.update ...open.notification
        :param args:
        :return:
        """
        agent_device =  self.agents[user].device

        if not '.' in action:
            # simple action
            if action in ['text','info','exists']:
                # attributes :
                try:
                    action_attribute = getattr(agent_device,action)
                except AttributeError:
                    raise AttributeError('unkwown selector action: %s ' % action)
                if callable(action_attribute):
                    # a method
                    return action_attribute(*args,**kwargs)
                else:
                    # an attribute
                    return action_attribute
        else:
            # composite action eg wait.update wait.exists
            first,second = action.split('.')
           # extract first
            try:
                first_attr = getattr(agent_device,first)
            except:
                raise ValueError('unkwown action:%s' % action)
            # extract second
            try:
                second_attr = getattr(first_attr,second)
            except:
                raise ValueError('unkwown action:%s' % action)
            # determine kind of action (attribute , method , method with args
            action_attribute = second_attr
            if callable(action_attribute):
                # a method
                return action_attribute(*args,**kwargs)
            else:
                # an attribute
                return action_attribute

