import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, 
                               QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QTableWidget, QTableWidgetItem)
from PySide6.QtCore import Qt
from logic import (AddCoinUseCase, ShowAllCoinsUseCase, DeleteCoinUseCase, FindCoinsByParamsUseCase, UpdateCoinUseCase)
from data import CoinCollection


class MainWindow(QMainWindow):
    def __init__(self, coin_collection):
        super().__init__()

        self.setWindowTitle("Coin Manager")
        self.resize(800, 600)

        # Initializing use-case classes
        self.add_coin_use_case = AddCoinUseCase(coin_collection)
        self.show_all_coins_use_case = ShowAllCoinsUseCase(coin_collection)
        self.delete_coin_use_case = DeleteCoinUseCase(coin_collection)
        self.find_coins_use_case = FindCoinsByParamsUseCase(coin_collection)
        self.update_coin_use_case = UpdateCoinUseCase(coin_collection)

        # List of field names
        self.field_names = ["coin_id", "coin_name", "coin_year", "coin_country", "coin_metal", "coin_weight", "coin_price"]

        # Input fields for the coin
        self.input_fields = {}
        input_layout = QVBoxLayout()
        max_label_width = 70

        for name in self.field_names:
            label = QLabel(name.capitalize())
            label.setAlignment(Qt.AlignRight)
            label.setMinimumWidth(max_label_width)

            line_edit = QLineEdit(self)
            self.input_fields[name] = line_edit

            field_layout = QHBoxLayout()
            field_layout.addWidget(label)
            field_layout.addWidget(line_edit)
            input_layout.addLayout(field_layout)

        # Action buttons
        self.add_button = QPushButton("Add new coin")
        self.add_button.clicked.connect(self.add_coin)

        self.show_button = QPushButton("Show all coins")
        self.show_button.clicked.connect(self.show_all_coins)

        self.find_button = QPushButton("Find coins")
        self.find_button.clicked.connect(self.find_coins)

        self.delete_button = QPushButton("Delete coin by ID")
        self.delete_button.clicked.connect(self.delete_coin)

        self.update_button = QPushButton("Edit coin info")
        self.update_button.clicked.connect(self.update_coin)

        # Table for displaying coins
        self.coin_table = QTableWidget(0, len(self.field_names))
        self.coin_table.setHorizontalHeaderLabels(self.field_names)
        header = self.coin_table.horizontalHeader()

        for col in range(len(self.field_names)):
            if col == 1:
                header.resizeSection(col, 210)
            elif col == 3:
                header.resizeSection(col, 120)
            else:
                header.resizeSection(col, 90)

        self.coin_table.cellClicked.connect(self.on_table_item_clicked)

        # Layout of elements
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.show_button)
        button_layout.addWidget(self.find_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.update_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.coin_table)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def on_table_item_clicked(self, row, column):
        """Table click handler extracts data from the selected row and fills the input fields"""
        for col, field in enumerate(self.field_names):
            item = self.coin_table.item(row, col)
            if item is not None:
                self.input_fields[field].setText(item.text())

    def add_coin(self):
        """Method for adding new coins"""
        try:
            coin_data = self.get_input_data()
            self.add_coin_use_case.execute(**coin_data)
            QMessageBox.information(self, "Success", "New coin added!")
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def show_all_coins(self):
        """Method for displaying all coins in the collection"""
        coins = self.show_all_coins_use_case.execute()
        self.populate_table(coins)

    def find_coins(self):
        """Searching method"""
        search_params = self.get_input_data(optional=True)
        
        # Filtering out empty values from the search parameters
        search_params = {key: value for key, value in search_params.items() if value}

        # Checking data types for numerical fields
        if "coin_year" in search_params:
            try:
                search_params["coin_year"] = int(search_params["coin_year"])
            except ValueError:
                QMessageBox.warning(self, "Error", "Year must be a valid integer.")
                return

        if "coin_weight" in search_params:
            try:
                search_params["coin_weight"] = float(search_params["coin_weight"])
            except ValueError:
                QMessageBox.warning(self, "Error", "Weight must be a valid number.")
                return

        if "coin_price" in search_params:
            try:
                search_params["coin_price"] = float(search_params["coin_price"])
            except ValueError:
                QMessageBox.warning(self, "Error", "Price must be a valid number.")
                return

        # Performing the query using the use case
        coins = self.find_coins_use_case.execute(**search_params)
        if coins is None or len(coins) == 0:
            QMessageBox.information(self, "No results", "No coins found with these parameters.")
        else:
            self.populate_table(coins)

    def delete_coin(self):
        """Method for removing coins from the collection"""
        coin_id = self.input_fields["coin_id"].text()
        if not coin_id.isdigit():
            QMessageBox.warning(self, "Error", "Enter correct ID")
            return
        self.delete_coin_use_case.execute(int(coin_id))
        QMessageBox.information(self, "Success", "Coin deleted!")

    def update_coin(self):
        """Method for editing coin imformation"""
        coin_id = self.input_fields["coin_id"].text()
        if not coin_id.isdigit():
            QMessageBox.warning(self, "Error", "Enter correct ID")
            return

        new_data = self.get_input_data(optional=True)
        self.update_coin_use_case.execute(int(coin_id), new_data)
        QMessageBox.information(self, "Success", "Coin info changed!")

    def get_input_data(self, optional=False):
        """Method for collecting input data from the GUI fields"""
        coin_data = {}
        for field, widget in self.input_fields.items():
            value = widget.text().strip()
            if value or optional:
                coin_data[field] = value

        if not optional:
            if not all(coin_data.values()):
                raise ValueError("All fields must be filled")

            coin_data["coin_year"] = int(coin_data["coin_year"])
            coin_data["coin_weight"] = float(coin_data["coin_weight"])
            coin_data["coin_price"] = float(coin_data["coin_price"])

        return coin_data

    def populate_table(self, coins):
        """Method for drawing a coin information table"""
        self.coin_table.setRowCount(0)
        for coin in coins:
            row_position = self.coin_table.rowCount()
            self.coin_table.insertRow(row_position)

            for col, value in enumerate(vars(coin).values()):
                self.coin_table.setItem(row_position, col, QTableWidgetItem(str(value)))
        
        self.coin_table.verticalHeader().setVisible(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    coin_collection = CoinCollection()
    window = MainWindow(coin_collection)
    window.show()

    sys.exit(app.exec())

