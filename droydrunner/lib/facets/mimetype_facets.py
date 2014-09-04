"""

    implements the mimetype facets



    structure



"""
import json
import pprint
from copy import deepcopy




class FacetsErrors(Exception):
    """

    """
    pass

class MimetypeFacets():
    """
        derived from : application/vnd.Collection+JSON

    """
    # name of the mimetype
    #mimetype = "application/vnd.Facets+JSON"
    mimetype='application/collection+json'

    def __init__(self,data):
        """
            @data: dict : the mimetype data
        """
        self._data=data

    @classmethod
    def from_json(cls,json_data):
        """
            build facet from json
        """
        data = json.loads(json_data)
        facets = cls(data)
        return facets



class CollectionFacets():
    """


        // sample colleciton.json map
        {
          "collection" :
          {
            "version" : "1.0",
            "href" : URI,
            "links" : [ARRAY],
            "items :
            [
               {
                 "href" : URI,
                 "data" : [ARRAY],
                 "links" : [ARRAY]
               },
               ...
            ],
            "queries" : [ARRAY],
            "template" :
            {
               "data" : [ARRAY]
            },
            "error" : {OBJECT}
          }
        }

    """


class ItemsFacets():
    """
        // sample items array
        {
          "collection" :
          {
            "version" : "1.0",
            "href" : URI,
            "items" :
            [
              {
                "href" : URI,
                "data" : [ARRAY],
                "links" : [ARRAY]
              },
              ...
              {
                "href" : URI,
                "data" : [ARRAY],
                "links" : [ARRAY]
              }
            ]
          }
        }

    """

class LinksFacets():
    """

        The links arrayThe links array is an optional child property of the items
                  array. It contains one or more anonymous objects, each with five
                  possible properties:
                    href (REQUIRED),
                    rel (REQURIED),
                    name (OPTIONAL),
                    render(OPTIONAL),
                    prompt (OPTIONAL


        // sample links array
        {
          "collection" :
          {
            "version" : "1.0",
            "href" : URI,
            "items" :
            [
              {
                "href" : URI,
                "data" : [ARRAY],
                "links" :
                [
                  {"href" : URI, "rel" : STRING, "prompt" : STRING, "name" : STRING, "render" : "image"},
                  {"href" : URI, "rel" : STRING, "prompt" : STRING, "name" : STRING}, "render" : "link",
                  ...
                  {"href" : URI, "rel" : STRING, "prompt" : STRING, "name" : STRING}
                ]
              }
            ]
          }

    """


class DataFacets():
    """
        The data arrayThe data array is a child property of the items
                  array and the template object. It contains one or more
                  anonymous data objects.
                  Each object can have any of three possible properties:
                    name (REQUIRED),
                    value (OPTIONAL),
                    prompt (OPTIONAL).

                  Below is an example of a data array within an
                  item. This item has two data elements
                  (full-name and email):// example of a data array
        "items" :
        [
          {
            "href" : "http://example.org/friends/jdoe",
            "data" :
            [
              {"name" : "full-name", "value" : "J. Doe", "prompt" : "Full Name"},
              {"name" : "email", "value" : "jdoe@example.org", "prompt" : "Email"}
            ]
          }
        ]

    """


class TemplateFacets():
    """
        The template objectThe template object contains all of the input
                  elements used to add or edit collection items. It is a top-level
                  document property and should contain a list of one or more
                  data elements. Essentially, the template object is the
                  equivalent in this design of the HTML FORM and INPUT elements. The
                  template object has a variable number of data elements, each
                  representing a name/value pair to be sent to the server for
                  processing. Whenever a client wants to compose a payload for adding
                  a new item, this is the guide. It should also be used when updating
                  an existing item:// sample template object
        {
          "template" :
          {
            "data" :
            [
              {"name" : "full-name", "value" : "", "prompt" : "Your Full Name"},
              {"name" : "email", "value" : "", "prompt" : "Your Email Address"}
            ]
          }
        }

    """


