__author__ = 'cocoon'
"""

    an interface to phone hub






"""

NativeClient_error = None
HttpClient_error = None

try:
    # see if we can use HttpClient ( requests )
    from droydrunner.phone.hub.client import HttpClient
except ImportError ,e:
    # no module requests
    HttpClient = None
    HttpClient_error = e

try:
    # see if we can use native client ( uiautomator )
    from droydrunner.phone.hub.api import NativeClient
except ImportError ,e :
    # no module requests
    NativeClient = None
    HttpClient_error = e



def PhoneHub(url = None):
    """

        return a NativeClient or an HttpClient (if url not None )

    :param url:
    :return:
    """

    if not url:
        # select the native api to phone hub
        if not NativeClient:
            raise ImportError('cannot load a NativeClient : %s' , str(NativeClient_error))
        # return a native client instance
        return NativeClient()

    else:
        # select a Http client to phone hub
        if not HttpClient:
            raise ImportError('cannot load an HttpClient: %s' % str(HttpClient_error))
        # return an HttpClient instance
        return HttpClient(url)
