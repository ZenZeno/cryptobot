class CostModel():
    def __init__(self, percent_fee):
        self.percent_fee = percent_fee

    def cost(self, amount):
        return amount * 0.01 * self.percent_fee
