"""


    syp_plugin to interface syprunner




"""

import json

from droydrunner.uiconfig import UiConfiguration

from droydrunner.phone.interface import PhoneHub

#from droydrunner.phone.hub.api import NativeClient as PhoneHubNativeClient


syp_ptf= dict(

    # here comes the platform configuration
)


class Pilot(object):
    """
        syp_plugin to interface syprunner


    """
    _platform = syp_ptf
    #_dry = False

    def __init__(self,*args,**kwargs):
        """
            init pilot
        """
        self._result = ''
        self._users = {}
        self.conf = {}      # configuration of a platform version
        self.ptf = None     # ref to a UiConfiguration instance
        self._session = None
        self._dry = False

    def set_pilot_dry_mode(self):
        """
            set pilot to dry mode ( no action will be taken towards syprunner)
        """
        print "warning: you enter in dry mode"
        self._dry = True

    def setup_pilot(self,platform_name,platform_version,platform_configuration_file):
        """
            initialize pilot with platform configuration file
        """
        print "setting up platform pilot for platform=%s , version=%s" % (platform_name,platform_version)

        self.platform_name = platform_name
        self.platform_version = platform_version

        if isinstance(platform_configuration_file,dict):
            # set platform directly with dict
            self.platforms = platform_configuration_file
        else:
            # assume it is a filename , load it
            with open(platform_configuration_file,"rb") as fh:
                self.platforms = json.loads(fh.read())

        self.conf = self.platforms[platform_version]

        #self.ptf = SypPlatform(self.conf)
        self.ptf = UiConfiguration(self.conf)



    def _dry_return(self,*args,**kwargs):
        """
            return with dry mode : always OK
        """
        print "warning you are in dry mode, no operation was transmitted to droydrunner"
        self._result = "OK"
        return self._result

    def open_Session(self,*users):
        """
            open a session : start session with a terminal per user specified

            Open Session Alice Bob
                start a session with userA=Alice , userB=Bob
        """
        print "Pilot initialisation conf = %s " % str(self.conf)
        print "Open Session with users: %s" % str(users)
        self._userlist = users  # list of user roles eg ['Alice','Bob', 'Charlie']
        self._session = "dummy"
        if self._dry:
            return self._dry_return()


        # create a session with SypRelay
        #self._session= SypRelay()
        #self._session= DroydRelay(config=self.conf)

        #result = self._session= PhoneHubNativeClient(**self.conf['mobiles'])

        #self._session= PhoneHubNativeClient()
        phonehub_url = self.ptf.phone_hub
        self._session= PhoneHub(phonehub_url)

        result = self._session.open_session(**self.conf['mobiles'])

        # build a user confs from _userlist and platform config
        #users_conf=[self.ptf.user_profile(role) for role in self._userlist ]

        #users_conf = self._session.get_users_conf(*users)
        # open a session
        #result = self._session.open_session(users_conf)
        #print "open session result is %s" % str(result)
        if not result:
            raise Exception("registration Failed")


    def get_platform_configuration(self):
        """
            get platform configuration ( a plartform.json)
        """
        print "platform configuration is %s" % str(self.conf)
        return json.dumps(str(self.conf))

    def dummy_operation(self):
        """
            a dummy operation:  do nothing
        """
        print "dummy operation :platform configuration is %s" % str(self.conf)



    def close_session(self,result=0,error=0):
        """
            close session , unregister all users and quit
        """
        print "Close Session"
        self._users = {}

        if self._dry:
            self._session = None
            return self._dry_return()
        #
        try :
            self._session.close_session()
        except AttributeError:
            raise
            pass
        self._session=None


    ### HELPERS
    # def get_sip_address(self,user=None,format=None,fac=None):
    #     """
    #         compute a sip destination from user , format and eventualy fac
    #
    #         @fac +CFA      (*71)
    #         @user   Charlie
    #         @format sid_ext  (12 2515)
    #
    #         destination: sip:*71122515@sip.osp.com
    #
    #     """
    #     print "get_sip_address(user=%s,format=%s,fac=%s)" % (str(user),str(format),str(fac))
    #     destination = None
    #     try:
    #         # is user a destination instead
    #         self.ptf.destination(user)
    #         destination = user
    #         user = None
    #     except KeyError:
    #         # not a destination
    #         pass
    #
    #     result = self.ptf.resolve_address(user=user,destination=destination,format=format,fac=fac)
    #     return result



    ### primary interface with syprelay
    def _execute(self,user,command,*args,**kwargs):
        """
           the transmission belt with droyrunner plugin

           all calls to syprunner plugin should pass here
        """
        if not self._dry:
            return self._session.execute(user,command,*args,**kwargs)
        else:
            return self._dry_return()

    def _relay(self,command,*args,**kwargs):
        """
            relay a command to syprelay
        """
        if not self._dry:
            sip_relay_func = getattr(self._session,command)
            return sip_relay_func(*args,**kwargs)
        else:
            return self._dry_return()

    ###  base functions
    def _call(self,user,address):
        """
            @user: eg Alice Bob
            @sip_address
        """
        return self._session.call_number(user,address)


    def _answer_call(self,user,code=200,wait_incoming = False):
        """
            answer call , by default assumes a pending call is present, don t wait for it

            @user  eg Alice , bob ...
            @code : 180 , 200 ...


        """
        return self._session.answer_call(user)
        #return self._execute(user,"phone.answer_call",code=code, wait_incoming=wait_incoming)

    # def _check_call(self,user,state="CONFIRMED"):
    #     #
    #     return self._execute(user,"check_call",state=state)
    #
    # def _expect(self,user,pattern,raise_on_error=True,title="",ignore_timeout=False):
    #     return self._execute(user,'expect', pattern=pattern, raise_on_error=True, title="",ignore_timeout=False)


    # def unregister(self,user):
    #     """
    #         unregister a user
    #     """
    #     print "user %s unregister" % user
    #     return self._execute(user,'unregister')
    #
    # def wait_timed_out(self,user):
    #     """
    #         wait for a time out
    #     """
    #     print "user %s wait for time out" % user
    #     return self._execute(user,'wait_timed_out')
    #
    # def watch_log(self,user,duration=2):
    #     """
    #         just listen for a while to catch the log
    #     """
    #     clock = int(duration)
    #     print "user %s watch log for a duration of %d " % (user,clock)
    #     return self._execute(user,'watch_log',duration=clock)


    def wait_incoming_call(self,user):
        """
            wait an incoming call  (INVITE)
        """
        print "user %s wait for incoming call" % (user)
        return self._session.wait_incoming_call(user)


    # def wait_incoming_response(self,user,code,operation,cseq=''):
    #     """
    #         wait an incoming sip response  ( SIP/2.0 <code> for an operation
    #
    #         @code:str  , 200, 202 ...
    #         @operation: str  , INVITE , REGISTER ...
    #
    #     """
    #     print "user %s wait for a sip response of type %s  (%s)" % (user ,str(code), operation)
    #     return self._execute(user,'wait_incoming_response', code=code,operation=operation,cseq=cseq)
    #
    # def wait_incoming_request(self,user,operation,cseq=''):
    #     """
    #         wait an incoming sip request  ( INVITE , CANCEL )
    #
    #         @operation: str  , INVITE , REGISTER ...
    #
    #     """
    #     print "user %s wait for a sip request of type %s " % (user , operation)
    #     return self._execute(user,'wait_incoming_request', operation=operation,cseq=cseq)



    def hangup(self,user):
        """
            hangup a call
        """
        print "user %s hangup the call" % user
        return self._session.hangup(user)
        #return self._execute(user,"phone.end_call")

    # def wait_hangup(self,user):
    #     """
    #         wait for hangup
    #     """
    #     print "user %s wait for hangup" % user
    #     #
    #     return self._execute(user,"wait_hangup")

    # def sleep(self,seconds=1):
    #     """
    #         sleep n seconds
    #     """
    #     self._session.sleep(seconds)

    # def _check_not_received(self,user,pattern,refresh_count=2):
    #     """
    #         check user dont receive pattern
    #
    #     """
    #     return self._execute(user,'check_not_received',pattern=pattern,refresh_count=2)


    # def _transfer(self,user,address):
    #     """
    #         transfer a call to a sip adress
    #         @user: eg Alice
    #         @sip_address
    #     """
    #     return self._execute(user,"phone.transfer" , destination=address)
    #
    # def hold_call(self,user):
    #     """
    #         put call on hold
    #     """
    #     return self._execute(user,"phone.hold")
    #
    # def unhold_call(self,user):
    #     """
    #         cancel call on hold
    #     """
    #     return self._execute(user,"phone.unhold")

    # def start_player(self,user):
    #     """
    #         start playing file
    #     """
    #     return self._execute(user,"start_player")
    #
    # def stop_player(self,user):
    #     """
    #         stop playing file
    #     """
    #     return self._execute(user,"stop_player")

    # def dump_call_quality_status(self,user):
    #     """
    #         ask the terminal to dump the media status of the call in log
    #
    #     """
    #     media_log = self._execute(user,'dump_call_quality_status')
    #     return media_log



    #
    # high level functions
    #

    # def wait_sip_response(self,user , code):
    #     """
    #         wait for a sip response of type  'SIP/2.0 <code>'
    #
    #         DEPRECATED
    #          use wait_incoming_response instead
    #     """
    #     #TODO: replace this (this version catch the first SIP/2.0 response which can be from an other sequence)
    #     expected = "SIP/2.0 %s" % str(code)
    #     print "user %s wait for a sip response of type %s  (%s)" % (user ,str(code), expected)
    #     return self._expect(user, pattern=expected, raise_on_error=True, title="", ignore_timeout=False)
    #
    #
    # def call_feature_access_code(self,user,call_feature_access_code,userX=None,format=None):
    #     """
    #         call Application server with a simple access code
    #         eg  -CFA , -CFU
    #     """
    #     sip_address=self.get_sip_address(user=userX,format=format,fac=call_feature_access_code)
    #
    #     print "user %s calls AS with Feature Access code  (%s)" % (user, sip_address)
    #     #fac = self.ptf.fac(call_feature_access_code)
    #     #sip_address= self.ptf.sip_address_for(fac)
    #     return self._call(user,sip_address)


    def call_number(self,user,destination):
        """
            call an arbitrary number or sip address
            @user: eg Alice , Bob
            @destination:  sip address or number

            WARNING:  using literal sip address in test may make your Test non portable"

            use 'Call User' or 'Call Destination' instead
        """
        print "user %s call destination %s" % (user,destination)
        print "WARNING:  using literal sip address in test may make your Test non portable "
        return self._call(user,address=destination)


    def call_destination(self,user,destination):
        """
            call a predefined destination (defined in platform.json)

            @user: eg Alice , Bob
            @destination:  the literal name of a destination defined in platform conf
        """
        # retrieve destination from configuration
        resolved_destination= self.ptf.destination(destination)
        address= self.ptf.sip_address_for(resolved_destination)
        print "user %s call destination %s  (%s)" % (user,destination,address)
        #
        return self._call(user,address=address)


    def call_user(self,userA,userX,format="universal"):
        """
             userA call userX with format (universal,national ...)
        """
        # compute sip address for userX with format
        #agent = self._session._agent_by_role[userX]
        #serial = agent.serial

        target_info = self.ptf.get_phone_config(userX)
        number = target_info.get_property('tel')
        print  "user %s call user %s at %s" % ( userA, userX, number)

        #sip_address = self.ptf.user(userX).sip_address_to_user(format)
        #print  "user %s call user %s with format %s  (%s)" % ( userA, userX, format ,sip_address)
        return self._call(userA,address=number)

    # def call_sd(self,user,sd):
    #     """
    #          userA call with direct sd8 key sd ( 1..8 )
    #     """
    #     target_user = self.ptf.sd8(user,sd)
    #     sip_address= self.ptf.sip_address_for(sd)
    #     print "user %s call direct sd8 key %s  (%s)" % (user,sd,sip_address)
    #     #
    #     return self._call(user,sip_address=sip_address)

    # def transfer_to_user(self,userA,userX,format="universal"):
    #     """
    #         unatented transfer call
    #         userA transfer call userX with format (universal,national ...)
    #     """
    #     # compute sip address for userX with format
    #     sip_address = self.ptf.user(userX).sip_address_to_user(format)
    #     print  "user %s transfer call to user %s with format %s  (%s)" % ( userA, userX, format ,sip_address)
    #     return self._transfer(userA,address=sip_address)
    #
    # def transfer_to_destination(self,user,destination):
    #     """
    #         transfer call (unatended) to a predefined destination (defined in platform.json)
    #
    #         @user: eg Alice , Bob
    #         @destination:  the literal name of a destination defined in platform conf
    #     """
    #     # retrieve destination from configuration
    #     resolved_destination= self.ptf.destination(destination)
    #     #sip_address= self.ptf.sip_address_for(resolved_destination)
    #     print "user %s transfer call to destination %s  (%s)" % (user,destination,resolved_destination)
    #     #
    #     return self._transfer(user,address=resolved_destination)
    #     #return self._call(user,sip_address=sip_address)
    #
    #
    # def transfer_attended(self,user,call_indice=0):
    #     """
    #         attented transfer call
    #         userA transfer current call to previously established call number 'call indice' eg 0
    #     """
    #     print  "user %s transfer current call to previously established call %s" % ( user, str(call_indice))
    #     return self._execute(user,"transfer_attended" , call_indice = str(call_indice))
    #
    #
    # def wait_incoming_call_and_answer_ok(self,user):
    #     """
    #         wait for an incoming call and send OK
    #     """
    #     return self.wait_incoming_call(user)
    #     #return self.answer_call_ok(user)


    def answer_call(self,user,code=200):
        """
            answer a pending call with code

            warning: check there is a pending call using 'Wait Incoming Call'
        """
        print "user %s answer call" % ( user )
        return self._answer_call(user,code=code,wait_incoming=False)

    # def answer_call_ringing(self,user):
    #     """
    #        answer a pending call with code 180 (ringing)
    #
    #         warning: check there is a pending call using 'Wait Incoming Call'
    #     """
    #     print "user %s sends 180 ringing" %  user
    #     return self._answer_call(user,code=180,wait_incoming=False)
    #
    # def answer_call_ok(self,user):
    #     """
    #        answer a pending call with code 200 (OK)
    #
    #         warning: check there is a pending call using 'Wait Incoming Call'
    #     """
    #     print "user %s sends 200 OK" %  user
    #     return self._answer_call(user,code=200,wait_incoming=False)
    #
    #
    # def wait_ringing(self,user):
    #     """
    #         wait for sip response  'SIP/2.0 180)
    #     """
    #     print "user %s wait for ringing" %  user
    #     return self.wait_sip_response(user,180)

    # def wait_call_confirmed(self,user):
    #     """
    #         wait for call to be confirmed
    #     """
    #     print "user %s wait for call to be confirmed" % user
    #     return self._check_call(user,state="CONFIRMED")
    #
    # def wait_call_disconnected(self,user):
    #     """
    #         wait for call to be dictonnected
    #     """
    #     print "user %s wait for call to be confirmed" % user
    #     #
    #     return self._check_call(user,state="DISCONNECTED")



    def bad_call(self):
        """
            a dummy function to get a failed call
        """
        self._result = "KO"
        return self._result

    # def activate_redirection_to_user(self,userA,userB,redirect_kind,call_format):
    #     """
    #         call Application Server using a Feature Access Code to redirect userA to userB
    #
    #         @userA : the user to be redirected
    #         @userB : target of the redirection
    #         @redirect_kind: CFA,CFB,CFNA,CFNR  (Always,Busy,NotAnswered,NotReachable)
    #         @call_format: site,national,international,universal
    #
    #     """
    #     fac_name = "+" + redirect_kind
    #     fac_code = self.ptf.fac(fac_name)
    #     destination = self.ptf.sip_address_for( fac_code + self.ptf.user(userB).to_user(format_=call_format))
    #     print "user %s ask a call forward via feature access code %s to user %s with format %s (%s) " % (
    #         userA,redirect_kind,userB,call_format,destination)
    #     # place the call
    #     return self._call(userA,sip_address=destination)


    # def cancel_redirection(self,user,redirect_kind):
    #     """
    #         @userA : the user to be redirected
    #         @redirect_kind: CFA,CFB,CFNA,CFNR  (Always,Busy,NotAnswered,NotReachable)
    #     """
    #     fac_name = "-" + redirect_kind
    #     fac_code = self.ptf.fac(fac_name)
    #     destination = self.ptf.sip_address_for(fac_code)
    #     print "call AS to cancel a redirection of type %s for user %s (%s)" %(redirect_kind,user,destination)
    #     # place the call
    #     return self._call(user,sip_address=destination)


    # def check_no_incoming_call_received(self,user):
    #     """
    #         check user dont receive an incoming call
    #
    #     """
    #     self._check_not_received(user,pattern=">*> Incoming call",refresh_count=2)



    #
    # functions using siprelay directly
    #
    # def  check_call_quality(self, user,min_packets= 100 , max_loss_rate = 0.1, channel = 'TX',slot = '0' , call=None):
    #     """
    #         analyse last dump media status
    #     """
    #     validation_func =  SypRelay.check_loss_rate(min_packets,max_loss_rate)
    #     return self._relay('check_media',role=user,channel=channel,slot=slot,call=call,validation = validation_func)

    # def check_incoming_call(self,user,from_user=None,checks="display"):
    #     """
    #         perform checks on last incoming call received ( INVITE message)
    #
    #         @user: str , the user receiving the call (eg Bob)
    #         @from_user: str , the user from we wait the call
    #         @checks:str , comma separated tags : the kind of check to perform ( "display,number"  )
    #
    #             if from_user is an account: (eg Alice )
    #                 check this call is coming from this user
    #                     if display in checks: check display_name ( CLIP Call Line Identity Pressentation
    #                     if number in checks: checks number       ( CNIP Call Number Identity presentation
    #             if from_user is 'unkwown' :
    #                 we check the identity restrictions
    #                    if display in checks : check display is unkwown  ( CLIR call line Identity Restriction )
    #                    if number in checks : check number is Unkwon     ( CNIR Call NumberIdentity Restriction
    #
    #
    #     """
    #     display_name=None
    #     if from_user:
    #         try:
    #             display_name = self.ptf.user(from_user).user_display
    #         except KeyError:
    #             # not an account
    #             if from_user == 'unkwown':
    #                 display_name = 'unkwown'
    #             else:
    #                 raise ValueError('Not a  valid from_user account: %s' % from_user)
    #     # perform the check
    #     validation = SypRelay.check_caller(user,display_name)
    #     r = self._relay('check_incoming_call',user,validation)
    #     return r

__author__ = 'cocoon'
