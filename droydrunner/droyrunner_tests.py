__author__ = 'cocoon'


from droydrunner.uidevice import UiDevice
from droydrunner.uiselector import UiSelector
import time


# white gs5
id1 = '388897e5'



def test_uiselector():


    # create uidevice
    d1 = UiDevice(serial=id1)

    # select phone app
    d1.quick_launch('phone')


    s = UiSelector(d1)







    return





def test():



    return


if __name__=='__main__':


    test_uiselector()

    #test()

