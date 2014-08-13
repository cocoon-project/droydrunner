__author__ = 'cocoon'


from droydrunner.api.api import NativeClient

import time

users = {

       "388897e5" : {  "name": "Caller" , "pin": None , "sim": "0000", "tel":"0640412593" ,'alias': '388897e5' },

        "e7f54be6":  {  "name": "Calee" , "pin": None , "sim": "0000", "tel":"0684820364", 'alias': 'e7f54be6'},


}





# def test_http_api():
#     """
#
#     """
#
#     alice = "388897e5"
#     bob = "e7f54be6"
#
#     bob_number = users[bob]['tel']
#
#     with Client('http://127.0.0.1:5001') as c :
#
#         # users = {
#         #     'Alice' : { 'tel': '06..'   },
#         #     'Bob' : { 'tel': '01'}
#         # }
#
#
#
#         session = c.open_session(**users)
#
#         c.call_number(alice, bob_number)
#
#         c.wait_incoming_call(bob)
#
#         c.answer_call(bob)
#
#         time.sleep(5)
#
#         c.hangup(alice)
#
#
#         c.close_session()


def test_native_phone_api():
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



def test_general_api():


    api = NativeClient()

    api.add_device(**users)

    for device_id in users.keys():

        # hub operation
        #api.hub.device_list()
        #api.add_device( device_id,device_data)

        # sytem operation
        #api.sys(device_id,'press')('home')
        #api.sys(device_id,'quick_launch')('PHONE')

        #api.phone.open()
        api.call(device_id,'phone.open')

        # aplication operations
        #api.app('phone',device_id).operation

    api.call('388897e5','phone.call_destination' , '0684820364')
    api.call('e7f54be6','phone.wait_incoming_call')
    api.call('e7f54be6','phone.answer_call')
    time.sleep(4)
    api.call('388897e5','phone.end_call' )

    #api.close()



    return



if __name__=='__main__':


    #test_native_phone_api()
    #test_http_api()

    test_general_api()


    print
