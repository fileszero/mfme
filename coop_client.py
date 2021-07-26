

class coop_client:
    _browser = None
    _display = None

    def __init__(self, config,browser=None):
        self.email = config["mail"]
        self.password = config["password"]
        self._browser=browser
