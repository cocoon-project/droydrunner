
# -*- coding: utf8 -*-
__author__ = 'cocoon'

import os, sys, time
import inspect

from uiautomator import device
from uiautomator import Device


# applications
from uisystem import UiSystem
from apps.uiphone import Application as PhoneApplication

class UiDevice(object):
    """


    """

    def __init__(self,alias=None,serial=None,applications=None,config=None):
        """

        :param device:
        :param alias:
        :param applications: list , list of application names
        :param config: instance of UiConfiguration
        :return:
        """
        if not serial:
            self.device=device
        else:
            self.device = Device(serial)

        self.alias = alias
        self.serial = serial

        if applications == None:
            applications = ['uiphone',]
        self.applications = applications

        self._config = config

        self.setup()


    def setup(self,connected=True):
        """

        :param self:
        :return:
        """

        if connected:
            # get info from device
            self._base_info = self.device.info



        # set the sdk version
        sdkint= 0
        sdkint = self._base_info.get('sdkInt',0)



        # set the system application
        self.sys=UiSystem(self,sdkint=sdkint,layout=None)

        self.phone = PhoneApplication(self)

        # set the application set
        #self.app = ApplicationSet(self.applications)

        if connected:

            # unlock phone if necessary
            self.sys.unlock()




        return

    def __getattr__(self, attr):
        """
            redirect to uiasystem or uiautomator

        """
        # redirect to uisystem ( sys )
        if hasattr(self.sys, attr):
            m =  getattr(self.sys, attr)
            if inspect.ismethod(m):
                def sys_wrapper(*args, **kwargs):
                    return m(*args, **kwargs)
                return sys_wrapper
            else:
                return m

        # forward method/attribute to uiautomator device if method supportted
        elif hasattr(self.device, attr):
            # if attr == 'screenshot':
            #     return self.screenshot_common
            m =  getattr(self.device, attr)
            if inspect.ismethod(m):
                def device_wrapper(*args, **kwargs):
                    return m(*args, **kwargs)
                return device_wrapper
            else:
                return m
        raise AttributeError(attr)

    def __call__(self, *args, **kwargs):
        '''
        selector support:
        d(text="Settings").click()
        '''
        return self.device(*args, **kwargs)




    def open(self):
        """

        :return:
        """
        # unlock device
        self.sys.unlock()

    def close(self):
        """

        :return:
        """
        # close phone application if necessary
        self.phone.close()

        # if self.phone._call_state != 'IDLE':
        #     self.phone.close()
        # else:
        #     self.device.press('home')


    def log(self,msg,level='DEBUG'):
        """

        :param msg:
        :param level:
        :return:
        """
        print "%s: %s" % (self.alias,msg)


    @property
    def sdk_version(self):
        return self._base_info['sdkInt']


    @property
    def config(self):
        return self._config

    def current_package_name(self):
        """

        """
        info = self.device.info
        return info['currentPackageName']



    def info(self,attribute=None):
        """
            return the device info

            attribute can be:

            { u'displayRotation': 0,
              u'displaySizeDpY': 640,
              u'displaySizeDpX': 360,
              u'currentPackageName': u'com.android.launcher',
              u'productName': u'takju',
              u'displayWidth': 720,
              u'sdkInt': 18,
              u'displayHeight': 1184,
              u'naturalOrientation': True
            }

        :param attribute:str name of param
        """
        fetch_info = self.device.info
        if attribute is not None:
            return fetch_info[attribute]
        else:
            return fetch_info



    # def press_home(self):
    #     self.device.press.home()

    def goto_home(self):
        """
            from any screen goto home

        :return:
        """
        self.press_home()
        self.press_home()


    def quick_launch(self,index):
        """
            lauch a task by the quick launch botom bar

            index
                is either numerical (0 , 4) representing icon position from left to right

                or the name of the task ( default attribution


        """
        _tabs = ['PHONE','CONTACTS','MESSAGES','INTERNET','APPS']
        # determine position
        try:
            if isinstance(index,int):
                # it is a numerical position
                position = index

            elif index.upper() in _tabs:
                # the name of the task
                position = _tabs.index(index.upper())
            else:
                position = -1
            assert 0 <= position <= 4
        except:
            raise ValueError('quick_launch: invalid argument: %s' % str(index))

        # press home to exit a the current screen
        self.press('home')

        # select the task
        return self.sys.hot_key(position)



    def apply(self,selector,action=None,raise_on_error=False):
        """
            check if selector exists , apply action on it
            default action is device.click

        """
        if not action:
            action=self.device.click
        if selector.exists:
            action(selector)
        else:
            if raise_on_error:
                raise KeyError('selector not found:%s' % str(selector))






class ApplicationSet(object):
    """
        represents the set of application of a device

    """
    def __init__(self, *app_name ):
        """

        :param app:
        :return:
        """
        self._apps ={}



