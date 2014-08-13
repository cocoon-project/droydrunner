__author__ = 'cocoon'


import time

import json

from uihub import UiHub
from uidevice import UiDevice
from uiapplication import UiApplication
from uihub import UiHub
from uihub import UiHubSession
from uiconfig import UiConfiguration

from uiconfig import ConfigStore

#from robot_relay import DroydRelay
from robot_plugin import Pilot




known_packages = {

    'android':                       'deverouillage pin ',
    'com.sec.android.app.launcher' : 'ecran d accueil home' ,

    'com.android.contacts' : ' phone application',

}


config = {

  "platform_version": {

    "mobiles" : {

        "388897e5" : {  "name": "Caller" , "pin": None , "sim": "0000", "tel":"0640412593"  },

        "e7f54be6":  {  "name": "Calee" , "pin": None , "sim": "0000", "tel":"0684820364"},

        #"4df18692171e5fed": {  "name": "GT-I9300" ,"pin": "325698", "sim":None , "tel": ""},

        }
    }
}

def test_uiconfig():
    """

    """

    cnf = UiConfiguration(config['platform_version'])

    my = cnf.get_phone_config('388897e5')

    assert my.pin_code == None
    assert my.sim_code == '0000'

    phones = cnf.find_device()


    return


def test_uiconfig_json():
    """

    """
    filename = '../platform.json'

    cnf = UiConfiguration.from_json(filename,platform_version='mobile_qualif')

    my = cnf.get_phone_config('388897e5')

    assert not my.pin_code
    assert my.sim_code == '0000'

    return



def test_UiHub():
    """

    """
    hub = UiHub()

    devices = hub.device_list()
    print devices

    return


def test_UiApplication():
    """

    """
    alice = UiDevice()
    my_app = UiApplication(alice)

    return


def test_UiDevice_myphone():
    """

    """

    # my phone
    alice = UiDevice('alice',serial='4df18692171e5fed')
    alice.setup()

    print alice.current_package_name()

    print alice.current_package_name()


    alice.sys.goto_home()


    return

def test_UiDevice():
    """

    """

    # my phone
    alice = UiDevice('caller',serial='388897e5')
    alice.setup()

    print alice.current_package_name()

    print alice.current_package_name()


    alice.device.press('home')

    alice.press('home')
    # click on hotkey Phone
    alice.select_choice('com.sec.android.app.launcher:id/layout',0,'0').click()
    # select keypad
    alice.select_choice('android:id/action_bar_container',0,"0/0").click()
    # click on option menu
    alice.select_choice('android:id/action_bar_container',0,"1/2").click()


    return


def test_caller():
    """

    """
        # my phone
    alice = UiDevice('caller',serial='388897e5')
    alice.setup()


    # unlock screen if necessary
    alice.sys.unlock()

    # alice.device.screen.on()
    # alice.device.wakeup()
    #
    # current = alice.current_package_name()
    # print current
    # if current == "com.android.keyguard":
    #     # lock screen
    #     #alice.device.swipe(100,100,300,500,steps=100)
    #     alice.device.swipe(270,1440,800,1000,steps=50)
    #     current = alice.current_package_name()
    #     print current
    #     if current == "com.android.keyguard":
    #         raise RuntimeError('Cant unlock device')
    # #com.sec.android.app.launcher

    #alice.device.press('home')

    # goto Phone application
    alice.sys.goto('uiphone')


    #get phone handler
    alice_phone_app = alice.phone

    alice_phone_app.select_keyboard_tab()

    #alice_phone_app.enter_destination('0681564613')
    alice_phone_app.call_destination('0681564613')

    #xml = alice.device.dump()
    #print xml

    print alice_phone_app.incallui.check()

    print alice_phone_app.incallui.check()


    alice_phone_app.end_call()



    return



