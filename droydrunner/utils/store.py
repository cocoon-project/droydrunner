# -*- coding: UTF-8 -*-
"""


    storage for dictionary ( persistance with  shelve )


    each qc  entities is stored in a shelf db on a subdirectory


    tests => tests.db
    test-sets => test-sets.db






"""

import os
import shelve
import json
import pickle


import logging
log = logging.getLogger(__name__)


class Store():
    """

        a storage of collection of items

            collection has a name (id) and data is a dictionary , id/data

            item has an id , the data is a set of key/value pairs

            indexable on all keys

            persistance option


    """


    # collections=  [
    #         'tests','test-configs','test-folders','runs','test-instances','test-sets',
    #         'test-set-folders','releases','release-cycles','release-folders','requirements','run-steps']


    collections = ['main',]


    def __init__(self,filename=None):
        """
            @path : directory where to store or None if not persistant
        """

        self.filename= filename
        if not filename:
            self.persistant=False
            # auto open if not persistant
            self.open()
        else:
            self.persistant = True

    def setup(self):
        """

        """
        return


    def create_pk(self):
        """
            create primary collection iter index
        """
        self._custom_indexes={}
        for collection in self.collections:
            self._custom_indexes[collection]={'_iter':[]}
        # build collections keys
        for key in self.db.keys():
            if ':' in key :
                collection,pk = key.split(':')
                # exclude internal collections
                if not collection.startswith('_'):
                    self._custom_indexes[collection]['_iter'].append(int(pk))
        return

    def open(self):

        if self.filename:
            self.db = shelve.open(self.filename,protocol=2)
        else:
            self.db = {}
        self.create_pk()
        self.setup()
        return self

    def sync(self):
        if self.persistant:
            return self.db.sync()
        else:
            return True


    def close(self):
        """
        """
        if self.persistant:
            try:
                self.db.close()
            except AttributeError:
                pass

    def __enter__(self,*args,**kwargs):
        """

        """
        print "__enter__"
        if self.persistant:
            self.open()
        return self

    def __exit__(self, type, value, traceback):
        """

        """
        print "__exit__"
        self.close()
        return


    def build_index(self,collection, * index_names):
        """

        """
        if not collection in self.collections:
            raise KeyError('Invalid collection: %s' % collection)

        for pk,entity in self.iter_collection(collection):
            for index_name in index_names:
                if index_name in entity:
                    value = entity[index_name]
                    if not index_name in self._custom_indexes[collection]:
                        self._custom_indexes[collection][index_name]= {}
                    if not  value in self._custom_indexes[collection][index_name]:
                        self._custom_indexes[collection][index_name][value]=[]
                    self._custom_indexes[collection][index_name][value].append(pk)

    def find(self,collection,index_name,value,order_by_index=False):
        """

            find ids corresponding to a index_name and value

                return an array of collection s id (integers)

                auto build index on demand

            @collection : tests , test-sets
            @index_name : parent-id , test-id
            @value  245,
        """
        value = unicode(value)
        try:
            entity_ids = self._custom_indexes[collection][index_name][value]
            # we found it
            if order_by_index:
                entity_ids=sorted(entity_ids)
            else:
                return entity_ids
        except KeyError:
            # no index corresponding ,build index and retry
            pass

            #
        # check if collection is valid
        if not collection in self.collections:
            raise KeyError('Invalid Collection: %s' % collection)
        # the collection is ok , go on

        # check index exits
        if not self._custom_indexes[collection].has_key(index_name):
            # no index index name : create it
            self.build_index(collection,index_name)
        # retry
        try:
            entity_ids = self._custom_indexes[collection][index_name][value]
            # we found it , at last
            if order_by_index:
                return sorted(entity_ids)
            else:
                return entity_ids
        except KeyError:
            # not found
            return []


    def iter2(self,collection,hint=None,**kwargs):
        """

            query on collections the items satisfiyng all the the kwargs requirements

            eg  find2('users' , enterprise_name = 'enterprise_1' ,site_name = 'site_1' )

        :param collection:
        :param hint:
        :param kwargs:
        :return:
        """
        if hint != None:
            raise NotImplementedError('hint is not implemented yet')
        for pk , data in self.iter_collection(collection):
            assert isinstance(data,dict)
            # try to statisfy condition
            hit = 0
            for kw , kw_value in kwargs.iteritems():
                value = self.db[self.key(collection,pk)][kw]
                if kw_value == value:
                    # this criteria is matching
                    hit += 1
                else:
                    break
            # if all criteria are matching : yield it
            if hit == len(kwargs):
                yield pk

    def find2(self,collection,hint=None,**kwargs):
        return list(self.iter2(collection,hint=hint,**kwargs))



    def raz(self):
        """
            destroy db and recreate empty
        """
        os.remove(self.filename)
        self.open()
        self.setup()
        return


    def keys(self):
        """
        """
        return self.db.keys()

    def has_key(self,entity_type,key):
        """
        """
        return self.db.has_key(self.key(entity_type,key))


    def get(self,collection,key):
        """


        """
        try:
            return self.db['%s:%s' % (collection ,str(key))]
        except KeyError:
            if not collection in self.collections:
                if not collection.startswith('_'):
                    raise KeyError('Invalid collection: %s' % collection)
                else:
                    # a special collection
                    raise KeyError('no such key %s:%s' %(collection,key) )
            else:
                raise KeyError('no such key %s in collection %s' % (key,collection))


    def put(self,collection,key,value):
        """
            put a complete entry ( value is a dict )
        """
        #TODO update index
        self.db[self.key(collection,key)] = value

    def delete(self, collection , id_ ):
        """
            delete an entity
        """
        del self.db[self.key(collection,id_)]
        # remove entity from main index
        pos= self._custom_indexes[collection]['_iter'].index(id_)
        self._custom_indexes[collection]['_iter'].pop(pos)
        # raz collection secondary indexes
        to_delete=[]
        for index_name in self._custom_indexes[collection]:
            if not index_name.startswith('_'):
                #self._custom_indexes[collection][index_name]={}
                to_delete.append(index_name)
                #to_delete.append(self._custom_indexes[collection][index_name])
        # effective delete
        for index_name in to_delete:
            del self._custom_indexes[collection][index_name]


    def delete_collection(self,collection):
        """
        """
        # delete all entries in collection
        for id_ in self.iter_id(collection):
            del self.db[self.key(collection,id_)]
        # rebuild primary index ( raz of all indexes)
        self.create_pk()
        return

    def key(self, collection, key):
        return collection + ":" + str(key)



    def iter_key(self,collection,order_by_id=False):
        """
            iter on all keys of a collection
        """
        for id_ in self.iter_id(collection,order_by_id):
                yield "%s:%d" % (collection,id_)


    def iter_id(self,collection,order_by_id=False):
        """
            iter on id (int) of a collection
        """
        if order_by_id:
            for id_ in sorted(self._custom_indexes[collection]['_iter']):
                yield id_
        else:
            for id_ in self._custom_indexes[collection]['_iter']:
                yield id_

    def iter_collection(self,collection,order_by_id=False,filter=None,fields=None):
        """

        """
        for pk in self.iter_id(collection,order_by_id):
            entity = self.get(collection,pk)
            if filter:
                if filter(entity) == False:
                    # skip it
                    continue
            if fields:
                model={}
                for key in fields:
                    model[key] = entity[key]
                yield model
            else:
                yield pk, entity

    def add_entity(self,collection,key,entity_data):
        """
            add entity to collection and update indexes
        """
        # update main index
        #self._custom_indexes[collection]['_iter'].append(int(key))
        self._custom_indexes[collection]['_iter'].append(key)
        # update indexes
        try:
            for index_name in self._custom_indexes[collection]:
                if index_name.startswith('_'):
                    # dont update special indexes
                    continue
                if index_name in entity_data:
                    try:
                        index = self._custom_indexes[collection][index_name][entity_data[index_name]]
                        index.append(entity_data['id'])
                    except KeyError:
                        self._custom_indexes[collection][index_name][entity_data[index_name]]= [entity_data['id'],]
        except KeyError:
            pass
        # create entity in db
        self.put(collection,key,entity_data)


    def set_item(self,collection,key,entity_id,entity_data):
        """
            add a item in an entry

        :param collection:
        :param key:
        :param entity_id:
        :param entity_data:
        :return:
        """
        # fetch data
        data = self.get(collection,key)
        # add item to data
        data[entity_id] = entity_data
        if self.persistant:
            self.put(collection,key,data)


    def dump_collection(self,collection,as_json=False,as_pickle=False,order_by_id=False,filter=None,
                        fields=None,pretty=False):
        """
            return a dict of entities of the collection
        """
        result = {}
        for pk, entry in self.iter_collection(collection,order_by_id=order_by_id,filter=filter,fields=fields):
            result[pk]=entry


        #result = list(self.iter_collection(collection,order_by_id=order_by_id,filter=filter,fields=fields))
        if as_json:
            if pretty:
                return json.dumps(result,indent=4)
            else:
                return json.dumps(result)
        elif as_pickle :
            return pickle.dumps(result)
        else:
            return result


    def count(self):
        return len(self.db.keys())

    def update_indexes(self,collection,key,data):
        """
            update the collection activeindexes
        """






