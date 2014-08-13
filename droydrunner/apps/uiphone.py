__author__ = 'cocoon'


import time

from droydrunner.uiapplication import UiApplication

from droydrunner.uiscreen import UiScreen, UiTab



class Application(UiApplication):
    """

        phone application


        screens:
            contacts:
                tabs
                    keyboard


    """
    name = 'uiphone'
    package_name = "com.android.contacts"



    def setup(self):

        # init call state ( IDLE , CALLING , INCOMING , INCALL)
        self._call_state = 'IDLE'

        # register contacts screen
        self.contacts = ContactScreen(self)

        self.incallui = InCallUiScreen(self)

        self.incoming = IncomingCallScreen(self)



    def open(self):
        """
            launch the phone application and select keypad tab
        :return:
        """
        # launch the phone application
        self.uidevice.quick_launch('Phone')
        # select keypad
        self.contacts.select_tab('keypad')

    def close(self):
        if self._call_state == 'CALLING' or self._call_state == 'INCALL':
            if self.incallui.end_call.exists:
                self.incallui.end_call.click()
        self._call_state = 'IDLE'

        self.uidevice.press('home')
        return



    def enter_destination(self,destination):
        """
        """
        tab =self.contacts.keyboard

        tab.selector('digits').long_click()
        tab.selector('deleteButton').click()
        tab.selector('digits').set_text(destination)
        return


    # high level function
    def call_destination(self,destination):
        """
        """
        tab = self.contacts.keyboard

        # dial number
        self.enter_destination(destination)

        # press call button
        tab.dialButton.click()

        self._call_state = 'CALLING'
        return

        # # click number
        # for digit in destination:
        #     tab.selector(digit).click()
        # # press call button
        # tab.selector('callButton').click()


    def end_call(self):
        """
            end a call ( when in incallui screen )
        """
        if self.incallui.check():
            self._call_state = 'IDLE'
            return self.incallui.end_call.click()
        raise RuntimeError('cant end call : not in incallui screen')


    # receiving calls

    def is_incoming_call(self):
        """
            lazy screen of incoming call popup
        :return:
        """
        try:
            return self._incoming_call_popup.check()
        except AttributeError:
            self._incoming_call_popup = IncomingCallPopup(self)
        return self._incoming_call_popup.check()

    def wait_incoming_call(self,timeout=10 , check_number=None , check_caller=None):
        """

        :param timeout:
        :return: string : number of the caller
        """
        caller = None
        for i in xrange(timeout):
            print "trying to detect incoming call ..."
            time.sleep(1)
            if self.is_incoming_call():
                print "incoming call popup screen detected"
                self._call_state = 'INCOMING'
                caller = self._incoming_call_popup.selector('popup_caller_number_or_location').info
                #caller= self.device( resourceId = 'com.android.incallui:id/popup_caller_number_or_location').info
                print "popup: caller is %s" % caller['text']
                return caller['text']

        # timeout
        raise RuntimeError("Timeout on waiting for a call")


    def reject_call(self):
        """
            reject an incoming call
        """
        button = self._incoming_call_popup.selector('Reject')
        print "rejecting call"
        button.click()
        self._call_state = 'IDLE'
        print "rejected with success"
        self.device.wait.update()
        return

    def answer_call(self,code=None,wait_incoming=None):
        """
            answer an incoming call

            code and wait_incoming are not used ( compatibility mode with syprunner )
            "phone.answer_call",code=code, wait_incoming=wait_incoming

        """
        button = self._incoming_call_popup.selector('Answer')
        print "answering call"
        button.click()
        self._call_state='INCALL'
        print "answers with success"
        self.device.wait.update()
        return



class ContactScreen(UiScreen):
    """

    """
    package_name = 'com.android.contacts'

    def setup(self):
        """

        """
        self.keyboard= ContactKeyboard(self)
        #self.contacts=
        #self.logs=


    def select_tab(self,tab_name):
        """
            return the selector of one the tab of the contacts screen ( keyboard ,  logs, favorites contacts

            resource Idandroid.app.ActionBar$Tab

        """
        _tabs = ['KEYPAD','LOGS','FAVORITES','CONTACTS']
        index = str(_tabs.index(tab_name.upper()))
        return self.device(className='android.app.ActionBar$Tab',packageName=self.package_name,index=index).click()