def test_callee():
    """

    """
        # my phone
    bob = UiDevice('callee',serial='388897e5')
    bob.setup()


    # unlock screen if necessary
    bob.sys.unlock()

    bob.device.press('home')


    #get phone handler
    bob_phone_app = bob.phone



    #answer_button = bob.phone.incoming.selector('answer').exists


    #button = bob.device(resourceId='com.android.incallui:id/handleImageView' , text="Swipe right to answer call.")
    button = bob.device( resourceId = 'com.android.incallui:id/handleImageView' , instance='0')
    if button.exists:
        print 'button exists'
        #button.swipe.right()
        button.click()
    else:
        print "button not found"
        xml = bob.device.dump()
        print xml

    # # wait for incoming call here
    # print bob.phone.incoming.selector('answer').exists
    #
    # answer_button = bob.phone.incoming.selector('answer')
    #
    # print answer_button
    #
    # # answer_button = bob.device(text='Answer').exists
    # # print answer_button
    # # answer_button = bob.device(text='Answer')
    # # #caller = bob.device(resourceId='com.android.incallui:id/popup_caller_name')
    # # #print caller.get_text()
    #
    #
    # answer_button.click()


        # reject the call
    #bob_phone_app.reject_call()

    #xml = bob.device.dump()
    #print xml




    # reject call




    return


def test_watchers():
    """


    """
    bob = UiDevice('callee',serial='388897e5')
    bob.setup()

    print "sdk_version: %s" % str(bob.sdk_version)

    # unlock screen if necessary
    bob.sys.unlock()

    bob.device.press('home')

    # # create watcher
    # bob.device.watcher('reject_call').when(resourceId = 'com.android.incallui:id/reject_call_with_message_handle' ).click(resourceId = 'com.android.incallui:id/reject_call_with_message_handle' )
    #
    # if bob.device.watcher('reject_call').triggered:
    #     print "answer call was triggered"
    # else:
    #     print "answer call watcher has failed"


    # enter phone app
    phone = bob.device(text='Phone',instance=0)
    if phone.exists:
        phone.click()
    bob.device.press('home')




    # bob.device.watcher('enter_phone').when(text = 'Phone' ).click(text='Phone')
    #
    # if bob.device.watcher('enter_phone').triggered:
    #     print "enter_phone was triggered"
    # else:
    #     print "enter_phone has failed"


    #xml = bob.device.dump()
    #print xml

    # register watcher
    #bob.device.watcher('answer_call').when(resourceId = 'com.android.incallui:id/handleImageView' , index=5).press('home')

    #click(resourceId = 'com.android.incallui:id/handleImageView' , index="5")

    # click answer

    bob.device.open.notification()
    bob.device.press('home')

    bob.device.open.quick_settings()
    bob.device.press('home')


    state=bob.device(resourceId='com.android.incallui:id/callStateLabel').get_text()
    print state


    #to try press('KEYCODE_ENDCALL','DOWN_AND_UP')

    bob.device(resourceId = 'com.android.incallui:id/handleImageView' , index=5).click()
    #bob.device(resourceId = 'com.android.incallui:id/handleImageView' , instance='1').swipe.right()


    # if bob.device.watcher('answer_call').triggered:
    #     print "answer call was triggered"
    # else:
    #     print "answer call watcher has failed"

    return



