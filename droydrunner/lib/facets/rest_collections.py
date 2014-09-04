__author__ = 'cocoon'



from flask.views import MethodView, View

from flask import request

import inspect






class CollectionWithOperationApi(View):
    """

        implement collection with operation extension

    """
    methods = ['GET','POST','DELETE','PUT','HEAD']


    def dispatch_request(self,*args,**kwargs):
        """

        :return:
        """
        if kwargs.has_key('operation'):
            # it is an operation ( /collection/<item>/operation
            return self.operation(**kwargs)
        else:
            # it is a classical rest collection
            func_name = request.method.lower()
            if hasattr(self, func_name):
                m =  getattr(self,func_name)
                # method implemented ( get , post, put )
                return m(**kwargs)
            else:
                # method not implemented
                raise NotImplementedError

        # parameters = []
        #
        # method = request.method
        # parameters.append('***method=%s' % method)
        #
        #
        # for k,v in kwargs.iteritems():
        #     parameters.append("***%s:%s" % (k,v))
        #
        # return 'here: agents.dispatch_request, parameters:%s' % "".join(parameters)


    def get(self,item=None):
        """
            get /collection :         return list of items
            get /collection/<item> :  return item content

        """
        if item is None:
            # return list of users
            return NotImplementedError
        else:
            # return single item
            return NotImplementedError


    def post(self):
        """
            create an item

            POST /collection                        # create an item

        :return:
        """
        raise NotImplementedError


    def delete(self,item=None):
        """
            delete an item

            DELETE /collection/item_id> : delete single items

        """
        raise NotImplementedError


    def put(self,item):
        """

            update an item

            PUT /collection/<item>   : update single item

        """
        raise NotImplementedError


    @classmethod
    def register(cls,app,endpoint,url):
        """
            register urls to the flask app for the collection

            url                       and url/
            url/<item>                and  url/<item>/
            url/<item>/<operation>    and  url/<item>/operation/

        """

        u = ''
        for add in [ url, '/','<item>', '/' , '<operation>' , '/']:
            u += add
            app.add_url_rule(u, view_func=endpoint)
            continue

    @classmethod
    def create(cls,app,name,url=None):
        """

        :param cls:
        :param app: instance of flask app
        :param name: str  eg sessions
        :param url: str eg /sessions ,default to / + name
        :return:
        """
        if not url:
            url = '/' + name
        # create view
        view  = cls.as_view(name)
        # register view urls with app
        cls.register(app,view,url)
        return view




    def operation(self,**kwargs):
        """

            dispatch operation

        :param operation:
        :param item_id:
        :return:
        """
        # it is an operation

        operation = kwargs['operation']

        func_name = "op_%s" % operation
        if hasattr(self, func_name):
            m =  getattr(self,func_name)

            # method implemented ( op_<operation>  )
            return m(**kwargs)
        else:
            # method not implemented
            raise NotImplementedError('Bad method (%s) for operation: %s' % (request.method,operation))


    # def get_operation(self,operation,item_id=None):
    #     """
    #         get a form for an operation ( on item or collection )
    #     """
    #     raise NotImplementedError
    #
    # def post_operation(self,operation,item_id=None):
    #     """
    #         perform operation (on item or collection )
    #     """
    #     raise NotImplementedError
    #
    # def put_operation(self,operation,item_id=None):
    #     """
    #         configure an operation ( item or collection )
    #     """



class CollectionApi(MethodView):
    """
        standard collection
    """

    def get(self,item_id=None):
        """
            get item(s)
        """
        if item_id is None:
            # return list of users
            pass
        else:
            # return single item
            pass


    def post(self):
        # create an item
        pass


    def delete(self,item_id):
        """
            delete single item
        """
        pass


    def put(self,item_id):
        """
            update single item
        """
        pass

    @staticmethod
    def register_api(app,view, endpoint, url, pk='id', pk_type='int'):
        """
        """
        view_func = view.as_view(endpoint)
        app.add_url_rule(url, defaults={pk: None},
                         view_func=view_func, methods=['GET',])
        app.add_url_rule(url, view_func=view_func, methods=['POST',])
        app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                         methods=['GET', 'PUT', 'DELETE'])

    @classmethod
    def register(cls,app,endpoint,url,pk='item_id',pk_type='str'):
        """
            eg register_api(UserAPI, 'user_api', '/users/', pk='user_id')

        """
        cls.register_api(app,cls,endpoint=endpoint,url=url,pk=pk,pk_type=pk_type)