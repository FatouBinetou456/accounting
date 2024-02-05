import sys

from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem,QFormLayout, QDateEdit, QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,QDialog,QLabel, QLineEdit, QComboBox, QLabel, QPushButton, QHBoxLayout, QLabel, QLineEdit, QPushButton, QApplication
from PyQt5.QtCore import QDate, QAbstractTableModel
import numpy as np
from PyQt5.QtWidgets import QTableView

from PyQt5.QtCore import Qt
import sqlite3

from PyQt5.QtWidgets import QHeaderView


class Category:
    def __init__(self, nom):
        self.nom = nom

class Produit(Category):
    def __init__(self, nom, nomprod, poid, prixAchat, prixVente):
        super().__init__(nom)
        self.nomprod = nomprod
        self.poid = poid
        self.prixAchat = prixAchat
        self.prixVente = prixVente

class Depenseinfo:
    def __init__(self, nomdep, montant,date):
        self.nomdep = nomdep
        self.montant= montant 
        self.date=date
        
class Transactiondonn:
    def __init__(self, date, montantver, articles,poids):
        self.date = date
        self.montantver = montantver
        self.poids=poids
        self.articles=articles

Categories = [Category("Poisson"),Category("Mouton"),Category("Volaille"),Category("Boeuf"),Category("Crevette"),Category("Poulet")]

import pandas as pd

column_names = ['Categorie','nom', "Prix d'achat unitaire", 'Poids','Prix de vente']
inventaire = pd.DataFrame({col: [] for col in column_names})



columns = ['Nom', 'Montant', 'Date']
vente= pd.DataFrame({col: [] for col in columns})

cols= ['Nom','Montant', 'Date']
bilan= pd.DataFrame({col: [] for col in columns})


conn = sqlite3.connect('comptabilite.db')

# Create a table to hold the data
cur = conn.cursor()

inventaire.to_sql('inventaire', conn, if_exists='append', index=False)
bilan.to_sql('bilan', conn, if_exists='append', index=False)
vente.to_sql('vente', conn, if_exists='append', index=False)

class Transaction(QDialog):
    def __init__(self):
        super().__init__()

        # Set window title and layout
        self.setWindowTitle("Nouvelle Transaction")
        layout = QVBoxLayout()

       

        # Add a combo box for selecting the category
        label_category = QLabel("Categorie:")
        self.combo_category = QComboBox()
        for category in Categories:
            self.combo_category.addItem(category.nom)
        layout.addWidget(label_category)
        layout.addWidget(self.combo_category)

        # Add a line edit for entering the product name
        label_product = QLabel("Nom du produit:")
        self.input_product = QLineEdit()
        layout.addWidget(label_product)
        layout.addWidget(self.input_product)

        # Add a line edit for entering the weight
        label_weight = QLabel("Poids:")
        self.input_weight = QLineEdit()
        layout.addWidget(label_weight)
        layout.addWidget(self.input_weight)
        
        label_quant = QLabel("Quantite:")
        self.input_quant = QLineEdit()
        layout.addWidget(label_quant)
        layout.addWidget(self.input_quant)
        

        # Add a line edit for entering the amount owed
        label_amount = QLabel("Montant:")
        self.input_amount = QLineEdit()
        layout.addWidget(label_amount)
        layout.addWidget(self.input_amount)

        # Add the date input field to the form layout
        label_date = QLabel("Date:")
        self.input_date = QDateEdit()
        self.input_date.setDisplayFormat("dd/MM/yyyy")
        self.input_date.setDate(QDate.currentDate())
        layout.addWidget(label_date)
        layout.addWidget(self.input_date)

        # Add button to submit transaction
        submit_button = QPushButton("Enregistrer")
        submit_button.clicked.connect(self.submit_transaction)
        layout.addWidget(submit_button)

        self.resize(600, 450)
        self.setLayout(layout)

    def submit_transaction(self):
        category = self.combo_category.currentText()
        product_name = self.input_product.text()
        weight_str = self.input_weight.text()
        quant_str = self.input_quant.text()
        amount = float(self.input_amount.text())
        date_edit = self.input_date.date()
        date = date_edit.toPyDate()
        new_row = {'nom':product_name, 'Montant':amount, 'Date':date}
        vente.loc[0] = new_row
        nom=inventaire['nom']
        
        if weight_str:
            weight=float(weight_str)
            weight = round(weight,3)
        else:
            weight=None
            
        if quant_str:
            quant=float(quant_str)
        else:
            quant=None
        
        

