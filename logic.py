from data import Coin, CoinCollection

class AddCoinUseCase:
    """Logic class for adding a coin to the collection"""
    def __init__(self, coin_collection: CoinCollection):
        self.coin_collection = coin_collection

    def execute(self, coin_id, coin_name, coin_year, coin_country, coin_metal, coin_weight, coin_price):
        """Method for adding a coin to the collection"""
        coin = Coin(coin_id, coin_name, coin_year, coin_country, coin_metal, coin_weight, coin_price)
        self.coin_collection.add_coin(coin)

class ShowAllCoinsUseCase:
    """Logic class for getting all coins from the collection"""
    def __init__(self, coin_collection: CoinCollection):
        self.coin_collection = coin_collection

    def execute(self):
        """Method for getting all coins from the collection"""
        return self.coin_collection.get_all_coins()


class DeleteCoinUseCase:
    """Logic class for deleting a coin from the collection"""
    def __init__(self, coin_collection: CoinCollection):
        self.coin_collection = coin_collection
    
    def execute(self, coin_id: int):
        """Method for deleting a coin from the collection by ID"""
        self.coin_collection.del_coin(coin_id)


class FindCoinsByParamsUseCase:
    """Logic class for searching coins by parameters"""
    def __init__(self, coin_collection: CoinCollection):
        self.coin_collection = coin_collection

    def execute(self, **params):
        """Method for searching coins by various parameters"""
        return self.coin_collection.find_coin_by_params(**params)


class UpdateCoinUseCase:
    """Logic class for updating a coin data"""
    def __init__(self, coin_collection: CoinCollection):
        self.coin_collection = coin_collection

    def execute(self, coin_id: int, new_coin_data: dict):
        """Method for updating a coin's data by ID"""
        self.coin_collection.update_coin(coin_id, new_coin_data)