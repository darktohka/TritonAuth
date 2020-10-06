def startProgram():
    from .TritonAuth import TritonAuth

    base = TritonAuth()
    base.startLogin()
    base.mainLoop()
