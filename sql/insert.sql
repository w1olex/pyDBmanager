-- Vložení dat do tabulky Zákazník
INSERT INTO zakaznik (jmeno, kontaktni_informace, kredit)
VALUES ('Jan Novák', 'jan.novak@email.cz', 5000),
('Petr Novotný', 'petr.novotny@email.cz', 6000),
('Eva Nováková', 'eva.novakova@email.cz', 3000);

-- Vložení dat do tabulky Produkt
INSERT INTO produkt (nazev, cena, skladova_zasoba)
VALUES ('Notebook Lenovo', 22000, 10),
('Monitor Dell', 9000, 5),
('Myš Logitech', 500, 20);

-- Vložení dat do tabulky Objednávka
INSERT INTO objednavka (datum_objednavky, zakaznik_id, produkt_id, mnozstvi, stav)
VALUES ('2022-10-01 12:00:00', 1, 1, 2, 'odeslano'),
('2022-10-02 14:00:00', 2, 2, 1, 'vyrizeno'),
('2022-10-03 16:00:00', 3, 3, 5, 'stornovano');

-- Vložení dat do tabulky Dodavatel
INSERT INTO dodavatel (jmeno, kontaktni_informace, zahranicni)
VALUES ('Dodavatel 1', 'dodavatel1@email.cz', 0),
('Dodavatel 2', 'dodavatel2@email.cz', 1),
('Dodavatel 3', 'dodavatel3@email.cz', 0);

-- Vložení dat do tabulky Dodávka
INSERT INTO dodavka (datum_dodani, produkt_id, dodavatel_id, mnozstvi)
VALUES ('2022-11-01 10:00:00', 1, 1, 5),
('2022-11-02 12:00:00', 2, 2, 2),
('2022-11-03 14:00:00', 3, 3, 10);

-- Vložení dat do tabulky objednávky_produkty
INSERT INTO objednavky_produkty (objednavka_id, produkt_id)
VALUES (1, 1),
(2, 2),
(3, 3);