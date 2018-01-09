from .TritonAuth import TritonAuth

if __name__ == "__main__":
    base = TritonAuth()
    base.startLogin()
    base.mainLoop()
