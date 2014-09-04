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

    with HttpClient('http://127.0.0.1:5001') as c :

    #with HttpClient('http://192.168.1.23:49153') as c :
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



if __name__=='__main__':


    #test_native_api()

    # dont forget to start server

    test_http_api()



    print
