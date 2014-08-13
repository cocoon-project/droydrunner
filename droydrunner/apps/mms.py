__author__ = 'cocoon'


"""


"""

package ='com.android.mms'



search = ('android:id/action_bar_container',0,'0/0/1')
compose = ('android:id/action_bar_container',1,'0/0/1')
more = ('android:id/action_bar_container',2,'0/0/1')


add_prioruty_sender = 'com.android.mms:id/add_priority_sender'


messages_list='android:id/list'

# 0 : msg 1

# last : 3 conversations



#more

option_select = ('root',0,'0/0')


option_help = ('root',8,'0/0')





#compose

recipient_editor_to = 'com.android.mms:id/recipients_editor_to'

add_recipient = 'com.android.mms:id/add_recipient_button'

edit = 'com.android.mms:id/edit_text_bottom'

attach = 'com.android.mms:id/attach_button'


send = 'com.android.mms:id/send_button'

# envoyer un message

compose.click()

recipient_editor_to.long_click()
recipient_editor_to.set_text()

edit.click()
edit.set_text()

send.click()