class ContactKeyboard(UiTab):
    """
        the keyboard tab screen of phone application

    """

    keys = ('zero','one','two','three','four','five','six','seven','height','nine')
    resource_key = "com.android.contacts:id/%s"

    #resource_enter = "com.android.contacts:id/callbutton"
    # com.android.contacts:id/star
    # com.android.contacts:id/pound
    # com.android.contacts:id/videocallbutton
    # com.android.contacts:id/deleteButton
    #resource_text =  "com.android.contacts:id/digits"

    def key_id(self,digit):
        """
            return resourceId for a keyboard digit
        """
        key_name = self.keys[int(digit)]
        return self.resource_key % key_name


    def setup(self):
        """

        :return:
        """

    def selector(self,name):
        """

        :param name:
        :return:
        """
        if name in ['1','2','3','4','5','6','7','8','9','0']:
            return self.device(resourceId = self.key_id(name))
        else:
            # name is in  : star  pound, callButton ,digits, deleteButton,videocallButton
            return self.device(resourceId = self.resource_key % name)


    @property
    def dialButton(self):
        """
            :return callButton selector

        """
        names = ['dialButton','callButton']
        for name in names:
            if (self.device(resourceId = self.resource_key % name)).exists:
                return self.device(resourceId = self.resource_key % name)
        raise RuntimeError('cant find call button')


    def digitButton(self,digit):
        """
            return the digit button
        """
        return self.device(resourceId = self.key_id(digit))



class IncomingCallPopup(UiScreen):
    """
        the popup of inncoming call

    """
    package_name = "com.android.incallui"

    elements= {
        'popup_call_state',
        'popup_caller_image',
        'popup_caller_name',
        'popup_caller_number_or_location',
        'popup_call_fullscreen',
        'popup_call_answer',
        'popup_call_answerViaSpeaker',
        'popup_call_reject',
    }

    def selector(self,name):
        """
            resourceId: com.android.incallui:id/$element

        :param name:
        :return:
        """
        if name in self.elements:
            # element accesible by resource id
            return self.device(resourceId="%s:id/%s" % (self.package_name,name))
        # high level selectors
        elif name == 'Answer':
            return self.selector('popup_call_answer')
        elif name == 'Reject':
            return self.selector('popup_call_reject')
        else:
            raise ValueError('IncomingCallPopup: invalid selector: % s' % name)


    def check(self):
        """
            check if this screen is present ( an incoming call screen )
        :return:
        """
        return self.selector('popup_call_state').exists



class IncomingCallScreen(UiScreen):
    """
        screen shown when receive an incoming call
    """
    package_name = "com.android.incallui"


    elements = [
        'caller_info_card_scroll_view'
        'callStateLabel',
        'name',
        'phoneNumber',
        'reject_call_with_message_handle',

        ]

       #'com.android.incallui:id/handleImageView' , # content-desc = 'Swipe right to answer call.'
        #'com.android.incallui:id/handleImageView'   # content-desc = Swipe left to reject call.

    def selector(self,name):
        """


            resourceId: com.android.incallui:id/$element

        :param name:
        :return:
        """
        if name in self.elements:
            # element accesible by resource id
            return self.device(resourceId="%s:id/%s" % (self.package_name,name))
        elif name in ['answer','reject']:
            # name or reject selector
            sel = self.device( resourceId= "com.android.incallui:id/handleImageView" , index=5)
            return sel
            #return self.device(resourceId="%s:id/handleImageView" % self.package_name , descriptionContains= name)
        else:
            raise ValueError('IncomingCallScreen: invalid selector: % s' % name)




    def check(self):
        """

            check if this screen is present ( an incoming call screen )

        :return:
        """
        current = self.uidevice.current_package_name()
        if current == self.package_name:
            if self.selector('reject_call_with_message_handle'):
                return True
        return False


    def answer_call(self,number=None):
        """

        :param number:
        :return:
        """
        button = self.selector('answer')
        return button.click()


    def reject_call(self,number=None):
        """

        :param number:
        :return:
        """
        button = self.selector('reject')
        return button.click()



class InCallUiScreen(UiScreen):
    """
        the screen we get after dialing a number , waiting for answer

    """
    package_name = "com.android.incallui"

    elements = [
        'caller_info_card_scroll_view',
        'callStateLabel',
        'name',
        'phoneNumber',
        'addCallButton',
        'dialpadButton',
        'endButton',
        'speakerButton'
        'muteButton',
        'bluetoothButton'
    ]


    def selector(self,name):
        """


            resourceId: com.android.incallui:id/$element

        :param name:
        :return:
        """
        assert name in self.elements
        return self.device(resourceId="%s:id/%s" % (self.package_name,name))


    def check(self):
        """

            check if this screen is present

        :return:
        """
        current = self.uidevice.current_package_name()
        if current == self.package_name:
            return True
        else:
            return False

    @property
    def end_call(self):
        """

        :return: endcall button selector
        """

        return self.selector('endButton')