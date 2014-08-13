# -*- coding: utf8 -*-
__author__ = 'cocoon'
"""

    the main application of the device system


"""

from uiapplication import UiApplication




class UiSystem(UiApplication):
    """
        represents the main device application


        uiSystem has uidevice



        uiSystem has screens:

        home
        home_pages



        actions

        goto_settings


        goto_right

        goto left



    """
    package_name = 'android'

    def __init__(self,uidevice,sdkint=0,layout=None):
        """

        :param device: instance of UiDevice
        :param alias:
        :return:
        """
        self.uidevice=uidevice
        self.device=uidevice.device

        # sdk version
        self._sdkint = sdkint

        # main layout
        self.layout = ApplicationLayout(uidevice=self.uidevice, layout =layout)


    def goto(self,app_name):
        """

        :param app_name:
        :return:
        """
        return self.layout.goto(app_name)

    def hot_key(self,index=0):
        """
            select a widget from the hot_keys(

        :param index:
        :return:
        """
        return self.layout.hot_key_selector(index).click()


    def unlock(self):
        """

            unlock the screen if necessary

        :return:
        """
        #TODO: only handle simple swipe unlock


        self.device.wakeup()

        current = self.uidevice.current_package_name()
        #print current
        if current == "com.android.keyguard":
            # unlock screen with swipe
            self.device.swipe(270,1440,800,1000,steps=50)
            self.device.wait.update()
            current = self.uidevice.current_package_name()
            #print current
            if current == "com.android.keyguard":
                raise RuntimeError('Cant unlock device')
        return


    def select_choice(self,resource_id,choice,path=None):
        """

            select a tab starting with resourceId , navigate path and select index


            eg select_tab('com.sec.android.app.launcher:id/hotseat', 0 '0/0'  )


        :param resource_id:
        :param path: str index separated with /  eg "0/1/0
        :param index: position in the menu (0..) or text
        :return:
        """

        # find the root element by id
        if resource_id == 'root':
            element = self.device(instance=0)
        else:
            element = self.device(resourceId=resource_id)

        # navigate down the path
        if path:
            indexes = path.split('/')
            for i in indexes:
                element = element.child(index= int(i))

        # return the selected item selector
        if isinstance(choice,int):
            # select by index
            return element.child( index=choice)
        else:
            # select by text
            return element.child( text=choice)




class ApplicationLayout(object):
    """

        represents the location of each app on the device menu

        eg uiphone: home quick 0  or home quick phone

    """

    default_layout = {

        'uiphone': ['home','quick' , 0 ],

        'uicamera' : ['home', 'home', 'right' , (1, 0 , 3)]

    }

    def __init__(self,uidevice,layout=None):
        """

        :param uidevice:
        :return:
        """
        self.uidevice=uidevice
        self.device=uidevice.device

        if not layout:
            layout = self.default_layout
        self._layout = layout



    def goto(self,app_name):
        """

        :param app_name:
        :return:
        """
        # hard coded , change this
        if app_name == 'uiphone':
            self.device.press('home')
            self.device.wait.update()
            names = [u"Téléphone","Phone"]
            for name in names:
                if self.device(text=name).exists:
                    return self.device(text=name).click()
            raise RuntimeError("Cant find application %s on device %s" % (app_name,self.uidevice.alias))

        else:
            raise NotImplemented('unkwown application: %s' % app_name)



    def hot_key_selector(self,index=0):
        """

        :param index:
        :return:
        """
        assert 0<= index <= 4
        package = 'com.sec.android.app.launcher'
        frame  =  'android.widget.FrameLayout'

        return self.device(packageName=package,className=frame,index='3').child(instance=0).child(className='android.widget.TextView', index=index)


