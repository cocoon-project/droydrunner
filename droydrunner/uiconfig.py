__author__ = 'cocoon'

"""
    configuration


"""
import json
import os
from utils.store import Store


class UiConfiguration(object):
    """

        platform_version = {
            phones = {
                '388897e5' : {  'name': 'Caller' ,'pin':None  },
                '4df18692171e5fed': {  'name': 'GT-I9300' , 'pin': "325698"},
            }
        }
    """


    def __init__(self,data,platform_version=None):
        """

        """
        self.platform_version=platform_version
        self.data=data


    def get_phone_config(self,device_id,kind="mobiles"):
        """
            get a mobile phone config object
        """
        phones= self.data['mobiles']
        return DeviceConfig(device_id,phones[device_id])


    def iter(self,kind='mobiles',sort=True):
        """
            iter on phones ; yield (device_id , data)
        :param kind:
        :return:
        """
        if not kind == 'mobiles':
            raise NotImplementedError('only handle mobile phones')
        keys = self.data[kind].keys()
        if sort:
            keys = sorted(keys)
        for device_id in keys:
            data = self.data[kind][device_id]
            yield device_id , data

    def find_device(self,serial=None,name=None,number=None,kind='mobiles'):
        """
            request on phones

        :return :  a list of DeviceConfig objects
        """
        response=[]
        if not kind == 'mobiles':
            raise NotImplementedError('only handles mobiles devices')
        if not serial and not name and not number:
            # no query parameters: return all
            for device_id, data in self.iter():
                response.append(DeviceConfig(device_id,data))

        return response



    @classmethod
    def from_json(cls,filename,platform_version=None):
        """

        """
        with open( filename,"r") as fp:
            data = json.load(fp)
        if platform_version:
            data = data[platform_version]
        obj = cls(data,platform_version=platform_version)
        obj._filename = os.path.abspath(filename)
        return obj


class DeviceConfig(object):
    """
        config object for a mobile devices

    """

    def __init__(self,device_id,data):
        """

        :param data:
        :return:
        """
        self._device_id = device_id
        self.data = data


    @property
    def device_id(self):
        return self._device_id

    @property
    def name(self):
        return self.data['name']

    @property
    def pin_code(self):
        return self.data['pin']

    @property
    def sim_code(self):
        return self.data['sim']

    @property
    def tel(self):
        return self.data['tel']


    def get_property(self,property_name):
        """


        :param property_name:
        :return:
        """
        try:
            return self.data[property_name]
        except KeyError:
            raise KeyError('device %s has no property: %s'% self.device_id,property_name)




class ConfigStore(Store):
    """

    """
    collections = ['main','users','enterprises','sites','featureaccesscode','destinations','mobiles']


    def setup(self):
        """

        :return:
        """

    def set_data(self,data):
        """

            init db from a data source

        :param data:
        :return:
        """
        # create main section  entry_data is a dictionary
        for entry_id, entry_data in data['main'].iteritems():
            self.add_entity('main',entry_id,entry_data)

        for collection,collection_data in data.iteritems():

            if collection == 'main':
                # already treated
                continue

            if collection.lower() in ['mobiles','featureaccesscode','destinations']:
                # entry_data is a dictionary
                for entry_id, entry_data in collection_data.iteritems():
                    self.add_entity(collection.lower(),entry_id,entry_data)
            elif collection == 'enterprises':
                site_count = 0
                for enterprise_name,enterprise_data in data['enterprises'].iteritems():
                    # setup enterprise entry
                    enterprise_id = enterprise_name
                    enterprise_entry = {'name': enterprise_name}
                    # treat everything but site
                    for element_id,element_data in data['enterprises'][enterprise_name].iteritems():

                        if element_id not in ['sites']:
                            # complete enterprise entry
                            enterprise_entry[element_id] = element_data
                    # create enterprise entry
                    self.add_entity('enterprises',enterprise_id,enterprise_entry)

                    # treat sites
                    try:
                        sites = data['enterprises'][enterprise_name]['sites']
                    except KeyError:
                        sites = {}
                    for site_name,site_data in sites.iteritems():

                        # setup site entry
                        site_count+=1
                        site_entry = { 'site_name': site_name , 'enterprise': enterprise_name   }

                        for element_id,element_data in sites[site_name].iteritems():
                            if element_id not in ['users']:
                                site_entry[element_id]= element_data

                        # create site entry
                        self.add_entity('sites',site_count , site_entry)

                        # treat site users
                        try:
                            users= sites[site_name]['users']
                        except:
                            users = {}

                        for user_id,user_data in users.iteritems():

                            # create user entry
                            user_entry = user_data.copy()
                            user_entry['enterprise_name']= enterprise_name
                            user_entry['site_name'] = site_name
                            # add default
                            for name in ['password','profile','domain','proxy']:
                                if not user_entry.has_key(name):
                                    default = data['main'].get(name,None)
                                    if default is not None:
                                        user_entry[name] = data['main'][name]


                            self.add_entity('users',user_id,user_entry)






