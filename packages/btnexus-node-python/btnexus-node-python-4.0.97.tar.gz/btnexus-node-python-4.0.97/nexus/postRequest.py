"""A post request with a callback for the response"""
# System imports

import json
import threading
import requests

# 3rd Party imports

# local imports

# end file header
__author__      = "Adrian Lubitz"
__copyright__   = "Copyright (c)2017, Blackout Technologies"

class PostRequest(object):
    """
    A post request with a callback for the response
    """
    def __init__(self, url, data, callback=None, errBack=None):
        """
        setting up the request.

        :param url: the url to send the request to
        :type url: String
        :param data: the data which should be send
        :type data: dict
        :param callback: the callback which handles the response. Takes one argument which is a json object
        :type callback: function pointer
        :param errBack: callback to handle errors. takes one argument which is the exception
        :type errBack: function pointer
        """

        self.url = url
        self.data = json.dumps(data)
        self.callback = callback
        self.errBack = errBack

    def _send(self, **kwargs):
        """
        sending the request and trigger the callback when response is ready - this is blocking
        """
        try:
            r = requests.post(self.url, data=self.data, **kwargs)
            r.raise_for_status()
            content =json.loads(r.content)            
            if self.callback:
                self.callback(r.json())
        except Exception as e:
            if self.errBack:
                self.errBack(e)
            else:
                raise(e)

    def send(self, blocking=False, **kwargs):
        """
        sending the request in a thread(if blocking=False) and triggers the callback when response is ready
        """
        if not blocking:    
            threading.Thread(target=self._send, kwargs=kwargs).start()
        else:
            self._send(**kwargs)


if __name__ == "__main__":
    import os
    token = os.environ["TOKEN"]
    axon = os.environ["AXON_HOST"]
    print ("URL: {}".format(axon))
    print ("Token: {}".format(token))