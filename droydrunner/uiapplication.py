__author__ = 'cocoon'

class UiApplication(object):
    """

        represents an android application on a device

    """
    package_name = None


    def __init__(self,uidevice):
        """

        :param device: instance of UiDevice
        :param alias:
        :return:
        """
        self.uidevice=uidevice
        self.device=uidevice.device

        self.setup()


    def setup(self):
        """

        :param self:
        :return:
        """
        return

    def click(self,*args,**kwargs):
        return self.device.click(*args,**kwargs)


    @property
    def package(self):
        return self.package_name



class uiApplications(object):
    """
        represents a set of applications
    """