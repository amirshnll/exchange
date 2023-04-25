class ExternalExchangeHandler:
    def buy_from_exchange(self, coin_name, count):
        print("exchange called:", coin_name, count, "$")
        return True
