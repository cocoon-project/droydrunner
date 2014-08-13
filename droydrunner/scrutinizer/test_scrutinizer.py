__author__ = 'cocoon'


from core import Scrutinizer, Searcher, UiNode



def test_iter():


    s = Scrutinizer.from_file(filename)


    # get all clickables
    for clickable in s.iter(check='clickable'):
        print "%s: class=%s [%s]" %  (clickable.attrib['resource-id'] ,clickable.attrib['class'],clickable.attrib['index'])


    return


def test_unique():
    """


    :return:
    """

    #s = Scrutinizer.from_file(filename)
    s = Scrutinizer.from_file(keypad)

    # get all clickables
    clickables = s.iter(check=['clickable','long-clickables'])

    uniques = s.uniques(clickables)

    print "unique with resource id"
    for unique in uniques['by_resource'].values():
        print UiNode(unique).short_id()
        #print UiNode(unique).hash()

    print "unique with class,index"
    for unique in uniques['by_class'].values():
        print UiNode(unique).class_id()
        #print UiNode(unique).hash()

    print "others"
    for e in uniques['others']:
        print e

    return


def test_selected():
    """

    :return:
    """
    #s = Scrutinizer.from_file(filename)
    s = Scrutinizer.from_file(keypad)

    # find tab selected
    selected = list(s.iter(check='selected', filter = {'class':'android.app.ActionBar$Tab'}))
    for s in selected:
        print "%s [%s]  %s" % ( s.attrib['class'], s.attrib['index'],  s.attrib['resource-id'] )

    return


def test_searcher():
    """


    :return:
    """
    s = Searcher.from_file(keypad)
    all_tabs = s.find_tabs()
    assert len(all_tabs) == 4

    selected = s.find_tabs(selected= True)
    assert len(selected) == 1

    passive = s.find_tabs(selected= False)
    assert len(passive) == 3


def test_find_first_textview():


    s = Searcher.from_file(more_menu)

    # find a list view
    filter = { 'class' : 'android.widget.ListView' , 'index' :'0' }
    start = list(s.iter(filter= filter))[0]

    t = s.find_first_textview(start)

    assert t.attrib['text'] == 'Speed dial'

    n = s.find_first_textview(t)
    assert n == None



    return


if __name__=='__main__':


    filename = '../../uisnapshots/dump_incallui.uix'
    keypad = '../../uisnapshots/dump_contacts.keypad.uix '

    more_menu = "../../uisnapshots/android_4.2.4/phone/contacts.keypad_more.uix"


    test_iter()
    test_unique()
    test_selected()
    test_searcher()
    test_find_first_textview()
