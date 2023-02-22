import xml.etree.ElementTree as ET


def cfg_setup():
    """
    Funkce pro nastaveni a ulozeni konfiguracniho souboru pro pripojeni k databazi.
    Ziska vstup od uzivatele (jmeno uzivatele, heslo, host a nazev databaze)
    a vytvori xml soubor s timto konfiguracnim nastavenim.
    """

    # Ziska vstupy od uzivatele
    user = input("Zadejte uzivatele (user): ")
    password = input("Zadejte heslo (password): ")
    host = input("Zadejte host: ")
    database = input("Zadejte databazi: ")

    # Vytvoreni XML souboru
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <config>
        <user>{}</user>
        <password>{}</password>
        <host>{}</host>
        <database>{}</database>
    </config>""".format(user, password, host, database)

    with open("config/config.xml", "w") as f:
        f.write(xml)



def cfg_read(file):
    """
    Funkce pro cteni konfiguracniho souboru.
    Nacte xml soubor a vypise nastaveni pro pripojeni k databazi (jmeno uzivatele, heslo, host a nazev databaze).

    :param file: Cesta k souboru s konfiguracnim nastavenim.
    """

    tree = ET.parse(file)
    root = tree.getroot()
    print("user =", root.find("user").text)
    print("password =", root.find("password").text)
    print("host =", root.find("host").text)
    print("database =", root.find("database").text)

