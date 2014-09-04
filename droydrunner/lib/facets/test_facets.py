__author__ = 'cocoon'




import json
from mimetype_facets import canonical , FacetsBuilder , FacetsScanner

from mimetype_facets import Template, data_to_dict ,dict_to_data , Item
# test section

sample_server= {
    "name": "welcome6",
    "created": {"$date": 1385551222419},
    "user": "phileas",
    "role": "server",
    "inbox": {"$oid": "5295c766a2ecd0c875b45b07"},
    "outbox": [
        {"$oid": "5295f2b7a2ecd0cf3bec7565"},
        {"$oid": "5295f39ba2ecd0cf67c2246c"},
        {"$oid": "5296248ca2ecd0d2c87ef74a"},
        {"$oid": "529624cea2ecd0d2c87ef74b"},
        {"$oid": "52962df4a2ecd0d3bb400c88"}],
    "_id": {"$oid": "5295c766a2ecd0c875b45b08"},
    "mode": "PASSIVE"
}

sample_collection= {
  "collection" : {
    "version" : "1.0",
    "href" : "http://127.0.0.1:5000/rendez-vous/server/",
    "links" : [
        {"href" : "URI", "rel" : "STRING", "prompt" : "STRING", "name" : "link0"}
        ],
    "items" :
    [
        # first item
       {
         "href" : "http://127.0.0.1:5000/rendez-vous/server/5295c766a2ecd0c875b45b08",
         "data" : [

              {"name" : "_id", "value" : "5295c766a2ecd0c875b45b08", "prompt" : "id"},
              {"name" : "name", "value" : "welcome6", "prompt" : "name"}

            ],
         "links" :                 [
              {"href" : "URI1", "rel" : "STRING", "prompt" : "STRING", "name" : "itlink1", "render" : "image"},
              {"href" : "URI2", "rel" : "STRING", "prompt" : "STRING", "name" : "itlink2", "render" : "link"},
              {"href" : "URI3", "rel" : "STRING", "prompt" : "STRING", "name" : "itlink3"}
            ]
       },
       # next item ...
    ],
    "queries" : [
        {
          "href" : "http://example.org/search",
          "rel" : "search",
          "prompt" : "Enter search string",
          "data" : [
            {"name" : "search", "value" : ""}
            ]
        },
    ],
    "template" :
        {
           "data" : [
              {"name" : "full-name", "value" : "", "prompt" : "Your Full Name"},
              {"name" : "email", "value" : "", "prompt" : "Your Email Address"},
           ]
        },
    "error" : { 'code': 200 ,'title': "OK" , 'message' : "" }
  }
}


sample_item = dict(

    name= "hello", role="client" , inbox="http://theclient/rendez-vous/inbox/123456", mode="passive"


)



def test_mimetype():
    """

    """
    m = FacetsBuilder.new()

    m.set("href","http://theserver/rendez-vous/server/subscribe/123456789")

    m.add_link('self',href= "http://theserver/rendez-vous/server/subscribe/123456789")


    item =Item.from_dict("http://myUri",sample_item)

    m.add_item(item)

    template_data= (
        ('user',"user name for the session"),
        ('client' , "client session url"),
        ('inbox','client inbox url'),
        ('outbox','client outbox url')
    )
    for name,prompt in template_data:
        m.add_template_data(name,prompt)


    template= Template.from_dict(sample_item)

    m.set_template(template)

    print m.content

    print m.to_json

    print m.pretty_print
    return


def test_FacetsScanner():
    """

        create
            from_json( json_data)

        check
            validate()

        query
            item_counts()
            has_template()
            has_error()

            has_links()



    """
    # create a facet object from json data
    json_data = json.dumps(sample_collection)
    facet = FacetsScanner.from_json(json_data)

    # check it
    facet.validate()

    print "number of item : %d" % facet.item_count()


    data_field = [
          {"name" : "full-name", "value" : "J. Doe", "prompt" : "Full Name"},
          {"name" : "email", "value" : "jdoe@example.org", "prompt" : "Email"}
        ]
    dic = facet.data_to_dict(data_field)
    print "transform data :\n %s \n to dict:\n %s" % (data_field,dic)

    print "facet prettyprint: \n%s" % facet.pretty_print

    items=facet.items()
    item1 = facet.item(items[0])

    queries=facet.queries()
    query1 = facet.query(queries[0])

    links=facet.links()
    link1 = facet.link(links[0])

    template = facet.template()


    item_values=facet.Item().values()

    item= facet.Item()

    item_links = item.links()
    item_href = item.href
    item_values = item.values()


    return


def test_helpers():
    """

    """
    data_field = [
          {"name" : "full-name", "value" : "J. Doe", "prompt" : "Full Name"},
          {"name" : "email", "value" : "jdoe@example.org", "prompt" : "Email"}
        ]
    dic = data_to_dict(data_field)
    print "transform data :\n %s \n to dict:\n %s" % (data_field,dic)

    data = dict_to_data(dic)
    print "transform dict :\n %s \n to data:\n %s" % (dic,data)


    canonic = canonical(sample_collection)

    return

### begins here

test_helpers()
test_mimetype()
test_FacetsScanner()

