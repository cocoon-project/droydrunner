"""

    DroyRelay is a driver for one or more  android device


    it is the entry point for robot framework plugin


"""


import os
import time
import imp
import sys




#from syplog import out
#from sypagent import SypAgent


#from syprunner.syprfc.sip_parser import Message


from droydrunner.uihub import UiHub
from droydrunner.uiconfig import UiConfiguration






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




class DroydRelay():
    """
        Droyd relay


        a relay between external robot to device if the session





    """
    title = ""



    def __init__(self,config = {}, log_cb=None  ):
        """
            @config

            @log_cb: function : output function  def log_cb(self,msg,nl=True)
                by default take the out()function of this module

        """


        if log_cb is None:
            # no gven log callbck use the module default out() function
            self.out = out
        else:
            # use the given callback for output
            self.out=log_cb


        self.config = config
        self.configurator = UiConfiguration(config)
        self.hub = UiHub(self.configurator)


        self.setup()

    def setup(self):
        """

        """

        self.platform=None

        self.test_name=   'test' # self.config.get('test','test')
        self.step_name=    'step' #self.config.get('name','step')
        self.title=  "%s/%s" % (self.test_name, self.step_name)

        self.log("START STEP: %s " % self.title)


        self.agents={}

        self.need_stdout_buffer=False

        #self.setup_agents()


    def open_session(self,users_conf):
        """


        """
        return self.setup_agents(users_conf)


    def close_session(self,result=0,error=0):
        """

        """
        #if result == 0:
        time.sleep(1)
        self.shutdown()

        if result == 0:
            self.log( "<*> Test " + self.title + " completed successfully")
        else:
            self.log("<*> Test " + self.title + " completed with errors " + str(error) )



        return result



    def setup_agents(self,users_conf,register=True):
        """

        :param users_conf: array if dict { alias, serial

        """
        result=True

        self._agent_by_role = {}  # index of agents by roles ( role= Alice, Bob ..)


        # common parameters for all agents ( codecs , play file
        params = {}


        # for each agent
        indices="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for indice in xrange(0,len(users_conf)):


            # # build user conf
            # user_conf= {}
            # for key,value in users_conf[indice].iteritems():
            #     if key in ['username','display','domain','password','proxy','registrar','profile']:
            #         user_conf[key]=value
            #
            # agent_name = "user%s" % indices[indice]
            # #role  = user_conf['display']
            # role = users_conf[indice]['allias']
            # # use allias for display
            # user_conf['display'] = role  # ALice instead of 'Alice Alice'

            alias = users_conf[indice]['alias']
            serial = users_conf[indice]['device_id']

            agent_name = "user%s" % indices[indice]

            # create and launch agent
            self.log("Start Agent: %s with role: %s" % (agent_name,alias))


            # create an agent
            agent = self.hub.add_device(alias=alias ,serial=users_conf[indice]['device_id'],applications=None)

            # update internal indexes
            self.agents[agent_name]= agent
            self._agent_by_role[alias] = agent


            # open phone app
            self.log("open phone for user %s" % agent_name)
            self.execute(alias,'phone.open')

        # if result:
        #     self.log("registration phase PASS")
        # else:
        #     self.log("registration phase FAIL")
        #
        return result


    def get_users_conf(self,*userlist):
        """
            return an array of

        :return:
        """
        users_conf=[]
        # request all mobile phones
        users = self.configurator.find_device()


        #serials = sorted(hub.config.data['phones'].keys())

        for index,alias in enumerate(userlist):

            user= users[index]
            conf = { 'device_id': user.device_id, 'alias': alias }
            conf.update(user.data)

            users_conf.append(conf)
        return users_conf


            # serial = serials[index]
            # content =  hub.config.data['phones'][serial]
            # value = content.copy()
            # value['device_id'] = serial
            # value['alias']= alias
            # users_conf.append(value)



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


    def sleep(self,seconds):
        self.log("sleep(%s)" % str(seconds))
        time.sleep(seconds)

    def get_users(self):
        """
            get user agent in alphabetical order : userA , userB ...


            usage in script: userA,userB , userC = pilot.get_users()

            return a SypAgent instance

        """
        agents=[]
        for agent_name in sorted(self.agents.keys()):
            agents.append(self.agents[agent_name])
        if len(agents) == 1 :
            # if single user , return user instead of list
            agents = agents[0]
        return agents

    def user_list(self):
        """
            return user roles , of the session eg [ Alice, Bob ..]
        """
        raise NotImplementedError


    def log(self,msg):
        """

        """
        self.out("pilot: %s" %  msg)


    # main interface with agents
    def execute(self,role,command,**kwargs):
        """
            execute the command on the specified agent

            main interface to different sipagents

            @role:  eg  Alice, bob , Charlie
            command:   the SypAgent command , call , answer_call  ...

        """
        agent = self._agent_by_role[role]

        # find the method
        try:
            parts = command.split('.')

            if len(parts)==2:
                # application + command   eg phone.open
                application = getattr(agent,parts[0])
                method = getattr(application,parts[1])
            else:
                assert len(parts) == 1
                method = getattr(agent,command)
        except:
            raise

        # run the method
        try:
            res  = method(**kwargs)
        except:
            raise
        return res

    #
    # high level functions
    #
    def catch_incoming_call(self,role,code,operation,cseq='',validation=None):
        """
            high level wait_incoming call :
                return the parsed INVITE message if validation function is None
                return result of evaluation if validation is not None

        """
        self.execute(role,'wait_incoming_call',code=code,operation=operation,cseq=cseq)
        validated = self.check_incoming_call(role,validation)
        return validated



    # checks on incoming calls
    def check_incoming_call(self,role,validation):
        """


        """
        raise NotImplementedError

    @classmethod
    def check_caller(cls,user, display=None , number=None):
        """
            check call is emitted by the given user

            @user: str, the agent: Alice, Bob ,
            @display: str the display name of the caller (eg "Alice Alice")
            @number: str : the number of the caller

        """
        def validate(call):
            """

                @call: a sip INVITE object (a syprfc.Message instance)

                getting the From:Header
                    from_header= call['from']

                available attributes:
                    from_header.tag
                    from_header.value.uri.user
                    from_header.value.uri.host
                    from_header.value.displayable  # warning length limited to a 25 eg : 'Q11A-EasyValid Q11A-Ea...'

                    from_header.value.displayName


            """
            from_header= call['from']
            if display:
                # check display name
                received = from_header.value.displayName
                if not received == display:
                    # display name check has failed
                    raise ValueError('bad display name, expected:%s , received: %s' %(display,received))
            if number:
                raise NotImplementedError('check number not implemented yet')
            return True

        return validate


    # def agent_by_role(self,alias):
    #     """
    #
    #     :param alias:
    #     :return:
    #     """
    #     return self._agent_by_role[alias]