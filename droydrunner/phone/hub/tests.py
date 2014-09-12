__author__ = 'cocoon'

import time

from droydrunner.phone.hub.api import NativeClient
from droydrunner.phone.hub.client import HttpClient

users = {

       "388897e5" : {  "name": "Caller" , "pin": None , "sim": "0000", "tel":"0640412593" ,'alias': '388897e5' },

        "e7f54be6":  {  "name": "Calee" , "pin": None , "sim": "0000", "tel":"0684820364", 'alias': 'e7f54be6'},


}





def test_http_api():
    """

    """

    alice = "388897e5"
    bob = "e7f54be6"

    bob_number = users[bob]['tel']

    #with HttpClient('http://127.0.0.1:5001') as c :

    with HttpClient('http://192.168.1.23:49153') as c :
        # users = {
        #     'Alice' : { 'tel': '06..'   },
        #     'Bob' : { 'tel': '01'}
        # }



        session = c.open_session(**users)

        c.call_number(alice, bob_number)

        c.wait_incoming_call(bob)

        c.answer_call(bob)

        time.sleep(5)

        c.hangup(alice)


        c.close_session()


def test_native_api():
    """

    """

    alice = "388897e5"
    bob = "e7f54be6"

    bob_number = users[bob]['tel']

    with NativeClient() as c :

        # users = {
        #     'Alice' : { 'tel': '06..'   },
        #     'Bob' : { 'tel': '01'}
        # }



        session = c.open_session(**users)

        c.call_number(alice, bob_number)

        c.wait_incoming_call(bob)

        c.answer_call(bob)

        time.sleep(5)

        c.hangup(alice)


        c.close_session()


def ussd_123_send(session,serial,choice):
    """


    :param choice:
    :return:
    """
    input_field_id = { 'resourceId':'com.android.phone:id/input_field'}
    send_button_id = {'resourceId':'android:id/button1'}

    # select choice
    session.select(serial,action='set_text', action_args=[str(choice),] ,**input_field_id)

    # send
    session.select(serial,action='click',**send_button_id)

    # wait update
    session.command(serial,action='wait.update')

    time.sleep(2)


    #input_field = agent.device( resourceId ='com.android.phone:id/input_field')
    #input_field.set_text(str(choice))
    # send
    #send_button = agent.device(resourceId='android:id/button1')
    #send_button.click()
    # wait next screen
    #d1.device.wait.update()
    return

def test_native_api_low_level():

    alice = "388897e5"


    user = { "388897e5": users["388897e5"]}

    with NativeClient() as c :

        # users = {
        #     'Alice' : { 'tel': '06..'   },
        #     'Bob' : { 'tel': '01'}
        # }




        session = c.open_session( **user)


        c.call_number(alice,"#123#")

        # get the message USSD code running
        message = c.select(alice,resourceId= 'android:id/message', className = 'android.widget.TextView',action='text')
        print message

        # wait screen update
        c.command(alice,action='wait.update')




        # wait to see the dialog message
        dialog_id = 'com.android.phone:id/dialog_message'

        c.select(alice,  action='wait.exists', resourceId=dialog_id )
        # print message main menu
        print c.select(alice,resourceId=dialog_id , action = 'text')


        # select 1 :detail suivi conso
        ussd_123_send(c,alice,1)

        # select 1 :Appels
        ussd_123_send(c,alice,1)


        # print message conso appel
        print c.select(alice,action='text',resourceId=dialog_id)


        time.sleep(5)


        # select 0 : Retour
        ussd_123_send(c,alice,0)

        # select 8 Retour
        ussd_123_send(c,alice,8)


        # send cancel
        c.select(alice,action='click' , resourceId='android:id/button2')


        c.close_session()



def test_http_api_low_level():

    alice = "388897e5"


    user = { "388897e5": users["388897e5"]}

    with HttpClient('http://192.168.1.23:49153') as c :
    #with HttpClient('http://localhost:5000') as c :
        # users = {
        #     'Alice' : { 'tel': '06..'   },
        #     'Bob' : { 'tel': '01'}
        # }




        session = c.open_session( **user)


        c.call_number(alice,"#123#")

        # get the message USSD code running
        #message = c.select(alice,resourceId= 'android:id/message', className = 'android.widget.TextView',action='text')
        #print message

        # wait screen update
        #c.command(alice,action='wait.update')

        c.wait(alice,action='update',timeout=2000)

        time.sleep(2)


        # wait to see the dialog message
        dialog_id = 'com.android.phone:id/dialog_message'

        c.select(alice,  action='wait.exists', resourceId=dialog_id )
        # print message main menu
        print c.select(alice,resourceId=dialog_id , action = 'text')


        # select 1 :detail suivi conso
        ussd_123_send(c,alice,1)

        # select 1 :Appels
        ussd_123_send(c,alice,1)


        # print message conso appel
        print c.select(alice,action='text',resourceId=dialog_id)


        time.sleep(5)


        # select 0 : Retour
        ussd_123_send(c,alice,0)

        # select 8 Retour
        ussd_123_send(c,alice,8)


        # send cancel
        c.select(alice,action='click' , resourceId='android:id/button2')


        c.close_session()





if __name__=='__main__':


    #test_native_api()
    #test_native_api_low_level()



    # dont forget to start server

    #test_http_api()
    test_http_api_low_level()


    print