class ErrorFacets():
    """

        The error objectThe error object contains additional information
              on the latest error condition reported by the server. It is a
              top-level document property. The following elements can appear as
              child properties: code, message, and
              title.// sample error object
        {
          "error" :
          {
            "title" : STRING,
            "code" : STRING,
            "message" : STRING
          }
        }

    """


class QueriesFacets():
    """

        Query TemplatesClients that support the Collection+JSON media type SHOULD be able
              to recognize and parse query templates found within responses. Query
              templates consist of a data array associated with an href
              property. The queries array supports query templates.For query templates, the name/value pairs of the data array set
              are appended to the URI found in the href property
              associated with the queries array (with a question mark as separator)
              and this new URI is sent to the processing agent:// query template sample
        {
          "queries" :
          [
            {
              "href : "http://example.org/search",
              "rel" : "search",
              "prompt" : "Enter search string",
              "data" :
              [
                {"name" : "search", "value" : ""}
              ]
            }
          ]
        }

    """


def data_to_dict(data,key='name'):
    """
        transform a facet data element in a dictionary

        return dict with name field as key

        from
            [
                { 'name': name1 , 'value': 'prompt': ...
                { 'name': name2  ....
            ]
        to
            {
                name1: { value: , prompt:
                name2: { value: , prompt:
:
    """
    res ={}
    for element in data:
        res[element[key]] =  {}
        for field,value in element.iteritems():
            if not field == key:
                res[element[key]][field] = value
    return res
facet2dict = data_to_dict

def dict_to_data(dic,key='name'):
    """

        transform a dict to a facet element
        from
            {
                name1: { value: , prompt:
                name2: { value: , prompt:


        to
            [
                { 'name': name1 , 'value': 'prompt': ...
                { 'name': name2  ....
            ]
    """
    data=[]
    for el_name in sorted(dic.keys()):
        el_value = dic[el_name]
        # add key
        el_value[key] = el_name
        data.append(el_value)
    return data
dict2facet=dict_to_data

def canonical(facet_data):
    """
        transform a native facet format to a canonical format (easier for query)


        facet_data ->

         collection:
            href: ""
            error:
                code: ""
                title: ""
                message: ""
            template:
                data:
                    -
                        name: ""
                        value: ""
                        prompt: ""
                ]
            items:
                -
                    href: ""
                    data:
                        -
                            name: ""
                            prompt: ""
                            value: ""
                    links:
                        -
                            name: ""
                            href: ""
                            rel: ""
                            prompt: ""
                            render: ""

            links:
                -
                    name: ""
                    href: ""
                    rel: ""
                    prompt: ""
                    render: ""

            version: ""


        canonical_data ->

            href: ""
            version: ""
            error:
                code: ""
                title: ""
                message: ""

            template:
                data:
                    $name:
                        prompt: ""
                        value: ""
            items:
                $oid:
                    href: ""
                    data:
                        $name:
                            prompt: ""
                            value: ""
                    links:
                        $name:
                            href: ""
                            rel: ""
                            prompt: ""
                            render: ""
            links:
                $name:
                    href: ""
                    rel: ""
                    prompt: ""
                    render: ""




    """
    canonic = deepcopy(facet_data['collection'])
    canonic['template']['data'] = data_to_dict(facet_data['collection']['template']['data'])
    if canonic.has_key('links'):
        canonic['links'] = data_to_dict( facet_data['collection']['links'])
    if canonic.has_key('items'):
        canonic['items'] = FacetsItemScanner.build_items_dict(facet_data['collection']['items'])
    if canonic.has_key('queries'):
        canonic['queries'] = FacetsQueriesScanner.build_queries_dict(facet_data['collection']['queries'])
    return canonic



class FacetsElement():
    """
        base class for facets element
    """
    mimetype='application/collection+json'

    _empty =  { "data":[] }

    def __init__(self,data,is_form=False):
        """
            data is dict representing a facet

            store it in _element
        """
        self._element = data
        self._type = None
        self._is_form = is_form

    @classmethod
    def new(cls):
        """
            build an empty item
        """
        item = deepcopy(cls._empty)
        return cls(item)

    @property
    def content(self):
        return self._element

    @property
    def to_json(self):
        return json.dumps(self.content)

    @property
    def pretty_print(self):
        return pprint.pformat(self.content)


    @property
    def html(self):
        lines=self.pretty_print.split('\n')
        return "<br>".join(lines)



