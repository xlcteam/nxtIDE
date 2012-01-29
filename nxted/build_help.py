#!/usr/bin/env python

import sys, yaml
sys.path.append('../nxtemu/')


def getAPI():
    """Returns a list of available functions for NXT brick. """
    
    out = {}
    
    api = __import__('api')

    for func in dir(api):
        if func[0].isupper():
            id = getattr(api, func)
            if type(id).__name__ == "function":
                out[func] = id.__doc__.replace(':param ', '')

    
    return out

if __name__ == "__main__":
    api = getAPI()

    f = open('help.yml', 'w')
    f.write(yaml.dump(api, default_flow_style=False))
    f.close()
