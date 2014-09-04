__author__ = 'cocoon'
"""

    native API to phone hub



"""

import sys
import time

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




class HubSession(dict):
    """

    """





class NativeClient():
    """
        Native Client to DroyRunner application

    """

    def __init__(self,log_cb=None):
        """

        :param url:
        :return:
        """
        self.title = 'DroydHub'


        if log_cb is None:
            # no gven log callbck use the module default out() function
            self.out = out
        else:
            # use the given callback for output
            self.out=log_cb


        # the phone session
        self._session = HubSession()



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


    def add_device(self,**accounts):
        """

            open a phone session:
                store accounts
        :param accounts:
        :return:
        """

        for device_id , device_data in accounts.iteritems():

            serial = device_id
            alias  = device_id

            # create and launch agent
            self.log("add device: %s " % (device_id))


            # create an agent
            agent = self.hub.add_device(alias=alias ,serial=serial,applications=None)

            # update internal indexes
            self.agents[serial]= agent


            # goto home
            self.log("%s: goto home" % serial)
            self.device(device_id).press('home')


    def device(self,device_id):
        """
            return the uidevice instance for the device_id
        :param device_id:
        :return:
        """
        #return the uidevice associates
        return self.agents[device_id]


    def sys(self,device_id,command):
        """
            return a command for the given device
        :param device_id:
        :param command:
        :return:
        """

        device = self.device(device_id)
        def system_wrapper(*args,**kwargs):

            method = getattr(device,command)
            return method(*args,**kwargs)

        return system_wrapper

    def phone(self,device_id,command):
        """
            return a phone command for the given device
        :param device_id:
        :param command:
        :return:
        """

        device = self.device(device_id)
        def system_wrapper(*args,**kwargs):

            method = getattr(device.phone,command)
            return method(*args,**kwargs)
        return system_wrapper


    def call(self,device_id,command,*args,**kwargs):
        """

            general interface to call a command on a device

            command can be composite app.cmd

            app is the name of an application (phone,mms ..)

            eg call( 'df234' , 'phone.call_destination' , '0101010101' )


        :param device_id:
        :param command:
        :return:
        """
        device = self.device(device_id)
        if '.' in command:
            # composite command
            parts = command.split('.')
            assert len(parts)==2
            app_name = parts[0]
            method_name = parts[1]
            app = getattr(device,app_name)
            method = getattr(app,method_name)
        else:
            # simple command
            method = getattr(device,command)
        method(*args,**kwargs)

        # def system_wrapper(*args,**kwargs):
        #     return method(*args,**kwargs)
        # return system_wrapper


    def _run(self,device_id,app_name,command,*args,**kwargs):
        """

            full interface to call a command on a device

            app is the name of an application (phone,mms ..)

        :param device_id:
        :param command:
        :return:
        """
        device = self.device(device_id)
        app = getattr(device,app_name)
        method = getattr(app,command)

        return method(*args,**kwargs)





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



    # high level function
    def quick_launch(self,device_id,index):
        """

        :param device_id:
        :param index:
        :return:
        """
        device = self.device(device_id)
        return self.device.sys.quick_launch(device_id,index)

    def home(self,device_id):
        """

        :param device_id:
        :return:
        """
        return self.device(device_id).press('home')