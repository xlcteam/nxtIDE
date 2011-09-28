
import sys
sys.path.append('../nxtemu/')


def getAPI():
    """Returns a list of available functions for NXT brick. """
    
    out = {}
    
    api = __import__('api')

    for func in dir(api):
        if func[0].isupper():
            id = getattr(api, func)
            if type(id).__name__ == "function":
                out[func] = id.__doc__

    
    return out

if __name__ == "__main__":
    api = getAPI()
    print api['Random']
