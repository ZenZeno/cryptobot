import market_model as mm
import alpha_model as am
import time

market = mm.KrakenMarketModel()
alpha = am.MovingAverageCrossover('MAC 2/10', 2, 10)

while True:
    market.update('XETHXXBT')
    alpha.generate_signals(market.last('XETHXXBT'))
    print(alpha)
    time.sleep(1)