# filters
def equal_filter(attribute,value):
    """
        return a filter of type entity['attribute'] == value

    """
    def _filter(entity):
        if entity[attribute] == value:
            return True
        return False
    return _filter

def list_filter(item_ids):
    """
        return a filter of type entity['id'] in  item_list

        @item_ids list of id
    """
    def _filter(entity):
        if entity['id'] in item_ids:
            return True
        return False
    return _filter





class ShelfModel(Store):
    """

    """



    def _create_custom_indexes(self):
        """

        """
        self._custom_indexes={}
        for collection in self.collections:
            self._custom_indexes[collection]={}
        return



    def get_by_index(self,collection,index_name,value):
        """
            @collection : tests , test-sets
            @index_name : parent-id , test-id
            @value  245,
        """
        try:
            entity_ids = self._custom_indexes[collection][index_name][value]
            # we found it return it
            return entity_ids
        except AttributeError:
            # no collection indexes create it
            self._create_custom_indexes()
        except KeyError:
            # no index corresponding ,
            pass
            #
        # check if collection is valid
        if not collection in self.collections:
            raise KeyError('Invalid Collection')
            # the collection is ok , go on

        # check index exits
        if not self._custom_indexes[collection].has_key(index_name):
            # no index index name : create it
            self._custom_indexes[collection][index_name]={}
            for e in self.iter_collection(collection):
                if index_name in e:
                    index_value = e[index_name]
                    if not index_value in self._custom_indexes[collection][index_name]:
                        self._custom_indexes[collection][index_name][index_value]=[]
                    self._custom_indexes[collection][index_name][index_value].append(e['id'])


        try:
            entity_ids = self._custom_indexes[collection][index_name][value]
            return entity_ids
        except KeyError:
            return []





