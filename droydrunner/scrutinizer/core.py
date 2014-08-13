# -*- coding: utf8 -*-
__author__ = 'cocoon'


from xml.etree import ElementTree as ET
import hashlib



class UiNode(object):
    """
        a node of an xml dump

    """
    def __init__(self,element):
        """
        """
        self.element = element

    def short_id(self):
        """
            return a short name

            can be
                1) resourceId without the packageName    (com.android.incallui:id/bluetoothButton -> bluetoothButton)
        """
        short = None

        resourceId = self.element.attrib['resource-id']
        packageName = self.element.attrib['package']

        package_id = "%s:id/" % packageName

        if package_id in resourceId:
            # make a short id
            short = resourceId[len(package_id):]
        else:
            # cannot make a short id
            short = resourceId
        return short


    def class_id(self):
        """
            return a class,index identifier
        :return:
        """
        className = self.element.attrib['class']
        index = self.element.attrib['index']
        return "%s,%s" % (className,index)




    def hash(self):
        """
            return a hash of all attributes key:value and number of chidren

        """
        sig = hashlib.md5()
        # compute hash for attribs
        for k,v in self.element.attrib.iteritems():
            h = u"%s:%s;" % (k,v)
            #h = unicode.encode(h,encoding='utf-8')
            sig.update(h.encode('utf8'))
        # add hash for len
        h = str(len(self.element))
        sig.update(h)
        return sig.hexdigest()


class Scrutinizer(object):
    """

        a class around an xml dump of an android screen


    """

    def __init__(self, root ):
        """

        :param element:
        :return:
        """
        self.root = root

        # compute hash table of all elements
        self._elements = self.hashes()



    @classmethod
    def from_file(cls,filename):
        """


        :param filename:
        :return:
        """
        xml = ET.parse(filename)
        root = xml.getroot()
        return cls(root)


    def hashes(self):
        """

        :return: a dict of hashes element
        """
        _elements = {}
        for element in self.root.iter():
            hash = UiNode(element).hash()
            _elements[hash] = element
        return _elements


    def iter(self,root=None, check=None,filter=None):
        """

            iter from a root element applying filter and checks


        :param root:
        :param filter_on:
        :return:
        """
        if root is None:
            root = self.root
        if check is None:
            check = []
        else:
            if isinstance(check,str):
                check = [check,]
        if filter is None:
            filter={}
        for element in root.iter():
            # checks ( clickable or long-clickables or  selected enabled , checked )
            any_check = False
            if len(check):
                # there is at least a check so verify at least one os one
                for c in check:
                    if c in element.attrib:
                        if element.attrib[c] == 'true':
                            any_check = True
                            break
            else:
                # no check : continue with it
                any_check = True
            if any_check:
                # filter it
                filter_hits = 0
                for filter_name,filter_value in filter.iteritems():
                    if filter_name in element.attrib:
                        if filter_value == element.attrib[filter_name]:
                            filter_hits += 1
                            continue
                        else:
                            break
                    else:
                        break
                if filter_hits == len(filter)  :
                     # all filters are matched
                     yield element
                continue

    def uniques(self,nodes):
        """

            scan nodes to find unique elements
                1) resource: unique if resource-id is unique

                2) class: unique if class an ine-dex are uniques


        :param nodes: array of etree element
        :return:
        """
        by_resource = {}
        by_class = {}
        others =[]
        for node in nodes:
            # search unique resource id
            ressourceId = node.attrib['resource-id']
            if ressourceId not in by_resource:
                by_resource[ressourceId] = node
            else:
                # search unique class/index
                classId = "%s,%s" % (node.attrib['class'],node.attrib['index'])
                if classId not in by_class:
                    by_class[classId] = node
                else:
                    others.append(node)
        result = dict( by_resource=by_resource,by_class=by_class,others=others)
        return result



class Searcher(Scrutinizer):
    """
        a high level scrutinizer
    """


    textview_class = 'android.widget.TextView'
    tab_patterns = ['android.app.ActionBar$Tab',]


    def find_tabs(self,root=None,selected=None):
        """
            iter to find tabs
                if selected is None: yield all tabs
                            is true: only selected tabs
                            is false only unselected tabs


        :return:
        """
        #tab_patterns = ['android.app.ActionBar$Tab',]

        tabs = []

        # collect all tabs
        for tab in self.tab_patterns:
            r = list(self.iter( root=root,filter = {'class':tab}))
            tabs.extend(r)
        if selected is None:
            # return all tabs
            return tabs
        else:
            # filter tabs
            if selected is True:
                sel = 'true'
            else:
                sel = 'false'
            r = [ e for e in tabs if e.attrib['selected']== sel ]
            return r


    def find_first_textview(self,element):
        """

            starting with element , find the first child with class text view

        :param element:
        :return:
        """
        try:
            child = element[0]
            if child.attrib['class'] == self.textview_class:
                return child
            else:
                # try deeper
                return self.find_first_textview(child)

        except IndexError:
            # no more children
            return None







