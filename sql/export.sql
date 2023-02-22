CREATE DATABASE  IF NOT EXISTS `alfa_3` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `alfa_3`;
-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
-- Host: 127.0.0.1    Database: alfa_3
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.24-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `dodavatel`
--

DROP TABLE IF EXISTS `dodavatel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dodavatel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jmeno` varchar(255) NOT NULL,
  `kontaktni_informace` varchar(255) NOT NULL,
  `zahranicni` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dodavatel`
--

LOCK TABLES `dodavatel` WRITE;
/*!40000 ALTER TABLE `dodavatel` DISABLE KEYS */;
INSERT INTO `dodavatel` VALUES (1,'Dodavatel 1','dodavatel1@email.cz',0),(2,'Dodavatel 2','dodavatel2@email.cz',1),(3,'Dodavatel 3','dodavatel3@email.cz',0);
/*!40000 ALTER TABLE `dodavatel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dodavka`
--

DROP TABLE IF EXISTS `dodavka`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dodavka` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `datum_dodani` datetime NOT NULL,
  `produkt_id` int(11) NOT NULL,
  `dodavatel_id` int(11) NOT NULL,
  `mnozstvi` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `produkt_id` (`produkt_id`),
  KEY `dodavatel_id` (`dodavatel_id`),
  CONSTRAINT `dodavka_ibfk_1` FOREIGN KEY (`produkt_id`) REFERENCES `produkt` (`id`),
  CONSTRAINT `dodavka_ibfk_2` FOREIGN KEY (`dodavatel_id`) REFERENCES `dodavatel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dodavka`
--