def test_Two_phones():
    """
    """
    raise NotImplementedError('not working')

    # cnf = UiConfiguration(config)
    #
    #
    # #alice_cnf = cnf.get_phone_config('e7f54be6')
    # #bob_cnf   = cnf.get_phone_config('388897e5')
    #
    # alice_cnf = cnf.get_phone_config('388897e5')
    # bob_cnf   = cnf.get_phone_config('e7f54be6')
    #
    #
    # # init caller
    # print "init alice ..."
    # alice = UiDevice('callee',serial= alice_cnf.device_id)
    # alice.setup()
    #
    # print "alice sdk_version: %s" % str(alice.sdk_version)
    #
    # # unlock screen if necessary
    # alice.sys.unlock()
    #
    # alice.device.press('home')
    #
    #
    # # init callee
    # print "init bob ..."
    # bob = UiDevice('callee',serial= bob_cnf.device_id)
    # bob.setup()
    #
    # print "bob sdk_version: %s" % str(bob.sdk_version)
    #
    # # unlock screen if necessary
    # bob.sys.unlock()
    #
    # bob.device.press('home')
    #
    #
    # # goto Phone application
    # alice.sys.goto('uiphone')
    # # goto keyborad
    # alice.phone.contacts.select_tab('keypad')
    # # dial number
    # print "alice: calling bob"
    # alice.phone.call_destination(bob_cnf.tel)
    #
    # # ANSWER CALL
    # bob.sys.goto('uiphone')
    # alice.phone.contacts.select_tab('keypad')
    # answer_button = bob.device(text='Answer')
    #
    # found = False
    # for i in xrange(3):
    #     print "bob: trying to detect incoming call ..."
    #     if answer_button.exists:
    #         found = True
    #         print "incoming call screen detected on bob"
    #         caller= bob.device( resourceId = 'com.android.incallui:id/popup_caller_number_or_location').info
    #         print "bob: popup: caller is %s" % caller['text']
    #         #xml = bob.device.dump()
    #         #print xml
    #         break
    #     time.sleep(4)
    #
    # #button_info = None
    # if not found:
    #     print "non incoming screen detected on bob device"
    # else:
    #
    #     # incoming popup
    #     try:
    #
    #         #print "getting button info"
    #         #button_info = answer_button.info
    #         print "bob is answering call"
    #         answer_button.click()
    #         print "bod answers with success"
    #         bob.device.wait.update()
    #         #print "dump ui"
    #         #xml = bob.device.dump()
    #         #print xml
    #
    #         caller = bob.device(resourceId = "com.android.incallui:id/phoneNumber").info
    #         print "bob: caller is %s" % caller['text']
    #         time.sleep(5)
    #     except Exception,e:
    #         print "bob failed to answer"
    #         raise e
    #     finally:
    #         print "alice hangup"
    #         alice.device.wakeup()
    #         alice.phone.end_call()
    #     print "end of call"
    # #print "button info is: %s" % button_info
    #
    #
    # time.sleep(1)



def test_simple_call():
    """
    """

    cnf = UiConfiguration(config)


    #alice_cnf = cnf.get_phone_config('e7f54be6')
    #bob_cnf   = cnf.get_phone_config('388897e5')

    alice_cnf = cnf.get_phone_config('388897e5')
    bob_cnf   = cnf.get_phone_config('e7f54be6')


    # init caller
    print "init alice ..."
    alice = UiDevice('callee',serial= alice_cnf.device_id)
    print "alice sdk_version: %s" % str(alice.sdk_version)


    alice.device.press('home')


    # init callee
    print "init bob ..."
    bob = UiDevice('callee',serial= bob_cnf.device_id)
    print "bob sdk_version: %s" % str(bob.sdk_version)

    # unlock screen if necessary


    # goto Phone application
    alice.sys.goto('uiphone')
    # goto keyborad
    alice.phone.contacts.select_tab('keypad')
    # dial number
    print "alice: calling bob"
    alice.phone.call_destination(bob_cnf.tel)

    # ANSWER CALL
    bob.sys.goto('uiphone')
    bob.phone.contacts.select_tab('keypad')

    # bob wait for incoming call
    caller =None
    try:
        caller = bob.phone.wait_incoming_call()
        print "bob: popup: incoming call from %s" % caller
    except Exception, e:
        # no incoming call
        print "incoming call not received"
        raise e

    if caller:
         # pendant incoming call
        try:
            bob.phone.answer_call()
            "print call established"
            time.sleep(5)
        except Exception,e:
            print  "cant answer call"

        finally:
            print "alice hangup"
            alice.device.wakeup()
            alice.phone.end_call()
            print "end of call"


    return




def test_contacts_screen():
    """


    """
    cnf = UiConfiguration(config)


    #alice_cnf = cnf.get_phone_config('e7f54be6')
    #bob_cnf   = cnf.get_phone_config('388897e5')

    alice_cnf = cnf.get_phone_config('388897e5')
    #bob_cnf   = cnf.get_phone_config('e7f54be6')


    # init caller
    print "init alice ..."
    alice = UiDevice('callee',serial= alice_cnf.device_id)
    alice.setup()

    print "alice sdk_version: %s" % str(alice.sdk_version)

    # unlock screen if necessary
    alice.sys.unlock()

    alice.device.press('home')


    alice.sys.goto('uiphone')


    alice.phone.contacts.select_tab('logs')
    alice.phone.contacts.select_tab('favorites')
    alice.phone.contacts.select_tab('contacts')
    alice.phone.contacts.select_tab('keypad')

    try:
        alice.phone.contacts.select_tab('dummy')
    except Exception,e:
        assert str(e) == "'DUMMY' is not in list"


    return


