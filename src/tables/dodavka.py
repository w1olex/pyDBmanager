class Dodavka:
    def __init__(self, datum_dodani, produkt_id, dodavatel_id, mnozstvi):
        """
        Konstruktor třídy Dodavka, který inicializuje atributy datum_dodani, produkt_id, dodavatel_id a mnozstvi.

        :param datum_dodani: Datum dodání dodávky
        :param produkt_id: ID produktu, který se dodává
        :param dodavatel_id: ID dodavatele, od kterého se produkt dodává
        :param mnozstvi: Množství produktu, které se dodává
        """

        self.datum_dodani = datum_dodani
        self.produkt_id = produkt_id
        self.dodavatel_id = dodavatel_id
        self.mnozstvi = mnozstvi

    def insert(self, cursor):
        """
        Vložení dodávky do databáze

        :param cursor: Kurzor databáze
        """

        # Zkontroluje, jestli produkt s daným ID existuje
        check_product = "SELECT * FROM produkt WHERE id = %s"
        cursor.execute(check_product, (self.produkt_id,))
        product = cursor.fetchone()
        if not product:
            raise Exception("Error: Produkt s id {} neexistuje".format(self.produkt_id))

        # Zkontroluje, jestli dodavatel s daným ID existuje
        check_supplier = "SELECT * FROM dodavatel WHERE id = %s"
        cursor.execute(check_supplier, (self.dodavatel_id,))
        supplier = cursor.fetchone()
        if not supplier:
            raise Exception("Error: Dodavatel s id {} neexistuje".format(self.dodavatel_id))

        query = "INSERT INTO dodavka (datum_dodani, produkt_id, dodavatel_id, mnozstvi) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (self.datum_dodani, self.produkt_id, self.dodavatel_id, self.mnozstvi))


    def select(self, cursor):
        """
        Získání všech dodávek z databáze

        :param cursor: kurzor databáze
        """

        query = "SELECT * FROM dodavka"
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def update(self, cursor, id, attr, value):
        """
        Aktualizace dodávky v databázi

        :param cursor: kurzor databáze
        :param id: ID dodávky, která se má aktualizovat
        :param attr: Atribut, který se má aktualizovat
        :param value: Nová hodnota pro daný atribut
        """

        # Zkontrolování, zda existuje dodavka s daným ID
        check_supply_exists = "SELECT id FROM dodavka WHERE id = %s"
        cursor.execute(check_supply_exists, (id,))
        supply_exists = cursor.fetchone()

        if not supply_exists:
            raise ValueError(f"Dodavka s ID {id} neexistuje.")

        # Zkontrolování, zda objednavka má daný atribut
        query = f"SHOW COLUMNS FROM dodavka LIKE %s"
        cursor.execute(query, (attr,))
        attr_exists = cursor.fetchone() is not None

        if not attr_exists:
            raise ValueError(f"Dodavka nema atribut '{attr}'.")

        if (attr == 'produkt_id'):
            # Zkontrolování existence produktu s daným ID
            query = f"SELECT * FROM produkt WHERE id = %s"
            cursor.execute(query, (value,))
            produkt_exists = cursor.fetchone() is not None

            if not produkt_exists:
                raise ValueError(f"Produkt s ID {value} neexistuje.")

        if (attr == 'dodavatel_id'):
            # Zkontrolování existence dodavatele s daným ID
            query = f"SELECT * FROM dodavatel WHERE id = %s"
            cursor.execute(query, (value,))
            dodavatel_exists = cursor.fetchone() is not None

            if not dodavatel_exists:
                raise ValueError(f"Dodavatel s ID {value} neexistuje.")

        query = f"UPDATE dodavka SET {attr} = %s WHERE id = %s"
        cursor.execute(query, (value, id))


    def delete(self, cursor, id):
        """

        :param cursor: kurzor databáze
        :param id: ID dodavky ktera se ma smazat
        """

        # Zkontrolování existence dodavky s daným ID
        check_supply_exists = "SELECT id FROM dodavka WHERE id = %s"
        cursor.execute(check_supply_exists, (id,))
        supply_exists = cursor.fetchone()

        if not supply_exists:
            raise ValueError("The dodavka with the specified id does not exist.")

        # Smazani dodavky
        query = "DELETE FROM dodavka WHERE id = %s"
        cursor.execute(query, (id,))