class FacetsItemScanner():
    """
        represents collection items , for easy query on it

        [
            # first item
           {
             "href" : "http://127.0.0.1:5000/rendez-vous/server/5295c766a2ecd0c875b45b08",
             "data" : [

                  {"name" : "_id", "value" : "5295c766a2ecd0c875b45b08", "prompt" : "id"},
                  {"name" : "name", "value" : "welcome6", "prompt" : "name"}

                ],
             "links" : []
           },
           # next item ...
        ]


    """
    def __init__(self,items_data):
        """

        """
        self._native={}
        self._canonical={}
        self._short={}

        self._data = items_data
        self.content = self.build_items_dict(items_data)


    @classmethod
    def from_native(cls,native_facet_data):
        """

        """


    @classmethod
    def from_canonical(cls,canonical_facet_data):
        """

        """


    @classmethod
    def build_items_dict(cls,items_data):
        """
            build item from native facet format
        """
        items={}
        # build internal data structure for queryng
        for item_data in items_data:
            href = item_data['href']
            oid = cls.extract_oid_from_href(href)
            data =  data_to_dict(item_data['data'])
            links = data_to_dict(item_data['links'])

            items[oid] = dict( href= href , links = links ,data = data)
        return items

    @classmethod
    def extract_oid_from_href(cls,href):
        """
            extract oid from href , the last part is supposed to be an oid

            eg
            "http://127.0.0.1:5000/rendez-vous/server/5295c766a2ecd0c875b45b08" -> 5295c766a2ecd0c875b45b08

        """
        oid = href.split('/')[-1]
        return oid



    # item getters
    def item_href(self,oid):
        """

        """
        return self._canonical[oid]['href']

    def item_data(self,oid):
        """
            return a dict representing the item

        """
        to_dict={}
        for name,data in self._canonical[oid]['data'].iteritems():
            to_dict[name] = data['value']
        return to_dict

    def item_links(self,oid):
        """

        """
        to_dict={}
        for name,data in self._canonical[oid]['links'].iteritems():
            to_dict[name] = data['value']
        return to_dict


class FacetsQueriesScanner():
    """
        represents collection queries , for easy query on it

          [
            # first query
            {
              "href : "http://example.org/search",
              "rel" : "search",
              "prompt" : "Enter search string",
              "data" :
              [
                {"name" : "search", "value" : ""}
              ]
            },
            # next query
          ]


    """
    def __init__(self,data):
        """

        """
        self._data = data
        self.content = self.build_queries_dict(data)

    @classmethod
    def build_queries_dict(cls,queries_data):
        """

        """
        result={}
        # build internal data structure for quering
        for item_data in queries_data:
            href = item_data['href']
            rel = item_data['rel']
            prompt = item_data['rel']
            data =  data_to_dict(item_data['data'])

            #TODO we use rel as key for queries, ensure rel is unique
            result[rel] = dict( href= href , prompt=prompt ,data = data)
        return result




