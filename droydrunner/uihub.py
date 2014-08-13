__author__ = 'cocoon'



from uidevice import UiDevice
from uiconfig import DeviceConfig
from uiconfig import ConfigStore

from uiautomator import  Adb


class UiHub(object):
    """
        represents a set of Device

    """

    def __init__(self,config=None):
        """

        :return:
        """

        self.config = config




        # dict of devices connected to the hub, key is the device_id
        self.connected_devices = {}

        # dict of active devices , key is alias
        self._devices = {}




        # device_ids available ( eg not actice)
        self.available_devices = []



        self.adb = Adb()




    def device_list(self):
        """

        :return: list : list of android connected device
        """
        self.connected_devices = self.adb.devices()
        return self.connected_devices



    def device(self,alias):
        """
            return the given connected device info
        :param alias:
        :return:
        """
        try:
            c = self.connected_devices
            assert c != {}
        except:
            self.device_list()
        return self.connected_devices[alias]



    def add_device(self,alias,serial=None,applications=None):
        """
            add a device , make it active

            if no serial is specified take a random device_it (not used ) amoung the connected devices


        :param allias:
        :param serial:
        :param applications:
        :return:
        """
        if not serial:
            # no serial specified: take a random one
            raise NotImplementedError


        self._devices[alias]= UiDevice(alias,serial=serial,applications=applications,config=self.config)
        return self._devices[alias]



    def iter_device(self):
        """
            iteration over active devices
        :return:
        """


    def find_device(self,**kwargs):
        """
            find an active device

        :param kwargs:
        :return:
        """



class UiHubSession(object):
    """
        a hub session

            keep track of devices implied in session for a given hub


            add, get , find, iter


    """

    # class to handle a device configuration
    #_device_handler = DeviceConfig

    def __init__(self,hub):
        """

        :param uihub: instance of UiHub
        :return:
        """
        self.hub = hub
        #self.config = hub.config

        # liste of active devices
        self.store = ConfigStore()


    # def iter(self,hint=None,**kwargs):
    #     """
    #         iterate over active devices
    #
    #     :return:
    #     """
    #     return self.store.iter_collection('main')
    #     #return self.store.iter2('main',hint=hint,**kwargs)

    def __iter__(self):
        return self.store.iter_collection('main')

    def __getitem__(self, item):
        return self.store.get('main',item)

    def get(self,pk):
        return self.store.get('main',pk)

    def find(self,hint=None,**kwargs):
        """
            query an active device

            return list of device ids

        :param kwargs:
        :return:
        """
        return self.store.find2('main',hint=hint,**kwargs)

    def find_one(self,hint=None,**kwargs):
        """

        :param hint:
        :param kwargs:
        :return:
        """
        try:
            return self.find(hint=hint,**kwargs)[0]
        except IndexError:
            raise KeyError('device not in session')

    def add(self,device_id,data,**kwargs):
        """

        :param device:
        :param data:
        :return:
        """
        # check unicity
        try:
            self.store.get('main',device_id)
        except KeyError:
            # ok it does not exists
             # add keys from kwargs
            data =data.copy()
            for k,v in kwargs.iteritems():
                data[k]=v
            self.store.add_entity('main',device_id,data)

        else:
            raise ValueError('device id %s already exists in session' % device_id)

    def has_device(self,device_id):
        try:
            self.store.get('main',device_id)
        except KeyError:
            return False
        return True


    def remove(self,device_id):
        """

        :param device:
        :return:
        """
        self.store.delete('main',device_id)

    def clear(self):
        """
            raz session
        :return:
        """
        del self.store
        self.store =ConfigStore()

    def count(self):
        """

        :return:
        """
        return self.store.count()


# global instance of a hub
hub = UiHub()