# Format the datetime object as a string
        if weight is not None:
            with sqlite3.connect('comptabilite.db' , timeout=10) as conn:
                cur=conn.cursor()
                cur.execute("UPDATE inventaire SET poids = poids - ?, date = ? WHERE nom = ?", (weight,date.strftime('%Y-%m-%d'), product_name))
                cur.execute("INSERT INTO vente (nom,prix,poids,date) VALUES (?,?,?)",(product_name,amount,weight,date.strftime('%Y-%m-%d')))
                conn.commit()
        elif quant is not None:
            with sqlite3.connect('comptabilite.db' , timeout=10) as conn:
                cur=conn.cursor() 
                cur.execute("UPDATE inventaire SET quantite = quantite - ? , date = ? WHERE nom = ?", (quant,date.strftime('%Y-%m-%d'), product_name))
                cur.execute("INSERT INTO vente (nom,prix,quantite,date) VALUES (?,?,?,?)",(product_name,amount,quant,date.strftime('%Y-%m-%d')))
        conn.commit()
        
        
    
        self.accept()
        

class NvProd(QDialog):
    def __init__(self):
        super().__init__()

        # Set window title and layout
        self.setWindowTitle("Nouveau Produit")
        layout = QVBoxLayout()

       

        # Add a combo box for selecting the category
        label_category = QLabel("Categorie:")
        self.combo_category = QComboBox()
        for category in Categories:
            self.combo_category.addItem(category.nom)
        layout.addWidget(label_category)
        layout.addWidget(self.combo_category)

        # Add a line edit for entering the product name
        label_product = QLabel("Nom du produit:")
        self.input_product = QLineEdit()
        layout.addWidget(label_product)
        layout.addWidget(self.input_product)

        # Add a line edit for entering the weight
        label_weight = QLabel("Poids:")
        self.input_weight = QLineEdit()
        layout.addWidget(label_weight)
        layout.addWidget(self.input_weight)
        
        
        label_quant = QLabel("Quantite:")
        self.input_quant = QLineEdit()
        layout.addWidget(label_quant)
        layout.addWidget(self.input_quant)

        # Add a line edit for entering the amount owed
        label_ach = QLabel("Prix d'achat total:")
        self.input_ach = QLineEdit()
        layout.addWidget(label_ach)
        layout.addWidget(self.input_ach)
        
        label_achun = QLabel("Prix d'achat unitaire:")
        self.input_achun = QLineEdit()
        layout.addWidget(label_achun)
        layout.addWidget(self.input_achun)
        
        label_ven = QLabel("Prix de vente :")
        self.input_ven = QLineEdit()
        layout.addWidget(label_ven)
        layout.addWidget(self.input_ven)

        # Add the date input field to the form layout
        label_date = QLabel("Date:")
        self.input_date = QDateEdit()
        self.input_date.setDisplayFormat("dd/MM/yyyy")
        self.input_date.setDate(QDate.currentDate())
        layout.addWidget(label_date)
        layout.addWidget(self.input_date)

        # Add button to submit transaction
        submit_button = QPushButton("Enregistrer")
        submit_button.clicked.connect(self.update_inv)
        layout.addWidget(submit_button)

        self.resize(600, 350)
        self.setLayout(layout)
        
        

    def update_inv(self):
    
        
        category = self.combo_category.currentText()
        product_name = self.input_product.text()
        weight_str = self.input_weight.text()
        quant_str = self.input_quant.text()
        ven=float(self.input_ven.text())
        ach = float(self.input_ach.text())
        achun=float(self.input_achun.text())
        date_edit= self.input_date
        date = date_edit.date().toPyDate()
        noms=np.array(inventaire['nom'])
        
        if weight_str:
            weight=float(weight_str)
            weight= round(weight,3)
        else:
            weight=None
            
        if quant_str:
            quant=float(quant_str)
        else:
            quant=None
        
        
        
        with sqlite3.connect('comptabilite.db' , timeout=10) as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM inventaire WHERE poids=? AND quantite=?",(0,0))

     
            cur.execute("SELECT * FROM inventaire WHERE nom=?", (product_name,))
            existing_product = cur.fetchone()

            if existing_product:
         # If the product already exists, update the weight and quantity
                 cur.execute("UPDATE inventaire SET poids=poids + ?, quantite= quantite + ?, date=? WHERE nom=?",
                     (weight or existing_product[3], quant or existing_product[4], date.strftime('%Y-%m-%d'), product_name))
                 
            else:
                if weight is not None:
                    cur.execute("INSERT INTO inventaire (category, nom, poids, prixach , prixun, prixvente, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (category, product_name, weight, ach, achun , ven, date.strftime('%Y-%m-%d')))
                    cur.execute("INSERT INTO bilan (nom, montant, poids, date) VALUES (?, ?, ?, ?) ", (product_name,ach,weight, date.strftime('%Y-%m-%d')))
                if quant is  not None:
                    
                    cur.execute("INSERT INTO bilan (nom, montant, quantite, date) VALUES (?, ?, ?, ?) ", (product_name,ach,quant, date.strftime('%Y-%m-%d')))
         # If the product doesn't exist, add a new row to the inventory table
                    cur.execute("INSERT INTO inventaire (category, nom, quantite, prixach , prixun, prixvente, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                     (category, product_name, quant, ach, achun , ven, date.strftime('%Y-%m-%d')))

     # Commit the changes to the database
            conn.commit()
               
# Commit the changes to the database
      
        self.accept()
    
       



class Depense(QDialog):
    def __init__(self):
        super().__init__()

        # Set window title and layout
        self.setWindowTitle("Nouvelle Depense")
        layout = QVBoxLayout()

        # Add labels and input fields for transaction information
        label_name = QLabel("Nom:")
        self.input_name = QLineEdit()
        label_amount = QLabel("Montant:")
        self.input_amount = QLineEdit()
        
        # Add the date input field to the form layout
        # Add the date input field to the form layout
        label_date = QLabel("Date:")
        self.input_date = QDateEdit()
        self.input_date.setDisplayFormat("dd/MM/yyyy")
        self.input_date.setDate(QDate.currentDate())
        layout.addWidget(label_date)
        layout.addWidget(self.input_date)
        





        layout.addWidget(label_name)
        layout.addWidget(self.input_name)
        layout.addWidget(label_amount)
        layout.addWidget(self.input_amount)
             # Add button to submit transaction
        submit_button = QPushButton("Enregistrer")
        submit_button.clicked.connect(self.submit_transaction)
        layout.addWidget(submit_button)
        self.resize(600, 250)
        self.setLayout(layout)

    def submit_transaction(self):
        nom = self.input_name.text()
        montant = float(self.input_amount.text())
        date=self.input_date.date().toPyDate()
        
        new_row = {'Nom':nom, 'Montant':montant, 'Date':date}
        bilan.loc[0] = new_row
        with sqlite3.connect('comptabilite.db' , timeout=10) as conn:
            cur =conn.cursor() 
            cur.execute("INSERT INTO depense (nom,montant,date) VALUES (?,?,?)",(nom,montant,date.strftime('%Y-%m-%d')))
        
        self.accept()



               
                
                


class MainWindow(QMainWindow): 
    def __init__(self):
        super().__init__()
        
        # Set window title and dimensions
        self.setWindowTitle("Accounting App")
        self.setGeometry(100, 100, 600, 600)
        central_widget = QWidget()
        

        # Create a widget for the main window
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Create a horizontal layout for the main window
        main_layout = QHBoxLayout(main_widget)

        # Create a vertical layout for the buttons
        button_layout = QVBoxLayout()

        # Create inventory button
        inv_button = QPushButton("Inventaire", self)
        inv_button.setStyleSheet("background-color: #cbe5f6; font-size: 20px")
        inv_button.setFixedHeight(75)
        inv_button.clicked.connect(self.show_dataframe)
        button_layout.addWidget(inv_button)

        # Create transaction history button
        hist_button = QPushButton("Nouvelle transaction", self)
        hist_button.setStyleSheet("background-color: #97caed; font-size: 20px")
        hist_button.setFixedHeight(75)
        hist_button.clicked.connect(self.show_new_transaction)
        button_layout.addWidget(hist_button)

        # Add button to open new transaction form
        trans_button = QPushButton("Depense", self)
        trans_button.setStyleSheet("background-color: #63b0e3; font-size: 20px")
        trans_button.setFixedHeight(75)
        trans_button.clicked.connect(self.show_new_transaction_form)
        button_layout.addWidget(trans_button)

        # Create client balance button
        bal_button = QPushButton("Bilan", self)
        bal_button.setStyleSheet("background-color: #3498db; font-size: 20px")
        bal_button.setFixedHeight(75)
        bal_button.clicked.connect(self.show_bilan)
        button_layout.addWidget(bal_button)
        
        
        prod_button = QPushButton("Nouveaux Produits", self)
        prod_button.setStyleSheet("background-color: #6495ED; font-size: 20px")
        prod_button.setFixedHeight(75)
        prod_button.clicked.connect(self.show_new_product)
        button_layout.addWidget(prod_button)

        central_widget.setLayout(button_layout)
        self.setCentralWidget(central_widget)

        # Add the button layout to the main layout
        main_layout.addLayout(button_layout)

        # Add other elements to the main layout here

    def show_new_transaction_form(self):
        # Show the new transaction form when the button is clicked
        form = Depense()
        form.exec_()
    def show_new_transaction(self):
        # Show the new transaction form when the button is clicked
        form = Transaction()
        form.exec_()
    def show_new_product(self):
        # Show the new transaction form when the button is clicked
        form = NvProd()
        form.exec_()
    def show_dataframe(self):
        # Create a sample dataframe
        
        
        # Create a QTableView widget to show the dataframe
        table = QTableView()
        
        # Set the model for the table to the dataframe
        model = pandasModel(inventaire)
        table.setModel(model)
        
        header = table.horizontalHeader()
        header.setStretchLastSection(True)
        
        # Show the table in a new window
        sub_window = QMainWindow(self)
        sub_window.setCentralWidget(table)
        
        sub_window.setGeometry(100, 100, 1300,1000)
        sub_window.show()
    def show_bilan(self):
        form=ComboBoxDialog(conn)
        form.exec_()

class pandasModel(QAbstractTableModel):
    def __init__(self, inventaire):
        QAbstractTableModel.__init__(self)
        with sqlite3.connect('comptabilite.db') as conn:
            cur= conn.cursor() 
            df = pd.read_sql('SELECT * FROM inventaire', conn)
        self._inventaire= df.sort_values("category")

    def rowCount(self, parent=None):
        return len(self._inventaire.values)

    def columnCount(self, parent=None):
        
        return self._inventaire.columns.size

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._inventaire.values[index.row()][index.column()])
        return None
    
    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return str(self._inventaire.columns[section])
        return None
  


class ComboBoxDialog(QDialog):
    def __init__(self, conn, parent=None):
        super().__init__(parent)
        
        self.conn = conn
        self.setWindowTitle("Choix de periode")
        self.setGeometry(100, 100, 300, 200)
        
        self.table1 = QTableWidget(self)
        self.table1.move(50, 100)
        self.table2 = QTableWidget(self)
        self.table2.move(350, 100)

        # Create combo boxes
        self.frequency_combo = QComboBox(self)
        self.frequency_combo.addItem("Mensuel")
        self.frequency_combo.addItem("Annuel")
        self.frequency_combo.currentIndexChanged.connect(self.populate_date_combo)

        self.date_combo = QComboBox(self)

        # Create label
        self.label = QLabel(self)
        self.label.setText("Veuillez choisir")

        # Create layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.frequency_combo)
        layout.addWidget(self.date_combo)
       

        submit_button = QPushButton("Enregistrer")
        submit_button.clicked.connect(self.see_bil)
        layout.addWidget(submit_button)

    def populate_date_combo(self, index):
        self.date_combo.clear()
        
        
        
        if index == 0: # Monthly
        # Retrieve the distinct dates from the database
            with sqlite3.connect('comptabilite.db' , timeout=10) as conn:
                cur=conn.cursor() 
                cur.execute("SELECT DISTINCT strftime('%Y-%m', date)[:-3] FROM bilan WHERE strftime('%Y-%m', date) >= '2000-01'")
            dates = [row[0] for row in cur.fetchall()]
                # Add the dates to the combobox
            for date in dates:
                self.date_combo.addItem(str(date))
            
        # Add more months here
        elif index == 1: # Yearly
            with sqlite3.connect('comptabilite.db' , timeout=10) as conn:
                cur=conn.cursor() 
                cur.execute("SELECT DISTINCT strftime('%Y', date)[:-6] FROM bilan WHERE strftime('%Y', date) >= '2000'")
            ans = [row[0] for row in cur.fetchall()]

        # Add the dates to the combobox
            for an in ans:
                self.date_combo.addItem(str(an))
    
    def see_bil(self):
        choix = self.date_combo.currentText()
        if len(choix) == 4:
            with sqlite3.connect('comptabilite.db', timeout=10) as conn:
                cur = conn.cursor()
                df1 = pd.read_sql("SELECT * FROM bilan WHERE strftime('%Y', date) = '{}'".format(choix), conn)
                df2 = pd.read_sql("SELECT * FROM depense WHERE strftime('%Y', date) = '{}'".format(choix), conn)
                df3 = pd.read_sql("SELECT * FROM vente WHERE strftime('%Y', date) = '{}'".format(choix), conn)

        else:
            with sqlite3.connect('comptabilite.db', timeout=10) as conn:
                cur = conn.cursor()
                df1 = pd.read_sql("SELECT * FROM bilan WHERE strftime('%Y-%m', date) = '{}'".format(choix), conn)
                df2 = pd.read_sql("SELECT * FROM depense WHERE strftime('%Y-%m', date) = '{}'".format(choix), conn)
                df3 = pd.read_sql("SELECT * FROM vente WHERE strftime('%Y-%m', date) = '{}'".format(choix), conn)

        result_dialog = ResultDialog(df1, df2,df3, self)
        result_dialog.exec_()
           
class ResultDialog(QDialog):
        def __init__(self, df1, df2,df3, parent=None):
            super().__init__(parent)

        # Create tables
            self.table1 = QTableWidget(self)
            self.table1.setRowCount(len(df1.index) + 1)  # add one row for the sum
            self.table1.setColumnCount(len(df1.columns))
            self.table1.setHorizontalHeaderLabels(df1.columns)  # set column names
            self.table1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            for i in range(len(df1.index)):
                for j in range(len(df1.columns)):
                    self.table1.setItem(i, j, QTableWidgetItem(str(df1.iloc[i, j])))
            self.table1.setItem(len(df1.index), 0, QTableWidgetItem('Somme des achats Stock:'))  # add label for sum
            self.table1.setItem(len(df1.index), 1, QTableWidgetItem(str(df1['montant'].sum()))) 
            self.table1.resizeColumnsToContents() # add sum value

            self.table2 = QTableWidget(self)
            self.table2.setRowCount(len(df2.index) + 1)  # add one row for the sum
            self.table2.setColumnCount(len(df2.columns))
            self.table2.setHorizontalHeaderLabels(df2.columns)  # set column names
            self.table2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            for i in range(len(df2.index)):
                for j in range(len(df2.columns)):
                    self.table2.setItem(i, j, QTableWidgetItem(str(df2.iloc[i, j])))
            self.table2.setItem(len(df2.index), 0, QTableWidgetItem('Somme des depenses:'))  # add label for sum
            self.table2.setItem(len(df2.index), 1, QTableWidgetItem(str(df2['montant'].sum())))
            self.table2.resizeColumnsToContents() # add sum value
            
            
            self.table3 = QTableWidget(self)
            self.table3.setRowCount(len(df3.index) + 1)  # add one row for the sum
            self.table3.setColumnCount(len(df3.columns))
            self.table3.setHorizontalHeaderLabels(df3.columns)  # set column names
            self.table3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            for i in range(len(df3.index)):
                for j in range(len(df3.columns)):
                    self.table3.setItem(i, j, QTableWidgetItem(str(df3.iloc[i, j])))
            self.table3.setItem(len(df3.index), 0, QTableWidgetItem('Somme des recettes:'))  # add label for sum
            self.table3.setItem(len(df3.index), 1, QTableWidgetItem(str(df3['prix'].sum())))  # add sum value
            self.table3.resizeColumnsToContents() 
        # Create layout
            layout = QVBoxLayout(self)
            layout.addWidget(self.table1)
            layout.addWidget(self.table2)
            layout.addWidget(self.table3)

            self.setWindowTitle("Resultat")
            self.setGeometry(100, 100, 1000,900)

    

    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    conn.close()
    
    window.show()
    sys.exit(app.exec_())

