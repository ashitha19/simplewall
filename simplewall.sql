CREATE DATABASE  IF NOT EXISTS `simplewall` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `simplewall`;
-- MySQL dump 10.13  Distrib 5.7.23, for Win32 (AMD64)
--
-- Host: localhost    Database: simplewall
-- ------------------------------------------------------
-- Server version	5.7.23-log

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
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messages` (
  `msg_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_userid` int(11) NOT NULL,
  `sentto_userid` int(11) NOT NULL,
  `description` mediumtext,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`msg_id`),
  KEY `fk_messages_users` (`user_userid`),
  CONSTRAINT `fk_messages_users` FOREIGN KEY (`user_userid`) REFERENCES `users` (`userid`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (1,3,1,'Hi Yuga','2018-09-24 13:08:43'),(2,3,1,'Hi yuga!!','2018-09-24 13:17:58'),(4,2,3,'Hi Sita...','2018-09-24 13:26:42'),(7,3,1,'Hi Yuga...please delete this','2018-09-24 13:53:21'),(9,4,3,'HI Sita,\r\nHow did you do your exam?\r\n','2018-09-24 18:37:28'),(10,1,4,'Hi Asha, Did you complete you training?','2018-09-24 18:38:47');
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `userid` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(45) DEFAULT NULL,
  `last_name` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `password` varchar(145) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'YUGANDHAR','DAMA','yugandhardama@yahoo.com','$2b$12$ScpDarxYN3sYIzQdoH8bK.EKyQugk32Ebh/noR2IakMRRglxgVeLa','2018-09-24 12:32:44'),(2,'Rama','Sena','ram@yahoo.com','$2b$12$d5ujwSRjNxaNAD36z10di.CcQhtn9DubBAzj0OTBNF01k9Qx148c2','2018-09-24 12:33:09'),(3,'Sita','Rama','sita@yahoo.com','$2b$12$XDcmqhjrCHB7GevRXFUFMeIKZX6QAaIA5nL32HbCJCFD4BTm8IiPy','2018-09-24 12:36:08'),(4,'Asha','PBalaji','asha@yahoo.com','$2b$12$mriRSBLo3tn84f15IedJIemb7nsjTQp5ZKHmJ/RfUOQcbkptcZzxC','2018-09-24 18:36:31');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-09-27  9:49:00