class FacetsScanner(FacetsElement):
    """
        scan an existing facet response

        query on it


            from_json(data)    create from a json text



    """
    @classmethod
    def from_json(cls,json_facets):
        """
            convert json to dict and return FacetsScanner instance

        """
        data = json.loads(json_facets)

        # determine type of collection:    collection or template
        if data.has_key('template'):
            # it is a template facet
            obj = cls(data)
            obj._type="template"
        else:
            obj = cls(data['collection'])
            obj._type="collection"
        return obj

    @property
    def content(self):
        if self._type == 'collection':
            return {'collection': self._element}
        elif self._type == 'template':
            return self._element
        return self._element


    def validate(self):
        """
            check data is a valid facet mimetype

        """
        #collection = self._element['collection']

        # transform self._element in a self._canonical
        self._canonical = canonical({'collection' : self._element})
        return self

    def _section_count(self,section_name):
        """

            section_name is an array section of collection (in items,links,queries,template,version , href
        """
        if section_name in ('items','links','queries'):
            # check array count
            try:
                return len(self._element[section_name])
            except KeyError:
                return 0
        elif section_name == 'template':
            # check template has data elements
            try:
                return len(self._element['template']['data'])
            except KeyError:
                return 0
        elif section_name == 'error':
            try:
                err =  self._element['error'] ['code']
                if str(err) != '':
                    # an error has been set
                    return 1
            except KeyError:
                pass
            return 0
        else:
            # href , version
            if self._element[section_name] == "":
                return 0
            return 1

    def _has_section(self,section_name):
        """

        """
        if self._section_count(section_name) > 0:
            return True
        return False


    def item_count(self):
        """
            return number of items
        """
        return self._section_count('items')


    def has_item(self):
        """
            return True if facet has item
        """
        return self._has_section('items')


    def template_count(self):
        """
            return the number of template data element
        """
        return self._section_count('template')


    def has_template(self):
        """
            return True if template data is non empty
        """
        return self._has_section('template')


    def has_error(self):
        """
            return true if error fields not empty
        """
        return self._has_section('error')


    def item_by_oid(self,oid):
        """

        """
        try:
            return self._item_by_oid[oid]
        except AttributeError:
            # build index
            self._item_by_oid={}


    def data_to_dict(self,data):
        return data_to_dict(data)

    @classmethod
    def canonical_to_dict(cls,data, selector="value"):
        """

        """
        result={}
        for name in data.keys():
            result[name]= data[name][selector]
        return result

    def items(self):
        """
            return a list of availables items (oid)
        """
        return sorted(self._canonical['items'].keys())

    def item(self,name):
        """
            return canonical form of item (oid)

        """
        return self._canonical['items'][name]

    def first_item(self):
        """
            return the canonical form of the first item in collection
        """
        first = self.item(self.items()[0])
        return first


    def queries(self):
        """
            return availables query names (rel)

        """
        return sorted(self._canonical['queries'].keys())

    def query(self,name):
        """
            return canonical form of a given query (rel)
        """
        return self._canonical["queries"][name]

    def links(self):
        """
            return availables links names (name)

        """
        return sorted(self._canonical['links'].keys())

    def link(self,name):
        """
            return canonical form of a given query
        """
        return self._canonical["links"][name]

    def template(self):
        """
            return canonical form of template
        """
        return self._canonical['template']

    def version(self):
        """

        """
        return self._canonical['version']

    def href(self):
        """

        """
        return self._canonical['href']


    # high level methods for data (return dictionaries


    #TODO: remove it  see canonical_data_to_dict
    def _canonical_data_to_dict(self,data):
        """
            return a dict from a data field

            template:data , items:$oid:data

            from :
                key1:
                    value: "v1"
                    ...
                key2:
                    value:"v2"
                    ...
                ...
            to:

                key1: v1
                key2: v2

        """
        result={}
        for name in data:
            result[name]=data[name]['value']
        return result


    def template_data(self):
        """
            return a dict from template data
        """
        data=self.template()['data']
        return self._canonical_data_to_dict(data)

    #
    # Item helper
    #
    class _Item():
        """
            a class to handle item

            use canonical


            href()
            values()   return a dict of data , name,value

        """
        def __init__(self,parent,oid=None):
            """
            """
            self.parent=parent
            if oid is None:
                # no oid : select first one
                oid = self.parent.items()[0]
            self.oid=oid
            # load canonical data for this item
            self._data = self.parent.item(oid)

        @property
        def href(self):
            return self._data['href']


        def values(self):
            """
                return a dict of item values :  attribute name , value
            """
            return self.parent.canonical_to_dict(self._data['data'])


        def links(self):
            """
                return canonical item links
            """
            return self._data['links']

        def link(self,name):
            """
                return item link  : { rel: , href: )
            """
            return self._data['links'][name]

    def Item(self,oid=None):
        """
            return a _Item instance for easy query
        """
        return self._Item(self,oid)

    #
    # Link helper
    #
    class _Links():
        """
            a class to handle links

            href(name)
            rel(name)


        """
        def __init__(self,data):
            """
                @data: dict : canonical data for links
            """

            self._data = data

        def href(self,name):
            """
                return the href of the given name link
            """
            return self._data[name]['href']

        def with_rel(self,rel_name):
            """
                return array of link names with this rel attribute
            """
            rels=[]
            for key,value in self._data.iteritems():
                if value['rel'] == rel_name:
                    rels.append(key)
            return rels

        def find(self,**kwargs):
            """
                find a specific link  with model :  rel=agent ,

                return an array of dict
            """
            raise NotImplementedError



    def Links(self,data):
        """
            return a _Item instance for easy query
        """
        return self._Links(data)







