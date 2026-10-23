-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: AirportDB
-- ------------------------------------------------------
-- Server version	8.0.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `AirportDB`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `AirportDB` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `AirportDB`;

--
-- Table structure for table `aircraft`
--

DROP TABLE IF EXISTS `aircraft`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `aircraft` (
  `aircraft_id` int NOT NULL,
  `model` varchar(60) NOT NULL,
  `capacity` int DEFAULT NULL,
  `manufacturer` varchar(50) DEFAULT NULL,
  `status` varchar(20) DEFAULT 'Available',
  PRIMARY KEY (`aircraft_id`),
  CONSTRAINT `aircraft_chk_1` CHECK ((`capacity` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aircraft`
--

LOCK TABLES `aircraft` WRITE;
/*!40000 ALTER TABLE `aircraft` DISABLE KEYS */;
INSERT INTO `aircraft` VALUES (201,'Airbus A320',190,'Airbus','Available'),(202,'Boeing 737',200,'Boeing','Available'),(601,'Airbus A321',220,'Airbus','Available'),(602,'Boeing 777',396,'Boeing','Available'),(603,'Boeing 787',318,'Boeing','Available'),(604,'Airbus A330',300,'Airbus','Available'),(605,'Airbus A319',156,'Airbus','Available'),(606,'Boeing 737 MAX',210,'Boeing','Available'),(607,'Airbus A350-900',325,'Airbus','Available'),(608,'Boeing 747',416,'Boeing','Maintenance'),(609,'Airbus A220',145,'Airbus','Available'),(610,'Boeing 767',375,'Boeing','Available'),(611,'Airbus A340',350,'Airbus','Available'),(612,'Embraer E190',114,'Embraer','Available'),(613,'Embraer E195',132,'Embraer','Available'),(614,'ATR 72',78,'ATR','Available'),(615,'ATR 42',50,'ATR','Maintenance'),(616,'Airbus A320neo',186,'Airbus','Available'),(617,'Boeing 737-800',189,'Boeing','Available'),(618,'Airbus A321neo',244,'Airbus','Available'),(619,'Boeing 787-9',296,'Boeing','Available'),(620,'Airbus A330neo',310,'Airbus','Available');
/*!40000 ALTER TABLE `aircraft` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `airport`
--

DROP TABLE IF EXISTS `airport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `airport` (
  `airport_id` int NOT NULL,
  `airport_name` varchar(100) NOT NULL,
  `city` varchar(50) NOT NULL,
  `country` varchar(50) NOT NULL,
  `airport_code` char(3) DEFAULT NULL,
  PRIMARY KEY (`airport_id`),
  UNIQUE KEY `airport_code` (`airport_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `airport`
--

LOCK TABLES `airport` WRITE;
/*!40000 ALTER TABLE `airport` DISABLE KEYS */;
INSERT INTO `airport` VALUES (101,'Chhatrapati Shivaji Airport','Mumbai','India','BOM'),(102,'Indira Gandhi Airport','Delhi','India','DEL'),(103,'Kempegowda Airport','Bangalore','India','BLR'),(104,'Rajiv Gandhi Airport','Hyderabad','India','HYD'),(501,'Rajiv Gandhi International Airport','Hyderabad','India','RGA'),(502,'Chennai International Airport','Chennai','India','CNI'),(503,'Netaji Subhas Chandra Bose Airport','Kolkata','India','NSC'),(504,'Cochin International Airport','Kochi','India','COK'),(505,'Pune International Airport','Pune','India','PUN'),(506,'Goa International Airport','Goa','India','GOI'),(507,'Jaipur International Airport','Jaipur','India','JPR'),(508,'Sardar Vallabhbhai Patel Airport','Ahmedabad','India','SVP'),(509,'Chaudhary Charan Singh Airport','Lucknow','India','CCS'),(510,'Lokpriya Gopinath Bordoloi Airport','Guwahati','India','LGB'),(511,'Biju Patnaik International Airport','Bhubaneswar','India','BPI'),(512,'Trivandrum International Airport','Thiruvananthapuram','India','TRV'),(513,'Devi Ahilyabai Holkar Airport','Indore','India','DAH'),(514,'Lal Bahadur Shastri Airport','Varanasi','India','LBS'),(515,'Coimbatore International Airport','Coimbatore','India','CBR'),(516,'Bagdogra Airport','Siliguri','India','BDG'),(517,'Mangalore International Airport','Mangalore','India','MNG'),(518,'Dr. Babasaheb Ambedkar Airport','Nagpur','India','DBA'),(519,'Chandigarh International Airport','Chandigarh','India','CDG'),(520,'Birsa Munda Airport','Ranchi','India','BRM');
/*!40000 ALTER TABLE `airport` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `booking`
--

DROP TABLE IF EXISTS `booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `booking` (
  `booking_id` int NOT NULL,
  `passenger_id` int DEFAULT NULL,
  `flight_id` int DEFAULT NULL,
  `booking_date` date DEFAULT NULL,
  `seat_no` varchar(5) DEFAULT NULL,
  `booking_status` varchar(20) DEFAULT 'Confirmed',
  PRIMARY KEY (`booking_id`),
  KEY `passenger_id` (`passenger_id`),
  KEY `flight_id` (`flight_id`),
  CONSTRAINT `booking_ibfk_1` FOREIGN KEY (`passenger_id`) REFERENCES `passenger` (`passenger_id`),
  CONSTRAINT `booking_ibfk_2` FOREIGN KEY (`flight_id`) REFERENCES `flight` (`flight_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booking`
--

LOCK TABLES `booking` WRITE;
/*!40000 ALTER TABLE `booking` DISABLE KEYS */;
INSERT INTO `booking` VALUES (801,501,301,'2026-07-10','1A','Confirmed'),(802,502,302,'2026-07-11','2B','Confirmed'),(803,503,303,'2026-07-12','3C','Confirmed'),(804,504,701,'2026-07-20','4A','Confirmed'),(805,505,702,'2026-07-20','5B','Confirmed'),(806,506,703,'2026-07-21','6C','Confirmed'),(807,507,704,'2026-07-21','7A','Confirmed'),(808,508,705,'2026-07-22','8B','Confirmed'),(809,509,706,'2026-07-22','9C','Confirmed'),(810,510,707,'2026-07-23','10A','Confirmed'),(811,511,708,'2026-07-23','11B','Confirmed'),(812,512,709,'2026-07-24','12C','Confirmed'),(813,513,710,'2026-07-24','13A','Confirmed'),(814,514,711,'2026-07-25','14B','Confirmed'),(815,515,712,'2026-07-25','15C','Confirmed'),(816,516,713,'2026-07-26','16A','Confirmed'),(817,517,714,'2026-07-26','17B','Confirmed'),(818,518,715,'2026-07-27','18C','Confirmed'),(819,519,716,'2026-07-27','19A','Confirmed'),(820,520,717,'2026-07-28','20B','Confirmed'),(821,521,718,'2026-07-28','21C','Confirmed'),(822,522,719,'2026-07-29','22A','Confirmed'),(823,523,720,'2026-07-29','23B','Confirmed'),(824,524,301,'2026-07-30','24C','Confirmed'),(825,525,302,'2026-07-30','25A','Confirmed'),(826,526,303,'2026-07-31','26B','Confirmed'),(827,527,701,'2026-08-01','27C','Confirmed'),(828,528,702,'2026-08-01','28A','Confirmed'),(829,529,703,'2026-08-02','29B','Confirmed'),(830,530,704,'2026-08-02','30C','Confirmed'),(831,531,705,'2026-08-03','31A','Confirmed'),(832,532,706,'2026-08-03','32B','Confirmed'),(833,533,707,'2026-08-04','33C','Confirmed'),(834,534,708,'2026-08-04','34A','Confirmed'),(835,535,709,'2026-08-05','35B','Confirmed'),(836,536,710,'2026-08-05','36C','Confirmed'),(837,537,711,'2026-08-06','37A','Confirmed'),(838,538,712,'2026-08-06','38B','Confirmed'),(839,539,713,'2026-08-07','39C','Confirmed'),(840,540,714,'2026-08-07','40A','Confirmed');
/*!40000 ALTER TABLE `booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flight`
--

DROP TABLE IF EXISTS `flight`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flight` (
  `flight_id` int NOT NULL,
  `flight_no` varchar(10) NOT NULL,
  `source_airport` int DEFAULT NULL,
  `destination_airport` int DEFAULT NULL,
  `aircraft_id` int DEFAULT NULL,
  `departure_time` datetime DEFAULT NULL,
  `arrival_time` datetime DEFAULT NULL,
  `fare` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`flight_id`),
  UNIQUE KEY `flight_no` (`flight_no`),
  KEY `source_airport` (`source_airport`),
  KEY `destination_airport` (`destination_airport`),
  KEY `aircraft_id` (`aircraft_id`),
  CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`source_airport`) REFERENCES `airport` (`airport_id`),
  CONSTRAINT `flight_ibfk_2` FOREIGN KEY (`destination_airport`) REFERENCES `airport` (`airport_id`),
  CONSTRAINT `flight_ibfk_3` FOREIGN KEY (`aircraft_id`) REFERENCES `aircraft` (`aircraft_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flight`
--

LOCK TABLES `flight` WRITE;
/*!40000 ALTER TABLE `flight` DISABLE KEYS */;
INSERT INTO `flight` VALUES (301,'AI101',101,102,201,'2026-07-20 09:00:00','2026-07-20 11:00:00',5300.00),(302,'AI202',102,103,202,'2026-07-21 13:00:00','2026-07-21 15:30:00',6800.00),(303,'AI303',103,101,201,'2026-07-22 18:00:00','2026-07-22 20:00:00',6100.00),(701,'AI501',101,501,601,'2026-08-01 06:30:00','2026-08-01 08:20:00',5500.00),(702,'AI502',501,101,602,'2026-08-01 10:00:00','2026-08-01 12:00:00',6200.00),(703,'AI503',101,502,603,'2026-08-02 07:00:00','2026-08-02 09:00:00',5800.00),(704,'AI504',502,101,604,'2026-08-02 11:30:00','2026-08-02 13:30:00',6100.00),(705,'AI505',102,503,605,'2026-08-03 08:15:00','2026-08-03 10:30:00',6400.00),(706,'AI506',503,102,606,'2026-08-03 14:00:00','2026-08-03 16:15:00',6700.00),(707,'AI507',103,504,607,'2026-08-04 06:45:00','2026-08-04 08:30:00',5200.00),(708,'AI508',504,103,608,'2026-08-04 18:00:00','2026-08-04 20:00:00',5900.00),(709,'AI509',505,101,609,'2026-08-05 07:30:00','2026-08-05 09:00:00',4800.00),(710,'AI510',101,505,610,'2026-08-05 16:30:00','2026-08-05 18:00:00',5000.00),(711,'AI511',506,507,611,'2026-08-06 09:00:00','2026-08-06 10:30:00',4500.00),(712,'AI512',507,506,612,'2026-08-06 15:00:00','2026-08-06 16:30:00',4700.00),(713,'AI513',508,102,613,'2026-08-07 06:00:00','2026-08-07 08:00:00',5300.00),(714,'AI514',102,508,614,'2026-08-07 17:00:00','2026-08-07 19:00:00',5600.00),(715,'AI515',509,101,615,'2026-08-08 08:00:00','2026-08-08 10:00:00',5100.00),(716,'AI516',101,509,616,'2026-08-08 18:30:00','2026-08-08 20:30:00',5400.00),(717,'AI517',510,102,617,'2026-08-09 07:15:00','2026-08-09 09:45:00',6900.00),(718,'AI518',102,510,618,'2026-08-09 13:30:00','2026-08-09 16:00:00',7100.00),(719,'AI519',511,101,619,'2026-08-10 06:30:00','2026-08-10 09:00:00',7200.00),(720,'AI520',101,511,620,'2026-08-10 17:30:00','2026-08-10 20:00:00',7500.00);
/*!40000 ALTER TABLE `flight` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_before_insert_flight` BEFORE INSERT ON `flight` FOR EACH ROW BEGIN
    IF NEW.fare < 0 THEN
        SET NEW.fare = 0;
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_after_insert_flight` AFTER INSERT ON `flight` FOR EACH ROW BEGIN
    INSERT INTO Flight_Audit
    (flight_id, operation_type, message)
    VALUES
    (NEW.flight_id, 'AFTER INSERT', 'New flight inserted');
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_before_update_flight` BEFORE UPDATE ON `flight` FOR EACH ROW BEGIN
    IF NEW.fare < 0 THEN
        SET NEW.fare = 0;
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_after_update_flight` AFTER UPDATE ON `flight` FOR EACH ROW BEGIN
    INSERT INTO Flight_Audit
    (flight_id, operation_type, message)
    VALUES
    (NEW.flight_id, 'AFTER UPDATE', 'Flight details updated');
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_before_delete_flight` BEFORE DELETE ON `flight` FOR EACH ROW BEGIN
    INSERT INTO Flight_Audit
    (flight_id, operation_type, message)
    VALUES
    (OLD.flight_id, 'BEFORE DELETE', 'Flight is about to be deleted');
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_after_delete_flight` AFTER DELETE ON `flight` FOR EACH ROW BEGIN
    INSERT INTO Flight_Audit
    (flight_id, operation_type, message)
    VALUES
    (OLD.flight_id, 'AFTER DELETE', 'Flight deleted successfully');
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `flight_audit`
--

DROP TABLE IF EXISTS `flight_audit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flight_audit` (
  `audit_id` int NOT NULL AUTO_INCREMENT,
  `flight_id` int DEFAULT NULL,
  `operation_type` varchar(30) DEFAULT NULL,
  `message` varchar(255) DEFAULT NULL,
  `operation_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`audit_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flight_audit`
--

LOCK TABLES `flight_audit` WRITE;
/*!40000 ALTER TABLE `flight_audit` DISABLE KEYS */;
INSERT INTO `flight_audit` VALUES (1,301,'AFTER UPDATE','Flight details updated','2026-10-12 05:19:38');
/*!40000 ALTER TABLE `flight_audit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `flight_details_view`
--

DROP TABLE IF EXISTS `flight_details_view`;
/*!50001 DROP VIEW IF EXISTS `flight_details_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `flight_details_view` AS SELECT 
 1 AS `flight_id`,
 1 AS `flight_no`,
 1 AS `source_airport`,
 1 AS `fare`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `flight_view`
--

DROP TABLE IF EXISTS `flight_view`;
/*!50001 DROP VIEW IF EXISTS `flight_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `flight_view` AS SELECT 
 1 AS `flight_id`,
 1 AS `flight_no`,
 1 AS `fare`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `passenger`
--

DROP TABLE IF EXISTS `passenger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `passenger` (
  `passenger_id` int NOT NULL,
  `passenger_name` varchar(100) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `flight_id` int DEFAULT NULL,
  `age` int DEFAULT NULL,
  PRIMARY KEY (`passenger_id`),
  KEY `flight_id` (`flight_id`),
  CONSTRAINT `passenger_ibfk_1` FOREIGN KEY (`flight_id`) REFERENCES `flight` (`flight_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passenger`
--

LOCK TABLES `passenger` WRITE;
/*!40000 ALTER TABLE `passenger` DISABLE KEYS */;
INSERT INTO `passenger` VALUES (401,'Arya','9999999999',301,20),(402,'Rohan','9876543211',302,21),(403,'Priya','9876543212',303,22),(501,'Aarav Sharma','9876501001',301,24),(502,'Ananya Patil','9876501002',302,22),(503,'Rohan Deshmukh','9876501003',303,27),(504,'Isha Kulkarni','9876501004',701,21),(505,'Aditya Joshi','9876501005',702,29),(506,'Sneha More','9876501006',703,25),(507,'Kunal Shah','9876501007',704,31),(508,'Priya Nair','9876501008',705,26),(509,'Rahul Mehta','9876501009',706,34),(510,'Neha Singh','9876501010',707,23),(511,'Vivek Pawar','9876501011',708,30),(512,'Kavya Iyer','9876501012',709,28),(513,'Siddharth Rao','9876501013',710,35),(514,'Riya Gupta','9876501014',302,22),(515,'Akash Verma','9876501015',303,32),(516,'Tanvi Bhosale','9876501016',711,24),(517,'Manav Jain','9876501017',712,27),(518,'Pooja Shinde','9876501018',713,29),(519,'Harsh Vora','9876501019',714,33),(520,'Simran Kaur','9876501020',715,25),(521,'Nikhil Sane','9876501021',716,28),(522,'Meera Desai','9876501022',717,23),(523,'Arjun Malhotra','9876501023',718,36),(524,'Diya Kapoor','9876501024',719,21),(525,'Saurabh Mishra','9876501025',720,40),(526,'Aditi Chavan','9876501026',301,26),(527,'Yash Thakur','9876501027',302,24),(528,'Nandini Rao','9876501028',303,30),(529,'Varun Reddy','9876501029',701,37),(530,'Mitali Joshi','9876501030',702,25),(531,'Omkar Jadhav','9876501031',703,29),(532,'Shreya Patil','9876501032',704,22),(533,'Dev Mehta','9876501033',705,31),(534,'Anushka Roy','9876501034',706,27),(535,'Kartik Shetty','9876501035',707,35),(536,'Muskan Ali','9876501036',708,23),(537,'Aman Yadav','9876501037',709,28),(538,'Sakshi Pawar','9876501038',710,26),(539,'Raj Malhotra','9876501039',711,39),(540,'Pallavi Kulkarni','9876501040',712,32);
/*!40000 ALTER TABLE `passenger` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `payment_id` int NOT NULL,
  `booking_id` int DEFAULT NULL,
  `payment_date` date DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `payment_method` varchar(20) DEFAULT NULL,
  `payment_status` varchar(20) DEFAULT 'Paid',
  PRIMARY KEY (`payment_id`),
  KEY `booking_id` (`booking_id`),
  CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`booking_id`) REFERENCES `booking` (`booking_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES (901,801,'2026-07-10',5200.00,'UPI','Paid'),(902,802,'2026-07-11',6800.00,'Card','Paid'),(903,803,'2026-07-12',6100.00,'UPI','Paid'),(904,804,'2026-07-20',5500.00,'Card','Paid'),(905,805,'2026-07-20',6200.00,'UPI','Paid'),(906,806,'2026-07-21',5800.00,'NetBanking','Paid'),(907,807,'2026-07-21',6100.00,'Card','Paid'),(908,808,'2026-07-22',6400.00,'UPI','Paid'),(909,809,'2026-07-22',6700.00,'Card','Paid'),(910,810,'2026-07-23',5200.00,'UPI','Paid'),(911,811,'2026-07-23',5900.00,'Card','Paid'),(912,812,'2026-07-24',4800.00,'UPI','Paid'),(913,813,'2026-07-24',5000.00,'NetBanking','Paid'),(914,814,'2026-07-25',4500.00,'UPI','Paid'),(915,815,'2026-07-25',4700.00,'Card','Paid'),(916,816,'2026-07-26',5300.00,'UPI','Paid'),(917,817,'2026-07-26',5600.00,'Card','Paid'),(918,818,'2026-07-27',5100.00,'UPI','Paid'),(919,819,'2026-07-27',5400.00,'Card','Paid'),(920,820,'2026-07-28',6900.00,'UPI','Paid'),(921,821,'2026-07-28',7100.00,'Card','Paid'),(922,822,'2026-07-29',7200.00,'UPI','Paid'),(923,823,'2026-07-29',7500.00,'NetBanking','Paid'),(924,824,'2026-07-30',5200.00,'Card','Paid'),(925,825,'2026-07-30',6800.00,'UPI','Paid'),(926,826,'2026-07-31',6100.00,'Card','Paid'),(927,827,'2026-08-01',5500.00,'UPI','Paid'),(928,828,'2026-08-01',6200.00,'Card','Paid'),(929,829,'2026-08-02',5800.00,'UPI','Paid'),(930,830,'2026-08-02',6100.00,'NetBanking','Paid');
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Current Database: `AirportDB`
--

USE `AirportDB`;

--
-- Final view structure for view `flight_details_view`
--

/*!50001 DROP VIEW IF EXISTS `flight_details_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = cp850 */;
/*!50001 SET character_set_results     = cp850 */;
/*!50001 SET collation_connection      = cp850_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `flight_details_view` AS select `f`.`flight_id` AS `flight_id`,`f`.`flight_no` AS `flight_no`,`a`.`airport_name` AS `source_airport`,`f`.`fare` AS `fare` from (`flight` `f` join `airport` `a` on((`f`.`source_airport` = `a`.`airport_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `flight_view`
--

/*!50001 DROP VIEW IF EXISTS `flight_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = cp850 */;
/*!50001 SET character_set_results     = cp850 */;
/*!50001 SET collation_connection      = cp850_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `flight_view` AS select `flight`.`flight_id` AS `flight_id`,`flight`.`flight_no` AS `flight_no`,`flight`.`fare` AS `fare` from `flight` */;
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

-- Dump completed on 2026-10-23 19:35:55
