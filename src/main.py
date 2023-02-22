from tables.zakaznik import Zakaznik
from tables.produkt import Produkt
from tables.dodavka import Dodavka
from tables.dodavatel import Dodavatel
from tables.objednavka import Objednavka

from src.config_setup import cfg_setup, cfg_read
from src.import_csv import CSVImport
from src.dbfacade import DBFacade


def main():
    """
    USER INTERFACE

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


    """
    #Vytvoreni instance databaze
    db = DBFacade()


    print("Vítejte v systému správy databáze!")
    print("===============================================")
    print("Aktualní konfigurace:\n")

    try:
        # Načtení konfiguračního souboru
        cfg_read("config/config.xml")
    except:
        # Chyba při načítání souboru config.xml
         print("Nebyl nalezen soubor config.xml ve slozce /config/")

    print("===============================================")
    default_config = input("Chcete nastavit vlastni konfiguracni soubor? | [y/n]:  ")

    if default_config == 'n':
        try:
            # Připojení k databázi
            db.connect()
        except:
            raise Exception("Nepodarilo se pripojit k databazi")
    elif default_config == 'y':
        try:
            # Nastavení konfiguračního souboru
            cfg_setup()
        except:
            raise Exception("Nepodarilo se nahrat soubor")

        try:
            # Připojení k databázi
            db.connect()
        except:
            raise Exception("Nepodarilo se pripojit k databazi")

        print("\nUSPESNE PRIPOJENI K DB")
        print("===============================================")
        print("Aktualni konfigurace:\n")
        cfg_read("config/config.xml")

    else:
        raise TypeError("Muzete zadat pouze [y/n]")


    while(True):
        print("\n=================== MENU ======================")
        print("Vyberte operaci:")
        print("1) Pracovat s tabulkami (zákazník, produkt, objednávka, dodávka, dodavatel)")
        print("2) Načíst data z CSV souboru do tabulek [zakaznik, produkt, dodavatel]")
        print("3) Provést transakci mezi dvěma účty")
        print("4) Zobrazit aktuální data ve všech tabulkách")
        print("5) Vygenerovat souhrný report objednávky a dodávky")
        print("0) Exit")
        menu_choice = int(input("Zadejte svůj výběr (0-5): "))

        # Pracovat s tabulkami
        if (menu_choice == 1):

            print("===============================================")
            print("\nSe kterou tabulkou chcete pracovat?")
            print("1) Zakaznik")
            print("2) Produkt")
            print("3) Objednavka")
            print("4) Dodavatel")
            print("5) Dodavka")
            print("0) Zpet do MENU")
            table_choice = int(input("Zadejte svůj výběr (0-5): "))

            #ZAKAZNIK
            if (table_choice == 1):
                zakaznik = Zakaznik(None, None, None)

                print("\nZvolte operaci kterou chcete provádět?")
                print("1) Select")
                print("2) Insert")
                print("3) Update")
                print("4) Delete")
                operation_choice = int(input("Zadejte svůj výběr (1-4): "))

                #SELECT - ZAKAZNIK
                if(operation_choice == 1):
                    print("===============================================")
                    print("Vypis vsech aktualnich zakazniku:")
                    print("ID | JMENO A PRIJMENI | EMAIL | KREDIT\n")
                    db.select("zakaznik")
                    print("===============================================")

                #INSERT - ZAKAZNIK
                elif(operation_choice == 2):
                    print("===============================================")
                    zakaznik_jmeno = input("Zadejte jmeno a prijmeni (Josef Novak):  ")
                    zakaznik_email = input("Zadejte email (josefnovak@seznam.cz): ")
                    zakaznik_kredit = int(input("Zadejte kredit: "))

                    if(zakaznik_kredit >= 0):
                        try:
                            zakaznik_insert = Zakaznik(zakaznik_jmeno, zakaznik_email, zakaznik_kredit)
                        except:
                            raise ValueError("Chyba v zadavani udaju zakaznika")

                        try:
                            db.insert(zakaznik_insert)
                        except:
                            raise Exception("Zakaznika se nepodarilo pridat do databaze")

                        print("\nZAKAZNIK BYL USPESNE NAHRAN")
                        print("===============================================")

                    else:
                        raise ValueError("Hodnota kreditu musi byt vetsi nez 0")

                #UPDATE - ZAKAZNIK
                elif(operation_choice == 3):
                    update_zakaznik_id = input("\nZadejte ID zakaznika u ktereho chcete update: ")
                    update_zakaznik_attr = input("Zadejte atribut ktery chcete upravit (jmeno, kontaktni_informace, kredit): ")
                    update_zakaznik_hodnota = input("Zadejte novou hodnotu: ")


                    if(update_zakaznik_attr == 'kredit' and int(update_zakaznik_hodnota) < 0):
                        raise ValueError("Hodnota kreditu musi byt vetsi nez 0")
                    else:
                         db.update(zakaznik, update_zakaznik_id, update_zakaznik_attr, update_zakaznik_hodnota)

                    print("\nUPDATE ZAKAZNIKA BYL USPESNY")
                    print("===============================================")

                #DELETE - ZAKAZNIK
                elif(operation_choice == 4):
                    delete_zakaznik_id = int(input("\nZadejte ID zakaznika ktereho chcete smazat: "))
                    db.delete(zakaznik, delete_zakaznik_id)

                    print("\nDELETE ZAKAZNIKA BYL USPESNY")
                    print("===============================================")

                else:
                    raise ValueError("Můžete vybrat číslo pouze 1-4")


            #PRODUKT
            elif (table_choice == 2):
                produkt = Produkt(None, None, None)

                print("\nZvolte operaci kterou chcete provádět?")
                print("1) Select")
                print("2) Insert")
                print("3) Update")
                print("4) Delete")
                operation_choice = int(input("Zadejte svůj výběr (1-4): "))

                # SELECT - PRODUKT
                if (operation_choice == 1):
                    print("===============================================")
                    print("Vypis vsech aktualnich produktu:")
                    print("ID | NAZEV | CENA | SKLADOVA ZASOBA\n")
                    db.select("produkt")
                    print("===============================================")

                #INSERT - PRODUKT
                elif (operation_choice == 2):
                    print("===============================================")
                    produkt_nazev = input("Zadejte nazev produktu (Jablko): ")
                    produkt_cena = int(input("Zadejte cenu: "))
                    produkt_skladova_zasoba = int(input("Zadejte skladovou zasobu: "))

                    if (produkt_cena >= 0 and produkt_skladova_zasoba >=0):
                        try:
                            produkt_insert = Produkt(produkt_nazev, produkt_cena, produkt_skladova_zasoba)
                        except:
                            raise ValueError("Chyba v zadavani udaju produktu")

                        try:
                            db.insert(produkt_insert)
                        except:
                            raise Exception("Produkt se nepodarilo pridat do databaze")

                        print("\nPRODUKT BYL USPESNE NAHRAN")
                        print("===============================================")

                    else:
                        raise ValueError("Cena produktu a jeho skladova zasoba musi byt vetsi nez 0")

                #UPDATE - PRODUKT
                elif (operation_choice == 3):
                    update_produkt_id = input("\nZadejte ID produktu u ktereho chcete UPDATE: ")
                    update_produkt_attr = input("Zadejte atribut ktery chcete upravit (nazev, cena, skladova_zasoba): ")
                    update_produkt_hodnota = input("Zadejte novou hodnotu: ")

                    if (update_produkt_attr == 'cena' and int(update_produkt_hodnota) < 0):
                        raise ValueError("Hodnota ceny musi byt vetsi nez 0")
                    elif(update_produkt_attr == 'skladova_zasoba' and int(update_produkt_hodnota) < 0):
                        raise ValueError("Hodnota skladove zasoby musi byt vetsi nez 0")
                    else:
                        db.update(produkt, update_produkt_id, update_produkt_attr, update_produkt_hodnota)

                    print("\nUPDATE PRODUKTU BYL USPESNY")
                    print("===============================================")

                #DELETE - PRODUKT
                elif (operation_choice == 4):
                    delete_produkt_id = int(input("\nZadejte ID produktu ktereho chcete smazat: "))
                    db.delete(produkt, delete_produkt_id)

                    print("\nDELETE PRODUKTU BYL USPESNY")
                    print("===============================================")

                else:
                    raise ValueError("Můžete vybrat číslo pouze 1-4")

            #OBJEDNAVKA
            elif (table_choice == 3):
                objednavka = Objednavka(None, None, None, None)

                print("\nZvolte operaci kterou chcete provádět?")
                print("1) Select")
                print("2) Insert")
                print("3) Update")
                print("4) Delete")
                operation_choice = int(input("Zadejte svůj výběr (1-4): "))

                # SELECT - OBJEDNAVKA
                if (operation_choice == 1):
                    print("===============================================")
                    print("Vypis vsech aktualnich objednavek:")
                    print("ID | DATUM | ID ZAKAZNIKA | ID PRODUKTU | MNOZSTVI | STAV\n")
                    db.select("objednavka")
                    print("===============================================")

                # INSERT - OBJEDNAVKA
                elif (operation_choice == 2):
                    print("===============================================")
                    objednavka_zakaznik_id = int(input("Zadejte ID zakaznika v objednavce: "))
                    objednavka_produkt_id = int(input("Zadejte ID produktu v objednavce: "))
                    objednavka_mnozstvi = int(input("Zadejte mnozstvi produktu v objednavce: "))
                    objednavka_stav = input("Zadejte stav objednavky ('odeslano',  'vyrizeno', 'stornovano'): ")

                    if(objednavka_stav in ['odeslano', 'vyrizeno', 'stornovano']):

                        if (objednavka_mnozstvi >= 0):
                            try:
                                objednavka_insert = Objednavka(objednavka_zakaznik_id, objednavka_produkt_id, objednavka_mnozstvi, objednavka_stav)
                            except:
                                raise ValueError("Chyba v zadavani udaju Objednavky")

                            try:
                                db.insert(objednavka_insert)
                            except:
                                raise Exception("Objednavku se nepodarilo pridat do databaze")

                            print("\nOBJEDNAVKA BYL USPESNE NAHRANA")
                            print("===============================================")
                        else:
                            raise ValueError("Mnozstvi objednavky musi byt vetsi nez 0")

                    else:
                        raise ValueError("Stav objednavky muze byt pouze: 'odeslano',  'vyrizeno', 'stornovano'")

                #UPDATE - OBJEDNAVKA
                elif (operation_choice == 3):
                    update_objednavka_id = input("\nZadejte ID objednavky u ktere chcete UPDATE: ")
                    update_objednavka_attr = input("Zadejte atribut ktery chcete upravit (zakaznik_id, produkt_id, mnozstvi, stav): ")
                    update_objednavka_hodnota = input("Zadejte novou hodnotu: ")

                    if (update_objednavka_attr == 'mnozstvi' and int(update_objednavka_hodnota) < 0):
                        raise ValueError("Hodnota mnozstvi musi byt vetsi nez 0")

                    if(update_objednavka_attr == 'stav' and update_objednavka_hodnota not in ['odeslano', 'vyrizeno', 'stornovano']):
                        raise ValueError("Stav objednavky muze byt pouze: 'odeslano', 'vyrizeno', 'stornovano'")
                    else:
                        db.update(objednavka, update_objednavka_id, update_objednavka_attr, update_objednavka_hodnota)

                    print("\nUPDATE OBJEDNAVKY BYL USPESNY")
                    print("===============================================")

                # DELETE - OBJEDNAVKA
                elif (operation_choice == 4):
                    delete_objednavka_id = int(input("\nZadejte ID objednavky kterou chcete smazat: "))
                    db.delete(objednavka, delete_objednavka_id)

                    print("\nDELETE OBJEDNAVKY BYL USPESNY")
                    print("===============================================")

                else:
                    raise ValueError("Můžete vybrat číslo pouze 1-4")

            #DODAVATEL
            elif (table_choice == 4):
                dodavatel = Dodavatel(None, None, None)

                print("\nZvolte operaci kterou chcete provádět?")
                print("1) Select")
                print("2) Insert")
                print("3) Update")
                print("4) Delete")
                operation_choice = int(input("Zadejte svůj výběr (1-4): "))

                # SELECT - DODAVATEL
                if (operation_choice == 1):
                    print("===============================================")
                    print("Vypis vsech aktualnich dodavatelu:")
                    print("ID | JMENO A PRIJMENI | EMAIL | ZAHRANICNI DODAVATEL\n")
                    db.select("dodavatel")
                    print("===============================================")


                # INSERT - DODAVATEL
                elif (operation_choice == 2):
                    print("===============================================")
                    dodavatel_jmeno = input("Zadejte jmeno a prijmeni (Josef Novak):  ")
                    dodavatel_email = input("Zadejte email (josefnovak@seznam.cz): ")
                    dodavatel_zahranicni = input("Zadejte zda se jedna o zahranicniho dodavatele !Case sensitive! (True/False) : ")

                    if (dodavatel_zahranicni in ["True", "False"]):
                        bool_dodavatel_zahranicni = dodavatel_zahranicni == "True"

                        try:
                            dodavatel_insert = Dodavatel(dodavatel_jmeno, dodavatel_email, bool_dodavatel_zahranicni)
                        except:
                            raise ValueError("Chyba v zadavani udaju dodavatele")

                        try:
                            db.insert(dodavatel_insert)
                        except:
                            raise Exception("Dodavatele se nepodarilo pridat do databaze")

                        print("\nDODAVATEL BYL USPESNE NAHRAN")
                        print("===============================================")

                    else:
                        raise ValueError("Dana hodnota muze byt pouze 'True' nebo 'False'")


                # UPDATE - DODAVATEL
                elif (operation_choice == 3):
                    update_dodavatel_id = input("\nZadejte ID dodavatele u ktereho chcete update: ")
                    update_dodavatel_attr = input("Zadejte atribut ktery chcete upravit (jmeno, kontaktni_informace, zahranicni): ")
                    update_dodavatel_hodnota = input("Zadejte novou hodnotu: ")

                    if (update_dodavatel_attr == 'zahranicni' and update_dodavatel_hodnota not in ["True", "False"]):
                        raise ValueError("Dana hodnota muze byt pouze 'True' nebo 'False'")
                    else:
                        if (update_dodavatel_attr == 'zahranicni'):
                            bool_update_dodavatel_hodnota = update_dodavatel_hodnota == "True"
                            db.update(dodavatel, update_dodavatel_id, update_dodavatel_attr, bool_update_dodavatel_hodnota)
                        else:
                            db.update(dodavatel, update_dodavatel_id, update_dodavatel_attr, update_dodavatel_hodnota)

                    print("\nUPDATE DODAVATELE BYL USPESNY")
                    print("===============================================")


                # DELETE - DODAVATEL
                elif (operation_choice == 4):
                    delete_dodavatel_id = int(input("\nZadejte ID dodavatele ktereho chcete smazat: "))
                    db.delete(dodavatel, delete_dodavatel_id)

                    print("\nDELETE DODAVATELE BYL USPESNY")
                    print("===============================================")

                else:
                    raise ValueError("Můžete vybrat číslo pouze 1-4")


            # DODAVKA
            elif (table_choice == 5):
                dodavka = Dodavka(None, None, None, None)

                print("\nZvolte operaci kterou chcete provádět?")
                print("1) Select")
                print("2) Insert")
                print("3) Update")
                print("4) Delete")
                operation_choice = int(input("Zadejte svůj výběr (1-4): "))

                # SELECT - DODAVKA
                if (operation_choice == 1):
                    print("===============================================")
                    print("Vypis vsech aktualnich dodavek:")
                    print("ID | DATUM DODANI | ID PRODUKTU | ID DODAVATELE | MNOZSTVI\n")
                    db.select("dodavka")
                    print("===============================================")


                # INSERT - DODAVKA
                elif (operation_choice == 2):
                    print("===============================================")
                    dodavka_datum_dodani = input("Zadejte datum dodani (YYYY-MM-DD-HH-MM):  ")
                    dodavka_produkt_id = int(input("Zadejte ID produktu: "))
                    dodavka_dodavatel_id = int(input("Zadejte ID dodavatele: "))
                    dodavka_mnozstvi = int(input("Zadejte mnozstvi dodavanych produktu: "))


                    if (dodavka_mnozstvi >= 0):
                        try:
                            dodavka_insert = Dodavka(dodavka_datum_dodani, dodavka_produkt_id, dodavka_dodavatel_id, dodavka_mnozstvi)
                        except:
                            raise ValueError("Chyba v zadavani udaju Dodavky")

                        try:
                            db.insert(dodavka_insert)
                        except:
                            raise Exception("Dodavku se nepodarilo pridat do databaze")

                        print("\nDODAVKA BYLA USPESNE NAHRANA")
                        print("===============================================")
                    else:
                        raise ValueError("Mnozstvi produktu u dodavky musi byt vetsi nez 0")


                # UPDATE - DODAVKA
                elif (operation_choice == 3):
                        update_dodavka_id = input("\nZadejte ID dodavky u ktere chcete UPDATE: ")
                        update_dodavka_attr = input("Zadejte atribut ktery chcete upravit (datum_dodani, produkt_id, dodavatel_id, mnozstvi): ")
                        update_dodavka_hodnota = input("Zadejte novou hodnotu: ")

                        if (update_dodavka_attr == 'mnozstvi' and int(update_dodavka_hodnota) < 0):
                            raise ValueError("Hodnota mnozstvi musi byt vetsi nez 0")

                        else:
                            db.update(dodavka, update_dodavka_id, update_dodavka_attr, update_dodavka_hodnota)

                        print("\nUPDATE DODAVKY BYL USPESNY")
                        print("===============================================")

                # DELETE - DODAVKA
                elif (operation_choice == 4):
                    delete_dodavka_id = int(input("\nZadejte ID dodavky kterou chcete smazat: "))
                    db.delete(dodavka, delete_dodavka_id)

                    print("\nDELETE DODAVKY BYL USPESNY")
                    print("===============================================")

                else:
                    raise ValueError("Můžete vybrat číslo pouze 1-4")


            elif(table_choice == 0):
                continue

            else:
                raise ValueError("Můžete vybrat číslo pouze 0-5")


        # Načíst data do CSV souboru do tabulek
        elif (menu_choice == 2):

            csv_import = CSVImport()

            print("===============================================")
            print("Overte si ze ve slozce /imports/ mate vas soubor")
            print("Soubor musi byt pojmenovany bud 'zakanik.csv', 'produkt.csv' nebo dodavatel.csv")
            print("===============================================")
            insert_choice = input("Chcete importovat do tabulky 'zakaznik', 'produkt' nebo 'dodavatel' | [z/p/d]: ")


            if(insert_choice == 'z'):
                try:
                    csv_import.import_zakaznik("imports/zakaznik.csv")
                except:
                    raise FileNotFoundError("Soubor 'zakaznik.csv' ve slozce /imports/ nebyl nalezen")

                csv_import.insert_to_database_zakaznik(db)

            elif(insert_choice == 'p'):
                try:
                    csv_import.import_produkt("imports/produkt.csv")
                except:
                    raise FileNotFoundError("Soubor 'produkt.csv' ve slozce /imports/ nebyl nalezen")

                csv_import.insert_to_database_produkt(db)

            elif (insert_choice == 'd'):
                try:
                    csv_import.import_dodavatel("imports/dodavatel.csv")
                except:
                    raise FileNotFoundError("Soubor 'dodavatel.csv' ve slozce /imports/ nebyl nalezen")

                csv_import.insert_to_database_dodavatel(db)

            else:
                raise TypeError("Muzete zadat pouze [z/p/d]")


            print("\nIMPORT SE ZDARIL")
            print("===============================================")

        # Provést transakci mezi dvěma účty
        elif (menu_choice == 3):
            print("===============================================")
            print("Vypis vsech aktualnich uctu zakazniku:")
            print("ID | JMENO A PRIJMENI | EMAIL | KREDIT")
            db.select("zakaznik")
            print("===============================================")
            transfer_choice_from = int(input("Zadejte id uctu ze ktereho chcete prevest kredit: "))
            transfer_choice_to = int(input("Zadejte id uctu na ktery chcete prevest kredit: "))
            transfer_choice_credit = int(input("Zadejte jakou castku chcete prevest: "))

            if(transfer_choice_credit >= 0):
                    db.transfer_credit(transfer_choice_from, transfer_choice_to, transfer_choice_credit)
            else:
                raise ValueError("Hodnota kreditu musi byt vetsi nez 0")

            print("\nTRANSAKCE SE ZDARILA")
            print("===============================================")
            print("Vypis vsech aktualnich uctu zakazniku po transakci:")
            print("ID | JMENO A PRIJMENI | EMAIL | KREDIT")
            db.select("zakaznik")
            print("===============================================")


        # Zobrazit aktuální data ve všech tabulkách
        elif(menu_choice == 4):
            print("\n===================== ZAKAZNICI =======================")
            print("ID | JMENO A PRIJMENI | EMAIL | KREDIT\n")
            db.select("zakaznik")
            print("\n====================== PRODUKTY =======================")
            print("ID | NAZEV | CENA | SKLADOVA ZASOBA\n")
            db.select("produkt")
            print("\n===================== OBJEDNAVKY =======================")
            print("ID | DATUM | ID ZAKAZNIKA | ID PRODUKTU | MNOZSTVI | STAV\n")
            db.select("objednavka")
            print("\n===================== DODAVATELE =======================")
            print("ID | JMENO A PRIJMENI | EMAIL | ZAHRANICNI DODAVATEL\n")
            db.select("dodavatel")
            print("\n===================== DODAVKY =======================")
            print("ID | DATUM DODANI | ID PRODUKTU | ID DODAVATELE | MNOZSTVI\n")
            db.select("dodavka")
            print("\n======= OBJEDNAVKY_PRODUKTY (Vazebni tabulka) ========")
            print("ID OBJEDNAVKY | ID PRODUKTU\n")
            db.select("objednavky_produkty")


        # Vygenerovat souhrný report objednávky a dodávky
        elif(menu_choice == 5):
            print("===============================================")
            print("REPORT OBJEDNAVEK:")
            print("OBJEDNAVKA ID | DATUM | JMENO ZAKAZNIKA | NAZEV PRODUKTU | CENA PRODUKTU | MNOZSTVI | STAV\n")
            db.order_details()
            print("\n===============================================")
            print("REPORT DODAVEK:")
            print("DODAVKA ID | DATUM DODANI | NAZEV PRODUKTU | MNOZSTVI | JMENO DODAVATELE | EMAIL DODAVATELE | ZAHRANICNI DODAVATEL\n")
            db.supply_details()
            print("===============================================")
            print("(Reporty byly ulozeny do souboru csv ve slozce /reports_export/)")
            print("===============================================")

        # Exit - ukonceni programu
        elif(menu_choice == 0):
            db.close()
            print("\nUkoncuji program...")
            break

        else:
            raise ValueError("Můžete vybrat číslo pouze 0-5")


if __name__ == "__main__":
    main()