class Data(list):
    """
        "data" :
            [
              {"name" : "full-name", "value" : "J. Doe", "prompt" : "Full Name"},
              {"name" : "email", "value" : "jdoe@example.org", "prompt" : "Email"}
            ]


    """
    @classmethod
    def from_dict(self,hash):
        """


        """
        data=Data()
        for key, value in hash.iteritems():
            data.append(dict(name=key,value=value,prompt=key))
        return data

class Query(FacetsElement):
    """
          "queries" :
          [
            {
              "href : "http://example.org/search",
              "rel" : "search",
              "prompt" : "Enter search string",
              "data" :
              [
                {"name" : "search", "value" : ""}
              ]
            }
          ]

    """
    _empty = { 'href':"", 'rel': "" , 'prompt':'empty' , 'data': []}

    @classmethod
    def from_dict(cls,hash):
        """
            build an item from a dictionary with empty links
        """
        obj = deepcopy(cls._empty)
        obj['data'] = Data.from_dict(hash)
        return cls(obj)

    @classmethod
    def from_keys(cls,href='..',rel= "", prompt='empty'):
        """
            build an item from a dictionary with empty links
        """
        obj = deepcopy(cls._empty)
        obj['href'] = href
        obj['prompt'] = prompt
        #obj['data'] = Data.from_dict({})
        return cls(obj)

    def add_data(self,name,value=""):
        """
            add data
        """
        self._element['data'].append(dict(name=name,value=value))


class Template(FacetsElement):
    """
          "template" :
          {
            "data" :
            [
              {"name" : "full-name", "value" : "", "prompt" : "Your Full Name"},
              {"name" : "email", "value" : "", "prompt" : "Your Email Address"}
            ]
          }
    """
    _empty =  { "data":[] }


    @classmethod
    def from_dict(cls,hash):
        """
            build an item from a dictionary with empty links
        """
        obj = deepcopy(cls._empty)
        obj['data'] = Data.from_dict(hash)
        return cls(obj)

    def add_data(self,name,prompt=None,value=""):
        """
            add data
        """
        if not prompt:
            prompt = name
        self._element['data'].append(dict(name=name,prompt=name,value=value))

    #@property
    #def content(self):
    #    return {'template': self._element}


class Item(FacetsElement):
    """

        item  = {
        "href" : "",
         "data" : [],
         "links" : []
        }


    """
    _empty = { "href":"", "data":[], "links": []}


    @classmethod
    def from_dict(cls,href,hash):
        """
            build an item from a dictionary with empty links
        """
        item = deepcopy(cls._empty)
        item['href'] = href
        item['data'] = Data.from_dict(hash)
        return cls(item)

    def add_link(self,rel,href,name='',prompt='',render='link'):
        """
        """
        if not name:
            name=rel
        if not prompt:
            prompt=name

        self._element["links"].append( { 'rel':rel,'href':href,'name':name,'prompt':prompt,'render':render})

    def set(self,key,value):
        """
        """
        self._element[key]=value



