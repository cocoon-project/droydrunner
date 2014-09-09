__author__ = 'cocoon'


from droydrunner.uidevice import UiDevice
import time


# white gs5
id1 = '388897e5'


def test_ussd_125():


    # create uidevice
    d1 = UiDevice(serial=id1)

    # select phone app
    d1.quick_launch('phone')

    # call #125#
    d1.phone.call_destination("#125#")

    # get the message USSD code running
    message = d1.device(resourceId= 'android:id/message', className = 'android.widget.TextView').text
    print message


    # wait to see OK button
    d1.device(resourceId='android:id/button1').wait.exists(timeout=3000)
    #time.sleep(3)

    # we got the screen

    # get the message
    message = d1.device(resourceId= 'android:id/message', className = 'android.widget.TextView').text
    print message

    # wait to see message
    time.sleep(3)

    # press OK
    button = d1.device(resourceId='android:id/button1')
    button.click()


    return


def test_ussd_123():


    print 'test suivi conso'

    # create uidevice
    d1 = UiDevice(serial=id1)

    # select phone app
    d1.quick_launch('phone')

    # call #123#
    d1.phone.call_destination("#123#")

    # get the message USSD code running
    message = d1.device(resourceId= 'android:id/message', className = 'android.widget.TextView').text
    print message


    package= 'com.android.phone'
    to_id= "com.android.phone=id/%s"

    # wait to see the dialog message
    dialog_id = 'com.android.phone:id/dialog_message'
    wait = d1.device(resourceId=dialog_id).wait.exists(timeout=3000)
    # print message
    print  d1.device(resourceId=dialog_id).text


    # select choice 1: detail suivi conso
    input_field = d1.device( resourceId ='com.android.phone:id/input_field')
    #input_field.long_click()

    # input choice
    input_field.set_text('1')


    # send
    send_button = d1.device(resourceId='android:id/button1')
    send_button.click()


    # wait next screen
    d1.device.wait.update()


    # print message
    message = d1.device(resourceId=dialog_id)
    print message.text


    # select 1: appels
    input_field = d1.device( resourceId ='com.android.phone:id/input_field')
    input_field.set_text('1')
    # send
    send_button = d1.device(resourceId='android:id/button1')
    send_button.click()
    # wait next screen
    d1.device.wait.update()




    # print message conso appel
    message = d1.device(resourceId=dialog_id)
    print message.text

    time.sleep(5)


    # select 0 -retour
    input_field = d1.device( resourceId ='com.android.phone:id/input_field')
    input_field.set_text('0')
    # send
    send_button = d1.device(resourceId='android:id/button1')
    send_button.click()
    # wait next screen
    d1.device.wait.update()

    # select 8-Retour
    input_field = d1.device( resourceId ='com.android.phone:id/input_field')
    input_field.set_text('8')
    # send
    send_button = d1.device(resourceId='android:id/button1')
    send_button.click()
    # wait next screen
    d1.device.wait.update()




    # press cancel
    cancel_button = d1.device(resourceId='android:id/button2')
    cancel_button.click()





    return



if __name__=='__main__':


    test_ussd_125()
    test_ussd_123()















