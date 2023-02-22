class Objednavka:
    def __init__(self, zakaznik_id, produkt_id, mnozstvi, stav):
        """
        Konstruktor třídy Objednavka, který inicializuje atributy zakaznik_id, produkt_id, mnozstvi a stav.

        :param zakaznik_id: ID zákazníka
        :param produkt_id: ID produktu
        :param mnozstvi: množství objednaného produktu
        :param stav: stav objednávky
        :type: stav: enum
        """

        self.zakaznik_id = zakaznik_id
        self.produkt_id = produkt_id
        self.mnozstvi = mnozstvi
        self.stav = stav

    def insert(self, cursor):
        """
        Vložení objednávky do databáze

        :param cursor: Kurzor databáze
        """

        # Zkontroluje, jestli existuje zákazník s daným ID
        check_customer = "SELECT * FROM zakaznik WHERE id = %s"
        cursor.execute(check_customer, (self.zakaznik_id,))
        customer = cursor.fetchone()
        if not customer:
            raise Exception("Error: Zakaznik s id {} neexistuje".format(self.zakaznik_id))

        # Zkontroluje, jestli existuje produkt s daným ID
        check_product = "SELECT * FROM produkt WHERE id = %s"
        cursor.execute(check_product, (self.produkt_id,))
        product = cursor.fetchone()
        if not product:
            raise Exception("Error: Produkt s id {} neexistuje".format(self.produkt_id))

        # Vložení objednávky do tabulky, pokud existuje zákazník i produkt
        query = "INSERT INTO objednavka (datum_objednavky, zakaznik_id, produkt_id, mnozstvi, stav) VALUES (NOW(), %s, %s, %s, %s)"
        cursor.execute(query, (self.zakaznik_id, self.produkt_id, self.mnozstvi, self.stav))

        order_id = cursor.lastrowid
        # Vložení položek objednávky do vazebni tabulky objednavky_produkty
        add_order_item = ("INSERT INTO objednavky_produkty (objednavka_id, produkt_id) "
                          "VALUES (%s, %s)")
        cursor.execute(add_order_item, (order_id, self.produkt_id))


    def select(self, cursor):
        """
        Výběr všech objednavek z databáze

        :param cursor: kurzor databáze
        """

        query = "SELECT * FROM objednavka"
        cursor.execute(query)
        result = cursor.fetchall()
        return result


    def update(self, cursor, id, attr, value):
        """
        Tato funkce aktualizuje data objednavky s daným ID v databázi.

        :param cursor: kurzor databáze
        :param id: ID produktu
        :param attr: název atributu, který se má aktualizovat
        :param value: nová hodnota atributu
        """

        # Zkontrolování, zda existuje objednavka s daným ID
        check_order_exists = "SELECT id FROM objednavka WHERE id = %s"
        cursor.execute(check_order_exists, (id,))
        order_exists = cursor.fetchone()

        if not order_exists:
            raise ValueError(f"Objednavka s ID {id} neexistuje.")

        # Zkontrolování, zda objednavka má daný atribut
        query = f"SHOW COLUMNS FROM objednavka LIKE %s"
        cursor.execute(query, (attr,))
        attr_exists = cursor.fetchone() is not None

        if not attr_exists:
            raise ValueError(f"Objednavka nema atribut '{attr}'.")

        if(attr == 'zakaznik_id'):
            # Zkontrolování existence zakaznika s daným ID
            query = f"SELECT * FROM zakaznik WHERE id = %s"
            cursor.execute(query, (value,))
            zakaznik_exists = cursor.fetchone() is not None

            if not zakaznik_exists:
                raise ValueError(f"Zakaznik s ID {value} neexistuje.")

        if(attr == 'produkt_id'):
            # Zkontrolování existence produktu s daným ID
            query = f"SELECT * FROM produkt WHERE id = %s"
            cursor.execute(query, (value,))
            produkt_exists = cursor.fetchone() is not None

            if not produkt_exists:
                raise ValueError(f"Produkt s ID {value} neexistuje.")


        # Aktualizace (update) objednavky
        query = f"UPDATE objednavka SET {attr} = %s WHERE id = %s"
        cursor.execute(query, (value, id))

        if (attr == "produkt_id"):
            query = f"UPDATE objednavky_produkty SET {attr} = %s WHERE objednavka_id = %s"
            cursor.execute(query, (value, id))


    def delete(self, cursor, id):
        """

        :param cursor: kurzor databáze
        :param id: ID objednavky ktera se ma smazat
        """

        # Zkontrolování existence objednavky s daným ID
        check_order_exists = "SELECT id FROM objednavka WHERE id = %s"
        cursor.execute(check_order_exists, (id,))
        order_exists = cursor.fetchone()

        if not order_exists:
            raise ValueError(f"Objednavka s ID {id} neexistuje.")

        # Smazání instance objednávky z tabulky objednavky_produkty
        delete_order_item = ("DELETE FROM objednavky_produkty WHERE objednavka_id = %s")
        cursor.execute(delete_order_item, (id,))

        # Smazani objednavky
        delete_order = ("DELETE FROM objednavka WHERE id = %s")
        cursor.execute(delete_order, (id,))