def test_quick_menu():

    """


    """

    cnf = UiConfiguration(config)

    alice_cnf = cnf.get_phone_config('388897e5')
    #bob_cnf   = cnf.get_phone_config('e7f54be6')


    # init caller
    print "init alice ..."

    alice = UiDevice('callee',serial= alice_cnf.device_id)
    alice.setup()

    print "alice sdk_version: %s" % str(alice.sdk_version)

    # unlock screen if necessary
    alice.sys.unlock()

    alice.device.press('home')


    package = 'com.sec.android.app.launcher'
    frame  =  'android.widget.FrameLayout'


    sel = alice.device(packageName=package,className=frame,index='3').child(instance=0).child(className='android.widget.TextView', index='1')
    sel.click()

    alice.device.press('home')
    alice.sys.hot_key(2)

    alice.quick_launch(3)

    alice.quick_launch('Phone')
    alice.quick_launch('Apps')

    alice.phone.open()

    alice.phone.close()
    alice.phone.open()
    return



def test_phone_interface():
    """
    """
    cnf = UiConfiguration(config['platform_version'])

    hub = UiHub(config=cnf)

    alice_cnf = hub.config.get_phone_config('388897e5')
    bob_cnf   = hub.config.get_phone_config('e7f54be6')


    # init caller
    print "init alice ..."

    #alice = UiDevice('alice',serial= alice_cnf.device_id,config=cnf)
    alice =  hub.add_device('alice',serial= alice_cnf.device_id)
    alice.phone.open()

    # init callee
    print "init bob ..."
    bob = UiDevice('bob',serial= bob_cnf.device_id,config=cnf)
    bob.phone.open()


    # call
    destination =  alice.config.get_phone_config('e7f54be6').tel
    alice.phone.call_destination(destination)

    #time.sleep(10)

    caller = None
    try :
        caller = bob.phone.wait_incoming_call()
        print "bob: popup: incoming call from %s" % caller


        bob.phone.answer_call()
        "print call established"
        time.sleep(5)

    finally:
        alice.phone.close()
        bob.phone.close()


    alice.phone.close()


    return


def test_robot_relay():
    """


    """

    relay = DroydRelay(config=config)

    users_conf = relay.get_users_conf('Alice','Bob')




    hub = relay.hub
    configurator = relay.hub.config

    # buils users conf
    users = ['Alice','Bob']

    users_conf = []
    serials = sorted(hub.config.data['phones'].keys())

    for index,alias in enumerate(users):

        serial = serials[index]
        content =  hub.config.data['phones'][serial]
        value = content.copy()
        value['device_id'] = serial
        value['alias']= alias
        users_conf.append(value)

    # start agents
    relay.setup_agents(users_conf)


    # alice call bob
    destination =  configurator.get_phone_config('e7f54be6').tel

    relay.execute('Alice','phone.open')
    relay.execute('Alice' ,'phone.call_destination' ,destination=destination)

    # bob waiting for call
    relay.execute('Bob','phone.open')
    caller = relay.execute('Bob','phone.wait_incoming_call')
    print "bob: popup: incoming call from %s" % caller

    relay.execute('Bob' ,'phone.answer_call')
    print "call established"


    time.sleep(5)

    relay.execute('Alice','phone.close')
    relay.execute('Bob','phone.close')

    return


def test_robot_plugin():
    """


    """
    filename = '../platform.json'

    pilot =Pilot()

    pilot.setup_pilot(platform_name='mobile',platform_version='mobile_qualif',platform_configuration_file=filename)

    pilot.open_Session('Alice', 'Bob')


    #destination =  alice.config.get_phone_config('e7f54be6').tel
    destination = "0684820364"
    destination = "0640412593"

    pilot.call_number('Alice', destination)


    pilot.wait_incoming_call('Bob')
    pilot.answer_call('Bob')
    pilot.sleep(5)
    pilot.hangup('Alice')

    pilot.close_session()


    return



