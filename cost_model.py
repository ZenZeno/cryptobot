class CostModel():
    def __init(self, percent_fee):
        self.percent_fee = percent_fee

    def cost(self, amount):
        return amount * .01 * self.percent_fee