class FacetsBuilder(FacetsElement):
    """

    """

    Item=Item
    Template=Template
    Query=Query

    _empty = {

        "version" : "0.1",
        "href" : "",
        "links" : [],
        "items" : [],
        "queries" : [],
        "template" : {
           "data" : []
            },
        "error" : {}
        }

    _empty_form = {
        "template" : {
           "data" : []
            },
        }

    @classmethod
    def new(cls,href="",version="0.1"):
        """
            build an empty item
        """
        empty = deepcopy(cls._empty)
        element = cls(empty)
        element.set("href",href)
        element.set("version",version)
        return element

    @classmethod
    def new_form(cls,template_dictionnary):
        """
            make a forms from a dict :
                template { ..

        """
        empty = deepcopy(cls._empty_form)
        element = cls(empty,is_form=True)

        temp = Template.from_dict(template_dictionnary)
        element.set_template(temp)

        return element

    def set(self,key,value):
        """
        """
        assert key in ["version","href","links","items","queries","template","error"]
        if key in ['links',"items","queries"]:
            assert isinstance(value,[])
        if key in ["template","error"]:
            assert isinstance(value,dict)
        self._element[key]=value

    def add_to(self,key,value):
        """
        """
        assert key in ['links',"items","queries"]
        self._element[key].append(value)

    def add_link(self,rel,href,name='',prompt='',render='link'):
        """
        """
        if not name:
            name=rel
        if not prompt:
            prompt=name

        self.add_to("links", { 'rel':rel,'href':href,'name':name,'prompt':prompt,'render':render})

    def add_item(self,item):
        """
        """
        assert isinstance(item,Item)
        self._element['items'].append(item.content)

    def add_query(self,element):
        """
        """
        assert isinstance(element,Query)
        self._element['queries'].append(element.content)

    def set_template(self,template):
        """

        """
        if isinstance(template,Template):
            value = template.content
        else:
            assert isinstance(template,dict)
            value = template
        self._element['template'] = value

    def add_template_data(self,name,prompt=None,value=""):
        """
            add data
        """
        if not prompt:
            prompt = name
        self._element['template']['data'].append(dict(name=name,prompt=prompt,value=value))

    def set_error(self,code,title="",message=""):
        """
          "error" :
          {
            "title" : STRING,
            "code" : STRING,
            "message" : STRING
          }
        """
        error= dict(code=str(code),title=title,message=message)
        self._element['error'] = error



    @property
    def content(self):
        if self._is_form:
            # it is a form (template)
            return self._element
        else:
            # it is a collections
            return {'collection': self._element}




