Správa databáze Objednávek a Dodávek


POŽADAVKY KE SPUŠTĚNÍ PROGRAMU:


K spuštění programu je potřeba databáze alfa_3 v jazyku MySQL, která je k souboru přiložená ať už jako skript tak také jako export.

Aplikace potřebné k spuštění skriptu jsou MySQL WorkBench
(Nejlépe verze 8.0 a výše), jelikož jsem hostoval svojí databázi na localhostu
použil jsem aplikaci XAMPP ve které jsem spustil server MySQL

Po spuštění skriptu se nejdříve vytváří databáze alfa_3 a uživatel 
(user: uzivatel, heslo: alfa123)

CREATE USER 'uzivatel'@'localhost' IDENTIFIED BY 'alfa123';

Po vytvoření uživatele se mu následně udělí práva

GRANT ALL PRIVILEGES ON alfa_3.* TO 'uzivatel'@'localhost';


Následně se vytvoří 6 tabulek a 2 pohledy. 

Všechny zmiňované věci jsou naprosto nezbytné pro funkčnost programu


Uživatelské rozhraní k databázi je napsáno v jazyce Python (verze 3.8.10), bylo programováno ve vývojovém prostředí PyCharm (verze 2020.2.3).
Pro funkčnost propojení s databází byl nainstalován modul mysql-connector-python, který se instaluje pomocí příkazu:

>> pip install mysql-connector-python

Následná konfigurace připojení do databáze se zadává manuálně do konzole 
po spuštění programu. Všechny pokyny, které program vyžaduje od uživatele
jsou vypisovány do konzole.




USER INTERFACE:

    1. Nastaveni konfiguracniho souboru:
        Program nabidne uzivateli nastavit vlastni konfiguracni soubor,
        Uzivatel ma moznost nastavit: user, password, host, database.
        (Pokud dany 'user' nema  nastavene heslo nechte prazdne misto)

    2. Menu:
        Hlavni menu ma celkem 6 moznosti:
        1) Pracovat s tabulkami (zákazník, produkt, objednávka, dodávka, dodavatel)
            - uzivatel ma moznost provadet select, insert, update, delete pro vsechny stoly v databazi
            - pokud uzivatel chce smazat napr. zakaznika, ktery je jiz zapsan v nejake objednavce,
                program uzivatele upozorni co a kde je presne potreba smazat drive,
                uzivatel si muze pomoci selectu presne zobrazit jake id ma ktera objednavka

        2) Načíst data do CSV souboru do tabulek [zakaznik, produkt, dodavatel]
            - uzivatel muze nacist data do tabulek a produkt ze sveho csv souboru,
                Soubor musi byt pojmenovany bud 'zakanik.csv', 'produkt.csv nebo 'dodavatel.csv'
                a musi se nachazet ve slozce /imports/

        3) Provést transakci mezi dvěma účty
            - uzivatel ma moznost prevest kredit z jednoho uctu zakaznika na druhy
            - pokud ma zakaznik nedostatecny kredit probehle tzv. rollback (navraceni dat pred transakci)

        4) Zobrazit aktuální data ve všech tabulkach
            - uzivatel ma moznost zobrazit si vsechna aktualni data v databazi

        5) Vygenerovat souhrný report objednávky a dodávky
            - uzivatel ma moznost vygenerovat 2 reporty:
                a) podrobnosti_objednavky
                    - tento report slouzi k zobrazeni objednavky a prislusnych dat k ni
                    - obsahuje informace celkove z 4 tabulek:
                        objednavka, zakaznik, objednavky_produkty, produkt
                    - prezentuje data:
                        objednavka.id,
                        objednavka.datum_objednavky,
                        zakaznik.jmeno,
                        produkt.nazev,
                        produkt.cena,
                        objednavka.mnozstvi,
                        objednavka.stav

                b) podrobnosti_dodavky
                    - tento report slouzi k zobrazeni dodavky a prislusnych dat k ni
                    - obsahuje informace celkove z 3 tabulek:
                        dodavka, produkt, dodavatel
                    - prezentuje data:
                        dodavka.id,
                        dodavka.datum_dodani,
                        produkt.nazev,
                        dodavka.mnozstvi,
                        dodavatel.jmeno,
                        dodavatel.kontaktni_informace,
                        dodavatel.zahranicni

            - tyto reporty se nasledne ulozi do csv souboru do slozky /reports_export/

        0) Exit
            - ukonceni programu

        Toto Menu se po kazde dokoncene operaci opet zobrazi,
        dokud uzivatel nezada 0 tudiz Exit
