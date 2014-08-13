__author__ = 'cocoon'




class UiSelector(object):
    """

    """
    def __init__(self,device):
        """

        """
        self.device = device


    def get_child_by_index(self,element,index):
        return element.child(index=index)


    def get_by_resourceId(self,resourceId):
        return self.device(resourceId=resourceId)

    def traverse_with_index(self,element,indexes):
        """
            go down the hierarchy start with element and apply child index for each index in indexes

        :param element: the start element
        :param indexes: array of int representing index to reach the target  eg 0 1 0
        :return:
        """
        for index in indexes:
            element=element.child(index=int(index))
        return element


    def select_textview_child_by_index(self,element,index):
        """

        :param index:
        :return:
        """

        if isinstance(index,int):
            # select by index
            return element.child(className='android.widget.TextView', index=index)
        else:
            # select by text
            return element.child(className='android.widget.TextView', text=index)


    def select_tab(self,resource_id,path,index):
        """

            select a tab starting with resourceId , navigate path and select index


            eg select_tab('com.sec.android.app.launcher:id/hotseat', '0/0' , 0 )


        :param resource_id:
        :param path: str index separated with /  eg "0/1/0
        :param index: position in the menu (0..) or text
        :return:
        """
        indexes = path.split('/')

        # find the root element by id
        element = self.get_by_resourceId(resource_id)

        # navigate down the path
        for i in indexes:
            element = element.child(index= int(i))

        # return the selected item selector
        return self.select_textview_child_by_index(element,index)



# class TabSelection(UiSelector):
#     """
#
#         a selection menu
#
#
#         path:  hotseat/0/0 for a id / view search
#
#         or   id:hotseat/view:0/view:0
#
#
#
#         resourceId pattern  :
#
#     """
#
#
#     def select(self,index):
#         """
#
#         :param index:
#         :return:
#         """
#         element = self.get_base_menu()
#
#         if isinstance(index,int):
#             return element.child(className='android.widget.TextView', index=index)
#         else:
#             return element.child(className='android.widget.TextView', text=index)
#
#
#     def get_base_menu(self,path):
#         """
#
#         """
#         indexes = path.split('/')
#         element = self.device(resourceId=self.resourceId)
#
#         for index in indexes:
#             element = self.get_child_by_index(index=int(index))
#         return element
#
#
#
#
# class HomeContainer(TabSelection):
#     """
#
#         the home panel with application and widgets
#
#
#     """
#     data = {
#         'resourceId':'com.sec.android.app.launcher:id/home_container',
#         'path' : "0/0/0"
#     }
#
