CREATE DATABASE alfa_3;
use alfa_3;

CREATE USER 'uzivatel'@'localhost' IDENTIFIED BY 'alfa123';
GRANT ALL PRIVILEGES ON alfa_3.* TO 'uzivatel'@'localhost';
FLUSH PRIVILEGES;


-- Vytvoření tabulky Zákazník
CREATE TABLE zakaznik (
  id INT PRIMARY KEY AUTO_INCREMENT,
  jmeno VARCHAR(255) NOT NULL,
  kontaktni_informace VARCHAR(255) NOT NULL,
  kredit INT NOT NULL
);

-- Vytvoření tabulky Produkt
CREATE TABLE produkt (
  id INT PRIMARY KEY AUTO_INCREMENT,
  nazev VARCHAR(255) NOT NULL,
  cena FLOAT(10,2) NOT NULL,
  skladova_zasoba INT NOT NULL
);

-- Vytvoření tabulky Objednávka
CREATE TABLE objednavka (
  id INT PRIMARY KEY AUTO_INCREMENT,
  datum_objednavky DATETIME NOT NULL,
  zakaznik_id INT NOT NULL,
  produkt_id INT NOT NULL,
  mnozstvi INT NOT NULL,
  stav ENUM('odeslano', 'vyrizeno', 'stornovano') NOT NULL,
  FOREIGN KEY (zakaznik_id) REFERENCES zakaznik(id),
  FOREIGN KEY (produkt_id) REFERENCES produkt(id)
);

-- Vytvoření tabulky Dodavatel
CREATE TABLE dodavatel (
  id INT PRIMARY KEY AUTO_INCREMENT,
  jmeno VARCHAR(255) NOT NULL,
  kontaktni_informace VARCHAR(255) NOT NULL,
  zahranicni BOOLEAN NOT NULL
);

-- Vytvoření tabulky Dodávka
CREATE TABLE dodavka (
  id INT PRIMARY KEY AUTO_INCREMENT,
  datum_dodani DATETIME NOT NULL,
  produkt_id INT NOT NULL,
  dodavatel_id INT NOT NULL,
  mnozstvi INT NOT NULL,
  FOREIGN KEY (produkt_id) REFERENCES produkt(id),
  FOREIGN KEY (dodavatel_id) REFERENCES dodavatel(id)
);

-- Vytvoření vazby M:N mezi tabulkami Objednávky a Produkty
CREATE TABLE objednavky_produkty (
  objednavka_id INT NOT NULL,
  produkt_id INT NOT NULL,
  PRIMARY KEY (objednavka_id, produkt_id),
  FOREIGN KEY (objednavka_id) REFERENCES objednavka(id),
  FOREIGN KEY (produkt_id) REFERENCES produkt(id)
);


-- Vytvoření pohledu pro zobrazení všech objednávek s informacemi o zákazníkovi a produktu

CREATE VIEW podrobnosti_objednavky AS
SELECT o.id, o.datum_objednavky, z.jmeno, p.nazev, p.cena, o.mnozstvi, o.stav
FROM objednavka AS o
JOIN zakaznik AS z ON z.id = o.zakaznik_id
JOIN objednavky_produkty AS op ON op.objednavka_id = o.id
JOIN produkt AS p ON p.id = op.produkt_id;

-- Vytvoření pohledu pro zobrazení všech dodávek s informacemi o produktu a dodavateli

CREATE VIEW podrobnosti_dodavky AS
SELECT d.id, d.datum_dodani, p.nazev, d.mnozstvi, de.jmeno, de.kontaktni_informace, de.zahranicni
FROM dodavka AS d
JOIN produkt AS p ON p.id = d.produkt_id
JOIN dodavatel AS de ON de.id = d.dodavatel_id;