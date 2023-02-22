class Zakaznik:
    def __init__(self, jmeno, kontaktni_informace, kredit):
        """
        Konstruktor třídy Zakaznik, který inicializuje atributy jméno, kontaktní informace a kredit.

        :param jmeno: jmeno a prijmeni zakaznika
        :type: jmeno: str
        :param kontaktni_informace: email zakaznika
        :type kontaktni_informace: str
        :param kredit: kredit zakaznika
        :type kredit: int
        """

        self.jmeno = jmeno
        self.kontaktni_informace = kontaktni_informace
        self.kredit = kredit

    def insert(self, cursor):
        """
        Tato funkce vkládá data o zákazníkovi z instance třídy Zakaznik do databáze.

        :param cursor: kurzor databáze
        """

        query = "INSERT INTO zakaznik (jmeno, kontaktni_informace, kredit) VALUES (%s, %s, %s)"
        cursor.execute(query, (self.jmeno, self.kontaktni_informace, self.kredit))

    def select(self, cursor):
        """
        Tato funkce vybere data o všech zákaznících z databáze.

        :param cursor: kurzor databáze
        """

        query = "SELECT * FROM zakaznik"
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def update(self, cursor, id, attr, value):
        """
        Tato funkce aktualizuje data o zákazníkovi s daným ID v databázi.

        :param id: ID zákazníka, který se má aktualizovat
        :param attr: název atributu, který se má aktualizovat
        :param value: nová hodnota atributu
        :param cursor: kurzor databáze
        """

        # Kontrola, zda zákazník s daným ID existuje
        query = f"SELECT id FROM zakaznik WHERE id = %s"
        cursor.execute(query, (id,))
        if cursor.fetchone() is None:
            raise ValueError(f"Zakaznik s ID {id} neexistuje.")

        # Kontrola, zda zákazník má daný atribut
        query = f"SHOW COLUMNS FROM zakaznik LIKE %s"
        cursor.execute(query, (attr,))
        if cursor.fetchone() is None:
            raise ValueError(f"Zakaznik nema atribut '{attr}'.")

        # Aktualizace zákazníka s daným ID a atributem
        query = f"UPDATE zakaznik SET {attr} = %s WHERE id = %s"
        cursor.execute(query, (value, id))


    def delete(self, cursor, id):
        """
         Tato funkce smaže zákazníka s daným ID z databáze.

        :param cursor: kurzor databáze
        :param id: ID zákazníka, který se má smazat
        """

        # Kontrola, zda existuje zákazník s daným ID
        query = "SELECT id FROM zakaznik WHERE id = %s"
        cursor.execute(query, (id,))
        if cursor.fetchone() is None:
            raise ValueError(f"Zakaznik s ID {id} neexistuje.")

        # Kontrola, zda zákazník s daným ID není zároveň zákazníkem v tabulce objednávka
        query = "SELECT id FROM objednavka WHERE zakaznik_id = %s"
        cursor.execute(query, (id,))
        if cursor.fetchone() is not None:
            raise ValueError(f"Nelze smazat Zakaznika s ID {id}, jelikoz se nachazi jiz v objednavce. \nSmazte nejdrive objednavku se zakaznik_id {id}.")

        # Smazání zákazníka s daným ID
        query = "DELETE FROM zakaznik WHERE id = %s"
        cursor.execute(query, (id,))

