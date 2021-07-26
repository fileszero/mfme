

class coop_client:
    def __init__(self, config):
        super().__init__(config)

    def __del__(self):
        super().__del__()

login = "https://ouchi.ef.cws.coop/auth/bb/login.do?relayed=1"