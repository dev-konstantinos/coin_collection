import sqlite3
import os

class Coin:
    """Класс монеты для хранения информации о монете"""
    def __init__(self, coin_id, coin_name, coin_year, coin_country, coin_metal, coin_weight, coin_price):
        self.coin_id = coin_id
        self.coin_name = coin_name
        self.coin_year = coin_year
        self.coin_country = coin_country
        self.coin_metal = coin_metal
        self.coin_weight = coin_weight
        self.coin_price = coin_price

    def __repr__(self):
        """Метод для представления монеты в виде строки"""
        return f"Coin(id={self.coin_id}, {self.coin_name}, {self.coin_year}, {self.coin_country}, {self.coin_metal}, {self.coin_weight}g, ${self.coin_price})"


class CoinCollection:
    """Класс коллекции монет для хранения и управления монетами в базе данных"""
    def __init__(self, db_file='coins.db'):
        # Получаем путь к каталогу, где находится текущий скрипт
        script_dir = os.path.dirname(os.path.realpath(__file__))
        # Составляем полный путь к базе данных, используя текущую директорию
        self.db_file = os.path.join(script_dir, db_file)
        self.create_table()

    def create_table(self):
        """Метод для создания таблицы в базе данных, если она не существует"""
        if not os.path.exists(self.db_file):
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS coins (
                            coin_id INTEGER PRIMARY KEY, 
                            coin_name TEXT, 
                            coin_year INTEGER, 
                            coin_country TEXT, 
                            coin_metal TEXT, 
                            coin_weight REAL, 
                            coin_price REAL)''')
            conn.commit()
            conn.close()

    def add_coin(self, coin):
        """Метод добавления монеты в коллекцию в базе данных"""
        
        # Проверяем уникальность coin_id
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('SELECT coin_id FROM coins WHERE coin_id = ?', (coin.coin_id,))
        existing_coin = c.fetchone()

        if existing_coin:
            raise ValueError(f"Coin ID {coin.coin_id} already exists in the database.")

        # Если coin_id уникален, добавляем монету в базу данных
        c.execute('''INSERT INTO coins (coin_id, coin_name, coin_year, coin_country, coin_metal, coin_weight, coin_price) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                (coin.coin_id, coin.coin_name, coin.coin_year, coin.coin_country, coin.coin_metal, coin.coin_weight, coin.coin_price))
        conn.commit()
        conn.close()

    def get_all_coins(self):
        """Метод получения всех монет из коллекции из базы данных"""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('SELECT * FROM coins')
        coins = c.fetchall()
        conn.close()
        return [Coin(*coin) for coin in coins]

    def del_coin(self, coin_id):
        """Метод удаления монеты из коллекции по ID из базы данных"""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('DELETE FROM coins WHERE coin_id = ?', (coin_id,))
        conn.commit()
        conn.close()

    def find_coin_by_params(self, **params):
        """Метод для поиска монет по различным параметрам из базы данных"""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Формирование запроса
        query = 'SELECT * FROM coins WHERE '
        query_conditions = []
        query_values = []

        # Проверяем, что есть хотя бы один параметр для поиска
        if not params:
            return []  # Если параметры пустые, возвращаем пустой список

        # Добавляем условия для каждого параметра
        for key, value in params.items():
            if value:  # Пропускаем пустые значения
                query_conditions.append(f'{key} = ?')
                query_values.append(value)

        if not query_conditions:
            return []  # Если нет условий, возвращаем пустой список

        # Строим полный запрос
        query += ' AND '.join(query_conditions)
        
        try:
            c.execute(query, tuple(query_values))
            coins = c.fetchall()
        except sqlite3.OperationalError as e:
            print(f"SQL Error: {e}")
            coins = []

        conn.close()
        return [Coin(*coin) for coin in coins] if coins else None


    def update_coin(self, coin_id, new_coin_data):
        """Метод для обновления данных монеты по ID в базе данных"""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        # Строим динамическое обновление на основе новых данных
        update_columns = []
        update_values = []
        
        for key, value in new_coin_data.items():
            update_columns.append(f"{key} = ?")
            update_values.append(value)
        
        update_values.append(coin_id)
        update_query = f"UPDATE coins SET {', '.join(update_columns)} WHERE coin_id = ?"
        c.execute(update_query, tuple(update_values))
        conn.commit()
        conn.close()