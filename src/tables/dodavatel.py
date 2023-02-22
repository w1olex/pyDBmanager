class Dodavatel:
    def __init__(self, jmeno, kontaktni_informace, zahranicni):
        """
        Konstruktor třídy Dodavatel, který inicializuje atributy jméno,
        kontaktní informace a zda se jedna o zahranicniho dodavatele.

        :param jmeno: Jméno dodavatele
        :param kontaktni_informace: Kontaktní informace dodavatele
        :param zahranicni: Informace, zda-li je dodavatel zahraniční
        """

        self.jmeno = jmeno
        self.kontaktni_informace = kontaktni_informace
        self.zahranicni = zahranicni

    def insert(self, cursor):
        """
        Vložení dodavatele do databáze

        :param cursor: kurzor databáze
        """

        query = "INSERT INTO dodavatel (jmeno, kontaktni_informace, zahranicni) VALUES (%s, %s, %s)"
        cursor.execute(query, (self.jmeno, self.kontaktni_informace, self.zahranicni))

    def select(self, cursor):
        """
        Vybrání všech dodavatelů z databáze

        :param cursor: kurzor databáze
        """

        query = "SELECT * FROM dodavatel"
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def update(self, cursor, id, attr, value):
        """
        Aktualizace atributu dodavatele v databázi

        :param cursor: kurzor databáze
        :param id: ID dodavatele, který se má aktualizovat
        :param attr: Název atributu, který se má aktualizovat
        :param value: Nová hodnota atributu
        """

        # Zkontrolování, zda-li dodavatel s daným ID existuje
        query = f"SELECT id FROM dodavatel WHERE id = %s"
        cursor.execute(query, (id,))
        if cursor.fetchone() is None:
            raise ValueError(f"Dodavatel s ID {id} neexistuje.")

        # Zkontrolování, zda-li dodavatel má daný atribut
        query = f"SHOW COLUMNS FROM dodavatel LIKE %s"
        cursor.execute(query, (attr,))
        if cursor.fetchone() is None:
            raise ValueError(f"Dodavatel nema atribut '{attr}'.")

        query = f"UPDATE dodavatel SET {attr} = %s WHERE id = %s"
        cursor.execute(query, (value, id))


    def delete(self, cursor, id):
        """
        Smaže dodavatele s daným ID.

        :param cursor: kurzor databáze
        :param id: ID dodavatele, který se má smazat
        """

        # Zkontroluje, zda dodavatel s daným ID existuje
        query = "SELECT id FROM dodavatel WHERE id = %s"
        cursor.execute(query, (id,))
        if cursor.fetchone() is None:
            raise ValueError(f"Dodavatel s ID {id} neexistuje.")

        # Zkontroluje, zda dodavatel s daným ID není v tabulce dodavka
        query = "SELECT * FROM dodavka WHERE dodavatel_id = %s"
        cursor.execute(query, (id,))

        if cursor.fetchone():
            raise Exception("Dodavatel s timto ID se nachazi v tabulce dodavka."
                            "\nPro jeho smazani nejprve smazte polozku v tabulce dodavka s dodavatel_id {}".format(id))

        # Smaže dodavatele s daným ID
        query = "DELETE FROM dodavatel WHERE id = %s"
        cursor.execute(query, (id,))