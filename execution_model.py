import datetime as dt

import portolio_constructor
import alpha_model
import risk_model

class ExecutionModel():
    def __init__(self, time_delta, market_model):
        self.time_delta = time_delta
        self.market_model

    def execute(self):
        if self.time_delta == False:
            for i in range(len(self.market_model.data)):
                self.tick()
        elif type(time_delta) == 'int':
            self.tick()
            dt.time.sleep(time_delta)

    def tick():
        pass