def test_robot_plugin2():
    """


    """
    filename = '../platform.json'

    pilot =Pilot()

    pilot.setup_pilot(platform_name='mobile',platform_version='mobile_qualif',platform_configuration_file=filename)

    pilot.open_Session('Alice', 'Bob')


    #destination =  alice.config.get_phone_config('e7f54be6').tel
    #destination = "0684820364"
    #destination = "0640412593"

    #pilot.call_number('Bob', destination)

    pilot.call_user('Alice','Bob')

    pilot.wait_incoming_call('Bob')
    pilot.answer_call('Bob')
    pilot.sleep(5)
    pilot.hangup('Alice')

    pilot.close_session()


    return


def test_config_store():
    """
    """
    filename = '../platform.json'

    with open(filename,"r") as fp :
        #data = fp.read()
        config = json.load(fp)
    data = config['mobile_qualif']

    s = ConfigStore()
    s.set_data(data)

    for collection in s.collections:

        json_dump = s.dump_collection(collection, as_json=True,pretty=True)
        print collection
        print json_dump
        print

    # some queries

    # get all users from enterprise 1
    users = s.find('users','enterprise_name', 'enterprise_1')
    assert len(users) == 22
    print users

    # get all users from enterprise 1 site 1
    users =  s.find2('users', enterprise_name='enterprise_1', site_name='site_1' )
    assert len(users) == 15
    print
    print users



    return


def test_uihubsession():
    """

    """
    filename = '../platform.json'

    with open(filename,"r") as fp :
        #data = fp.read()
        config = json.load(fp)
    data = config['mobile_qualif']

    s = ConfigStore()
    s.set_data(data)


    mobiles = s.find2('mobiles')

    m1 = mobiles[0]
    m2 = mobiles[1]

    # create session
    session = UiHubSession('dummy')

    # add device in session
    session.add(m1, s.get('mobiles',m1), alias='Alice')

    print session[m1]

    # add same device
    try:
        session.add(m1, s.get('mobiles',m1))
    except ValueError:
        # ok we cannot add an existing device
        pass
    else:
        raise AssertionError('device_id not unique')

    assert not session.has_device(m2)

    # add a second mobile
    session.add(m2, s.get('mobiles',m2),alias='Bob')

    bob = session.find(alias='Bob')

    assert session.has_device(m2)

    assert session.count() == 2

    # list session
    for pk ,data in session:
        print pk , data

    # delete m2
    session.remove(m1)

    assert not session.has_device(m1)

       # list session
    # list session
    for pk ,data in session:
        print pk , data

    session.clear()

    devices = session.find()
    assert len(devices) == 0

    assert session.count() == 0

    return


def test_new_robot_plugin():
    """


    """
    filename = '../platform.json'

    Alice = "e7f54be6"
    Bob = "388897e5"


    pilot =Pilot()

    pilot.setup_pilot(platform_name='mobile',platform_version='mobile_qualif',platform_configuration_file=filename)

    pilot.open_Session(Alice, Bob)


    destination =  pilot.ptf.get_phone_config(Bob).tel
    #pilot.call_number(Alice, destination)

    pilot.call_user(Alice,Bob)

    pilot.wait_incoming_call(Bob)
    pilot.answer_call(Bob)
    time.sleep(5)
    pilot.hangup(Alice)

    pilot.close_session()


    return




def test():
    """

    """
    test_UiDevice()

    return



if __name__=='__main__':
    """
    """


    #test_uiconfig()
    #test_uiconfig_json()

    #test_UiHub()

    #test()

    #test_UiDevice()


    #test_callee()
    #test_caller()

    #test_watchers()

    #test_Two_phones()

    #test_simple_call()


    #test_contacts_screen()


    #test_quick_menu()


    #test_phone_interface()



    #test_robot_relay()

    #test_robot_plugin()
    #test_robot_plugin2()

    #test_config_store()

    #test_uihubsession()


    test_new_robot_plugin()



    print


