class Produkt:
    def __init__(self, nazev, cena, skladova_zasoba):
        """
        Konstruktor třídy Produkt, který inicializuje atributy nazev, cena a skladova zasoba.

        :param nazev: název produktu
        :param cena: cena produktu
        :param skladova_zasoba: množství produktů na skladě
        """

        self.nazev = nazev
        self.cena = cena
        self.skladova_zasoba = skladova_zasoba

    def insert(self, cursor):
        """
        Vložení produktu do databáze.

        :param cursor: kurzor databáze
        """
        query = "INSERT INTO produkt (nazev, cena, skladova_zasoba) VALUES (%s, %s, %s)"
        cursor.execute(query, (self.nazev, self.cena, self.skladova_zasoba))

    def select(self, cursor):
        """
        Výběr všech produktů z databáze

        :param cursor: kurzor databáze
        """

        query = "SELECT * FROM produkt"
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def update(self, cursor, id, attr, value):
        """
        Tato funkce aktualizuje data o produktu s daným ID v databázi.

        :param cursor: kurzor databáze
        :param id: ID produktu
        :param attr: název atributu, který se má aktualizovat
        :param value: nová hodnota atributu
        """

        # Zkontrolování, zda existuje produkt s daným ID
        query = f"SELECT id FROM produkt WHERE id = %s"
        cursor.execute(query, (id,))
        if cursor.fetchone() is None:
            raise ValueError(f"Produkt s ID {id} neexistuje.")

        # Zkontrolování, zda produkt má daný atribut
        query = f"SHOW COLUMNS FROM produkt LIKE %s"
        cursor.execute(query, (attr,))
        if cursor.fetchone() is None:
            raise ValueError(f"Produkt nema atribut '{attr}'.")

        # Aktualizace produktu s daným ID a atributem
        query = f"UPDATE produkt SET {attr} = %s WHERE id = %s"
        cursor.execute(query, (value, id))


    def delete(self, cursor, id):
        """
        Tato funkce smaže produkt s daným ID z databáze.

        :param cursor: kurzor databáze
        :param id: ID produktu
        """

        # Zkontrolování existence produktu s daným ID
        query = "SELECT COUNT(*) FROM produkt WHERE id = %s"
        cursor.execute(query, (id,))
        if cursor.fetchone()[0] == 0:
            raise ValueError("Produkt s ID {} neexistuje.".format(id))

        # Zkontrolování existence produktu v objednávce
        query = "SELECT COUNT(*) FROM objednavka WHERE produkt_id = %s"
        cursor.execute(query, (id,))
        if cursor.fetchone()[0] > 0:
            raise ValueError(
                "Produkt s ID {} nelze smazat, jelikoz se vyskytuje v objednavce, \nSmazte nejdrive objednavku s produkt_id {}.".format(id,id))

        # Zkontrolování existence produktu v dodávce
        query = "SELECT COUNT(*) FROM dodavka WHERE produkt_id = %s"
        cursor.execute(query, (id,))
        if cursor.fetchone()[0] > 0:
            raise ValueError("Produkt with ID {} nelze smazat, jelikoz se vyskytuje v dodavce, "
                             "\nSmazte nejdrive dodavku s produkt_id {}.".format(id,id))

        # Smazání produktu
        query = "DELETE FROM produkt WHERE id = %s"
        cursor.execute(query, (id,))