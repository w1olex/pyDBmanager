import csv
from tables.zakaznik import Zakaznik
from tables.produkt import Produkt
from tables.dodavatel import Dodavatel

class CSVImport:
    def __init__(self):
        self.zakaznik_list = []
        self.produkt_list = []
        self.dodavatel_list = []

    def import_zakaznik(self, file_name):
        """
        Tato funkce importuje data o zákaznících z csv souboru do instancí
        třídy Zakaznik a ukládá je do seznamu zakaznik_list.

        :param file_name: jméno souboru, kde jsou uložena data o zákaznících
        """
        with open(file_name, 'r') as file:
            # Načtení souboru pomocí csv.reader
            reader = csv.reader(file)
            header = next(reader)
            # Procházení řádků v souboru
            for row in reader:
                # Vytvoření instance třídy Zakaznik s použitím dat z aktuálního řádku
                zakaznik = Zakaznik(row[0], row[1], row[2])
                # Přidání instance do seznamu
                self.zakaznik_list.append(zakaznik)


    def import_produkt(self, file_name):
        """
        Tato funkce importuje data o produktech z csv souboru
        do instancí třídy Produkt a ukládá je do seznamu produkt_list.

        :param file_name: jméno souboru, kde jsou uložena data o produktech
        """

        with open(file_name, 'r') as file:
            # Načtení souboru pomocí csv.reader
            reader = csv.reader(file)
            header = next(reader)
            # Procházení řádků v souboru
            for row in reader:
                # Vytvoření instance třídy Produkt s použitím dat z aktuálního řádku
                produkt = Produkt(row[0], row[1], row[2])
                # Přidání instance do seznamu
                self.produkt_list.append(produkt)


    def import_dodavatel(self, file_name):
        """
        Tato funkce importuje data o dodavateli z csv souboru do instancí
        třídy Dodavatel a ukládá je do seznamu dodavatel_list.

        :param file_name: jméno souboru, kde jsou uložena data o dodavateli
        """


        with open(file_name, 'r') as file:
            # Načtení souboru pomocí csv.reader
            reader = csv.reader(file)
            header = next(reader)
            # Procházení řádků v souboru
            for row in reader:
                # Vytvoření instance třídy Dodavatel s použitím dat z aktuálního řádku
                dodavatel = Dodavatel(row[0], row[1], row[2])
                # Přidání instance do seznamu
                self.dodavatel_list.append(dodavatel)


    def insert_to_database_zakaznik(self, db):
        """
        Tato funkce vkládá data o zákaznících z instancí třídy Zakaznik do databáze.

        :param db: instance třídy, která implementuje funkci pro vkládání do databáze
        """

        for zakaznik in self.zakaznik_list:
            db.insert(zakaznik)

    def insert_to_database_produkt(self, db):
        """
        Tato funkce vkládá data o produktech z instancí třídy Produkt do databáze.

        :param db: instance třídy, která implementuje funkci pro vkládání do databáze
        """

        for produkt in self.produkt_list:
            db.insert(produkt)

    def insert_to_database_dodavatel(self, db):
        """
        Tato funkce vkládá data o dodavateli z instancí třídy Dodavatel do databáze.

        :param db: instance třídy, která implementuje funkci pro vkládání do databáze
        """
        for dodavatel in self.dodavatel_list:
            db.insert(dodavatel)