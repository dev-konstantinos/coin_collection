from data import Coin, CoinCollection


class AddCoinUseCase:
    """Класс бизнес-логики для добавления монеты в коллекцию"""
    def __init__(self, coin_collection: CoinCollection):
        self.coin_collection = coin_collection

    def execute(self, coin_id, coin_name, coin_year, coin_country, coin_metal, coin_weight, coin_price):
        """Метод для добавления монеты в коллекцию"""
        coin = Coin(coin_id, coin_name, coin_year, coin_country, coin_metal, coin_weight, coin_price)
        self.coin_collection.add_coin(coin)

class ShowAllCoinsUseCase:
    """Класс бизнес-логики для получения всех монет из коллекции"""
    def __init__(self, coin_collection: CoinCollection):
        self.coin_collection = coin_collection

    def execute(self):
        """Метод для получения всех монет из коллекции"""
        return self.coin_collection.get_all_coins()


class DeleteCoinUseCase:
    """Класс бизнес-логики для удаления монеты из коллекции"""
    def __init__(self, coin_collection: CoinCollection):
        self.coin_collection = coin_collection
    
    def execute(self, coin_id: int):
        """Метод для удаления монеты из коллекции по ее ID"""
        self.coin_collection.del_coin(coin_id)


class FindCoinsByParamsUseCase:
    """Класс бизнес-логики для поиска монет по параметрам"""
    def __init__(self, coin_collection: CoinCollection):
        self.coin_collection = coin_collection

    def execute(self, **params):
        """Метод для поиска монет по различным параметрам"""
        return self.coin_collection.find_coin_by_params(**params)


class UpdateCoinUseCase:
    """Класс бизнес-логики для обновления данных монеты"""
    def __init__(self, coin_collection: CoinCollection):
        self.coin_collection = coin_collection

    def execute(self, coin_id: int, new_coin_data: dict):
        """Метод для обновления данных монеты по ID"""
        self.coin_collection.update_coin(coin_id, new_coin_data)