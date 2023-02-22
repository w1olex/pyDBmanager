import mysql.connector
import xml.etree.ElementTree as ET
import csv


class DBFacade:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        """
        1. Parsování konfiguračního souboru XML
        2. Připojení se k databázi
        """
        tree = ET.parse("config/config.xml")
        root = tree.getroot()
        host = root.find("host").text
        user = root.find("user").text
        password = root.find("password").text
        database = root.find("database").text


        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        self.cursor = self.conn.cursor()


    def close(self):
        """
        Uzavření připojení k databázi
        """
        self.cursor.close()
        self.conn.close()


    def insert(self, obj):
        """
        Vložení (Insert) nového záznamu do databáze

        :param obj: instance třídy vybrané tabulky
        :type obj: object
        """
        obj.insert(self.cursor)
        self.conn.commit()


    def update(self, obj, id, attr, value):
        """
        Aktualizace (Update) existujícího záznamu v databázi

        :param obj: instance třídy vybrané tabulky
        :param id: id záznamu který chcete aktualizovat
        :param attr: atribut který chceme aktualizovat
        :param value: nová hodnota
        """
        obj.update(self.cursor, id, attr, value)
        self.conn.commit()


    def delete(self, obj, id):
        """
        Smazání (Delete) záznamu z databáze

        :param obj: instance třídy vybrané tabulky
        :param id: id záznamu který chcete smazat
        :return:
        """
        obj.delete(self.cursor, id)
        self.conn.commit()


    def select(self, table_name):
        """
        Výběr záznamů z tabulky

        :param table_name: název tabulky z které chceme vybrat záznamy
        """

        query = f"SELECT * FROM {table_name}"
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        for object in result:
            print(object)


    def drop_all_objects(self):
            """
            Smazání všech objektů (tabulek, pohledů)

            """
            # Seznam všech tabulek ke smazání
            objects = ['objednavky_produkty', 'objednavka', 'dodavka', 'dodavatel', 'produkt', 'zakaznik', 'podrobnosti_objednavky', 'podrobnosti_dodavky']

            # Procházení seznamu tabulek a odstranění každé z nich
            for obj in objects:
                self.cursor.execute(f"DROP TABLE IF EXISTS {obj}")
                self.cursor.execute(f"DROP VIEW IF EXISTS {obj}")

            # Potvrzení změn
            self.conn.commit()

            print("\nVsechny tabulky a pohledy byly uspesne smazany")


    def transfer_credit(self, from_customer_id, to_customer_id, kredit):
        """
        Převod kreditů z jednoho účtu zákazníka na druhý

        :param from_customer_id: ID uctu zakaznika ze ktereho chcete prevest kredit
        :param to_customer_id: ID uctu na ktery chcete prevest kredit
        :param kredit: hodnota prevadeneho kreditu
        """
        try:
            # Získání kreditu zakaznika
            self.cursor.execute("SELECT kredit FROM zakaznik WHERE id = %s", (from_customer_id,))
            from_customer_credit = self.cursor.fetchone()
            if from_customer_credit is None:
                # Zakaznik se zadanym ID neexistuje
                raise Exception("Transaction failed: customer with id {} does not exist".format(from_customer_id))
                return
            else:
                from_customer_credit = from_customer_credit[0]

            # Získání kreditu příjemce
            self.cursor.execute("SELECT kredit FROM zakaznik WHERE id = %s", (to_customer_id,))
            to_customer_credit = self.cursor.fetchone()
            if to_customer_credit is None:
                # Zakaznik se zadanym ID neexistuje
                raise Exception("Transaction failed: customer with id {} does not exist".format(to_customer_id))
                return

            # Pokud má zákazník dostatečný kredit
            if from_customer_credit >= kredit:
                self.cursor.execute("START TRANSACTION")

                # Odebrání kreditu od zákazníka
                update_points = ("UPDATE zakaznik SET kredit = kredit - %s WHERE id = %s")
                self.cursor.execute(update_points, (kredit, from_customer_id))

                # Připsání kreditu příjemci
                update_points = ("UPDATE zakaznik SET kredit = kredit + %s WHERE id = %s")
                self.cursor.execute(update_points, (kredit, to_customer_id))

                self.conn.commit()
            else:
                # Pokud zákazník nemá dostatečný kredit
                raise Exception("Transaction failed: insufficient credit")

        except:
            # Pokud dojde k chybě, provede se rollback
            self.conn.rollback()
            raise


    def order_details(self):
        """
        Tato funkce slouzi k vypisu detailu objednavek z databaze

        """
        query = "SELECT * FROM podrobnosti_objednavky"

        self.cursor.execute(query)
        result = self.cursor.fetchall()

        # Prochazeni vysledku dotazu a vypis do konzole
        for row in result:
            print(row)

        # Ziskani jmen sloupcu
        columns = [i[0] for i in self.cursor.description]

        try:
            # Ulozeni vysledku do CSV souboru
            with open("reports_export/podrobnosti_objednavky.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(columns)
                writer.writerows(result)
        except:
            print("Ulozeni reportu do csv souboru se nezdarilo")


    def supply_details(self):
        """
        Tato funkce slouzi k vypisu detailu dodavky z databaze

        """
        query = ("SELECT * FROM podrobnosti_dodavky")

        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        # Prochazeni vysledku dotazu a vypis do konzole
        for row in rows:
            print(row)

        # Ziskani jmen sloupcu
        columns = [i[0] for i in self.cursor.description]

        try:
            # Ulozeni vysledku do CSV souboru
            with open("reports_export/podrobnosti_dodavky.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(columns)
                writer.writerows(rows)
        except:
            print("Ulozeni reportu do csv souboru se nezdarilo")