# if __name__== "__main__":
#
#     # test section
#
#
#
#     sample_server= {
#         "name": "welcome6",
#         "created": {"$date": 1385551222419},
#         "user": "phileas",
#         "role": "server",
#         "inbox": {"$oid": "5295c766a2ecd0c875b45b07"},
#         "outbox": [
#             {"$oid": "5295f2b7a2ecd0cf3bec7565"},
#             {"$oid": "5295f39ba2ecd0cf67c2246c"},
#             {"$oid": "5296248ca2ecd0d2c87ef74a"},
#             {"$oid": "529624cea2ecd0d2c87ef74b"},
#             {"$oid": "52962df4a2ecd0d3bb400c88"}],
#         "_id": {"$oid": "5295c766a2ecd0c875b45b08"},
#         "mode": "PASSIVE"
#     }
#
#     sample_collection= {
#       "collection" : {
#         "version" : "1.0",
#         "href" : "http://127.0.0.1:5000/rendez-vous/server/",
#         "links" : [
#             {"href" : "URI", "rel" : "STRING", "prompt" : "STRING", "name" : "link0"}
#             ],
#         "items" :
#         [
#             # first item
#            {
#              "href" : "http://127.0.0.1:5000/rendez-vous/server/5295c766a2ecd0c875b45b08",
#              "data" : [
#
#                   {"name" : "_id", "value" : "5295c766a2ecd0c875b45b08", "prompt" : "id"},
#                   {"name" : "name", "value" : "welcome6", "prompt" : "name"}
#
#                 ],
#              "links" :                 [
#                   {"href" : "URI1", "rel" : "STRING", "prompt" : "STRING", "name" : "itlink1", "render" : "image"},
#                   {"href" : "URI2", "rel" : "STRING", "prompt" : "STRING", "name" : "itlink2", "render" : "link"},
#                   {"href" : "URI3", "rel" : "STRING", "prompt" : "STRING", "name" : "itlink3"}
#                 ]
#            },
#            # next item ...
#         ],
#         "queries" : [
#             {
#               "href" : "http://example.org/search",
#               "rel" : "search",
#               "prompt" : "Enter search string",
#               "data" : [
#                 {"name" : "search", "value" : ""}
#                 ]
#             },
#         ],
#         "template" :
#             {
#                "data" : [
#                   {"name" : "full-name", "value" : "", "prompt" : "Your Full Name"},
#                   {"name" : "email", "value" : "", "prompt" : "Your Email Address"},
#                ]
#             },
#         "error" : { 'code': 200 ,'title': "OK" , 'message' : "" }
#       }
#     }
#
#
#     sample_item = dict(
#
#         name= "hello", role="client" , inbox="http://theclient/rendez-vous/inbox/123456", mode="passive"
#
#
#     )
#
#
#
#     def test_mimetype():
#         """
#
#         """
#         m = FacetsBuilder.new()
#
#         m.set("href","http://theserver/rendez-vous/server/subscribe/123456789")
#
#         m.add_link('self',href= "http://theserver/rendez-vous/server/subscribe/123456789")
#
#
#         item =Item.from_dict("http://myUri",sample_item)
#
#         m.add_item(item)
#
#         template_data= (
#             ('user',"user name for the session"),
#             ('client' , "client session url"),
#             ('inbox','client inbox url'),
#             ('outbox','client outbox url')
#         )
#         for name,prompt in template_data:
#             m.add_template_data(name,prompt)
#
#
#         template= Template.from_dict(sample_item)
#
#         m.set_template(template)
#
#         print m.content
#
#         print m.to_json
#
#         print m.pretty_print
#         return
#
#
#     def test_FacetsScanner():
#         """
#
#             create
#                 from_json( json_data)
#
#             check
#                 validate()
#
#             query
#                 item_counts()
#                 has_template()
#                 has_error()
#
#                 has_links()
#
#
#
#         """
#         # create a facet object from json data
#         json_data = json.dumps(sample_collection)
#         facet = FacetsScanner.from_json(json_data)
#
#         # check it
#         facet.validate()
#
#         print "number of item : %d" % facet.item_count()
#
#
#         data_field = [
#               {"name" : "full-name", "value" : "J. Doe", "prompt" : "Full Name"},
#               {"name" : "email", "value" : "jdoe@example.org", "prompt" : "Email"}
#             ]
#         dic = facet.data_to_dict(data_field)
#         print "transform data :\n %s \n to dict:\n %s" % (data_field,dic)
#
#         print "facet prettyprint: \n%s" % facet.pretty_print
#
#         items=facet.items()
#         item1 = facet.item(items[0])
#
#         queries=facet.queries()
#         query1 = facet.query(queries[0])
#
#         links=facet.links()
#         link1 = facet.link(links[0])
#
#         template = facet.template()
#
#
#         item_values=facet.Item().values()
#
#         item= facet.Item()
#
#         item_links = item.links()
#         item_href = item.href
#         item_values = item.values()
#
#
#         return
#
#
#     def test_helpers():
#         """
#
#         """
#         data_field = [
#               {"name" : "full-name", "value" : "J. Doe", "prompt" : "Full Name"},
#               {"name" : "email", "value" : "jdoe@example.org", "prompt" : "Email"}
#             ]
#         dic = data_to_dict(data_field)
#         print "transform data :\n %s \n to dict:\n %s" % (data_field,dic)
#
#         data = dict_to_data(dic)
#         print "transform dict :\n %s \n to data:\n %s" % (dic,data)
#
#
#         canonic = canonical(sample_collection)
#
#         return
#
#     ### begins here
#
#     test_helpers()
#     test_mimetype()
#     test_FacetsScanner()
#
#     print