if __name__=="__main__":

    # init logging
    logging.basicConfig(datefmt='%H:%M:%S',format='[%(levelname)s %(asctime)s] %(message)s', level=logging.DEBUG)


    db_path = "./export_syprunner/qc.db"
    collections = Store.collections




    sample_data = {

      "platform_version": {

        "mobiles" : {

            "388897e5" : {  "name": "Caller" , "pin": None , "sim": "0000", "tel":"0640412593"  },

            "e7f54be6":  {  "name": "Calee" , "pin": None , "sim": "0000", "tel":"0684820364"},

            "4df18692171e5fed": {  "name": "GT-I9300" ,"pin": "325698", "sim":None , "tel": "0681564613"},

            }
        }
    }




    def test():
        """

        """
        model = Store(db_path).open()
        print model.keys()
        model.close()


        with ShelfModel(db_path) as model:

            #model.create_pk()

            tests=list(model.iter_collection('tests'))
            t2 = list(model.iter_collection('tests',order_by_id=True))
            print model.keys()


            tests=list(model.iter_collection('tests'))

            # random_name = tests[3]['name']
            #
            # test_with_name = model.find('tests','name',random_name)


            # delete an entity
            model.delete('runs',3247)

            # delete collection
            model.delete_collection('tests')

            print

        print

        return


    def test_load_from_json():

        source= './export_syprunner/export.json'
        #source= './export_btic/export.json'
        #source= './export_oopro/export.json'


        with open(source,"rb") as fh :
            content=fh.read()

        json_data = json.loads(content)


        db  = Store(db_path)
        #db.raz()
        db.setup()    # * QcStore.collections)

        for collection , entities in json_data.iteritems():
            print collection

            if collection == "run-steps":
                for run , content in entities.iteritems():
                    for entity in content:
                        print entity['id']
                        if entity['id'] != '0':
                            db.put( collection, entity['id'], entity)
            elif collection == "assets-relations":
                pass

            else:
                for entity in entities:
                    print entity['id']
                    db.put( collection, entity['id'], entity)

        print db.keys()


        return


    def equal_filter(attribute,value):
        """
            return a filter of type entity['attribute'] == value

        """
        def _filter(entity):
            if entity[attribute] == value:
                return True
            return False
        return _filter

    def list_filter(item_ids):
        """
            return a filter of type entity['id'] in  item_list

            @item_ids list of id
        """
        def _filter(entity):
            if entity['id'] in item_ids:
                return True
            return False
        return _filter



    def test_query():

        db  = Store(db_path)


        for e in db.iter_collection('tests',order_by_id = True, filter = equal_filter('parent-id','692')):
            print e
            assert e['parent-id'] == '692'
            continue

        json_dump = db.dump_collection('tests',filter= equal_filter('parent-id','692'), as_json=True)
        print len(json_dump)

        pickle_dump = db.dump_collection('tests',filter= equal_filter('parent-id','692'), as_pickle=True)
        print len(pickle_dump)


        json_dump = db.dump_collection('tests',filter= equal_filter('parent-id','692'), as_json=True,pretty=True)
        print json_dump

        return


    def test_non_persistant():

        """



        :return:
        """

        class Mobiles(Store):
            """


            :return:
            """
            collections=['main','mobiles']


        s = Mobiles()


        collection = 'main'
        collection = 'mobiles'

        # populate database
        for key,value in sample_data['platform_version']['mobiles'].iteritems():
            s.add_entity(collection,key=key,entity_data=value)


        # queries
        for pk, e in s.iter_collection(collection,order_by_id = True, filter = equal_filter('sim','0000')):
            print e
            assert e['sim'] == '0000'
            continue

        json_dump = s.dump_collection(collection,filter= equal_filter('sim','0000'), as_json=True)
        print len(json_dump)

        pickle_dump = s.dump_collection(collection,filter= equal_filter('sim','0000'), as_pickle=True)
        print len(pickle_dump)


        json_dump = s.dump_collection(collection,filter= equal_filter('sim','0000'), as_json=True,pretty=True)
        print json_dump


        # find
        results = s.find(collection,'tel','0681564613')

        first = results[0]

        content = s.get(collection,first)

        # change item
        content['alias'] = 'Alice'

        s.put(collection,first,content)
        print first, content



        # delete key
        s.delete(collection,first)


        # check item has been removed from index tel
        results = s.find(collection,'tel','0681564613')
        assert results == []

        # check item has been removed from index tel
        results = s.find(collection,'tel','0640412593')
        assert len(results) == 1
        assert results[0] == "388897e5"


        # assert other entries are accessible
        results = s.find('mobiles','sim','0000')
        assert len(results)== 2

        return



    def test_with_store():
        """

        :return:
        """
        collection = 'main'
        with Store() as s:

            # populate database
            for key,value in sample_data['platform_version']['mobiles'].iteritems():
                s.add_entity(collection,key=key,entity_data=value)




        return


    ##### begins here #####

    #test()

    #test_load_from_json()
    #test_query()
    #test_model()

    test_non_persistant()
    test_with_store()