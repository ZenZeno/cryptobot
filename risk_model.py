import poloniex

class RiskModel():
    pass

class Limiter(RiskModel):
    def __init__(self, limit):
        self.limit = limit * .01
    
    def limit(self):
        return self.limit
