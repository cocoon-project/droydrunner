__author__ = 'cocoon'




#from uiautomator import AutomatorDeviceUiObject


class UiScreen(object):
    """


    screen have

        selectors

        tabs
            tabs have selectors



    """
    def __init__(self,uiapplication):
        """

        :param uidevice:
        :return:
        """
        self.uiapplication = uiapplication
        self.uidevice=uiapplication.uidevice
        self.device=uiapplication.uidevice.device

        self.setup()


    def setup(self):
        return


class UiTab(object):
    """
        a tab on a screen


    """
    _check = {}


    def __init__(self,uiscreen):
        """

        :param uidevice:
        :return:
        """
        self.uiscreen = uiscreen
        self.device=uiscreen.device