LOCK TABLES `dodavka` WRITE;
/*!40000 ALTER TABLE `dodavka` DISABLE KEYS */;
INSERT INTO `dodavka` VALUES (1,'2022-11-01 10:00:00',1,1,5),(2,'2022-11-02 12:00:00',2,2,2),(3,'2022-11-03 14:00:00',3,3,10);
/*!40000 ALTER TABLE `dodavka` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `objednavka`
--

DROP TABLE IF EXISTS `objednavka`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `objednavka` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `datum_objednavky` datetime NOT NULL,
  `zakaznik_id` int(11) NOT NULL,
  `produkt_id` int(11) NOT NULL,
  `mnozstvi` int(11) NOT NULL,
  `stav` enum('odeslano','vyrizeno','stornovano') NOT NULL,
  PRIMARY KEY (`id`),
  KEY `zakaznik_id` (`zakaznik_id`),
  KEY `produkt_id` (`produkt_id`),
  CONSTRAINT `objednavka_ibfk_1` FOREIGN KEY (`zakaznik_id`) REFERENCES `zakaznik` (`id`),
  CONSTRAINT `objednavka_ibfk_2` FOREIGN KEY (`produkt_id`) REFERENCES `produkt` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `objednavka`
--

LOCK TABLES `objednavka` WRITE;
/*!40000 ALTER TABLE `objednavka` DISABLE KEYS */;
INSERT INTO `objednavka` VALUES (1,'2022-10-01 12:00:00',1,1,2,'odeslano'),(2,'2022-10-02 14:00:00',2,2,1,'vyrizeno'),(3,'2022-10-03 16:00:00',3,3,5,'stornovano');
/*!40000 ALTER TABLE `objednavka` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `objednavky_produkty`
--

DROP TABLE IF EXISTS `objednavky_produkty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `objednavky_produkty` (
  `objednavka_id` int(11) NOT NULL,
  `produkt_id` int(11) NOT NULL,
  PRIMARY KEY (`objednavka_id`,`produkt_id`),
  KEY `produkt_id` (`produkt_id`),
  CONSTRAINT `objednavky_produkty_ibfk_1` FOREIGN KEY (`objednavka_id`) REFERENCES `objednavka` (`id`),
  CONSTRAINT `objednavky_produkty_ibfk_2` FOREIGN KEY (`produkt_id`) REFERENCES `produkt` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `objednavky_produkty`
--

LOCK TABLES `objednavky_produkty` WRITE;
/*!40000 ALTER TABLE `objednavky_produkty` DISABLE KEYS */;
INSERT INTO `objednavky_produkty` VALUES (1,1),(2,2),(3,3);
/*!40000 ALTER TABLE `objednavky_produkty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `podrobnosti_dodavky`
--

DROP TABLE IF EXISTS `podrobnosti_dodavky`;
/*!50001 DROP VIEW IF EXISTS `podrobnosti_dodavky`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `podrobnosti_dodavky` AS SELECT 
 1 AS `id`,
 1 AS `datum_dodani`,
 1 AS `nazev`,
 1 AS `mnozstvi`,
 1 AS `jmeno`,
 1 AS `kontaktni_informace`,
 1 AS `zahranicni`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `podrobnosti_objednavky`
--

DROP TABLE IF EXISTS `podrobnosti_objednavky`;
/*!50001 DROP VIEW IF EXISTS `podrobnosti_objednavky`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `podrobnosti_objednavky` AS SELECT 
 1 AS `id`,
 1 AS `datum_objednavky`,
 1 AS `jmeno`,
 1 AS `nazev`,
 1 AS `cena`,
 1 AS `mnozstvi`,
 1 AS `stav`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `produkt`
--

DROP TABLE IF EXISTS `produkt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `produkt` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nazev` varchar(255) NOT NULL,
  `cena` float(10,2) NOT NULL,
  `skladova_zasoba` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produkt`
--

LOCK TABLES `produkt` WRITE;
/*!40000 ALTER TABLE `produkt` DISABLE KEYS */;
INSERT INTO `produkt` VALUES (1,'Notebook Lenovo',22000.00,10),(2,'Monitor Dell',9000.00,5),(3,'Myš Logitech',500.00,20);
/*!40000 ALTER TABLE `produkt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zakaznik`
--

DROP TABLE IF EXISTS `zakaznik`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `zakaznik` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jmeno` varchar(255) NOT NULL,
  `kontaktni_informace` varchar(255) NOT NULL,
  `kredit` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zakaznik`
--

LOCK TABLES `zakaznik` WRITE;
/*!40000 ALTER TABLE `zakaznik` DISABLE KEYS */;
INSERT INTO `zakaznik` VALUES (1,'Jan Novák','jan.novak@email.cz',5000),(2,'Petr Novotný','petr.novotny@email.cz',6000),(3,'Eva Nováková','eva.novakova@email.cz',3000);
/*!40000 ALTER TABLE `zakaznik` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `podrobnosti_dodavky`
--

/*!50001 DROP VIEW IF EXISTS `podrobnosti_dodavky`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `podrobnosti_dodavky` AS select `d`.`id` AS `id`,`d`.`datum_dodani` AS `datum_dodani`,`p`.`nazev` AS `nazev`,`d`.`mnozstvi` AS `mnozstvi`,`de`.`jmeno` AS `jmeno`,`de`.`kontaktni_informace` AS `kontaktni_informace`,`de`.`zahranicni` AS `zahranicni` from ((`dodavka` `d` join `produkt` `p` on(`p`.`id` = `d`.`produkt_id`)) join `dodavatel` `de` on(`de`.`id` = `d`.`dodavatel_id`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `podrobnosti_objednavky`
--

/*!50001 DROP VIEW IF EXISTS `podrobnosti_objednavky`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `podrobnosti_objednavky` AS select `o`.`id` AS `id`,`o`.`datum_objednavky` AS `datum_objednavky`,`z`.`jmeno` AS `jmeno`,`p`.`nazev` AS `nazev`,`p`.`cena` AS `cena`,`o`.`mnozstvi` AS `mnozstvi`,`o`.`stav` AS `stav` from (((`objednavka` `o` join `zakaznik` `z` on(`z`.`id` = `o`.`zakaznik_id`)) join `objednavky_produkty` `op` on(`op`.`objednavka_id` = `o`.`id`)) join `produkt` `p` on(`p`.`id` = `op`.`produkt_id`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-02-03 22:34:13
