-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: localhost    Database: rbi_04_03
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `z_user`
--

DROP TABLE IF EXISTS `z_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `z_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(60) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `email_service` varchar(100) DEFAULT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `adress` varchar(200) DEFAULT NULL,
  `username` varchar(40) DEFAULT NULL,
  `password` varchar(40) DEFAULT NULL,
  `other_info` int DEFAULT NULL,
  `kind` varchar(20) DEFAULT NULL,
  `date_joined` datetime DEFAULT NULL,
  `active` tinyint(1) DEFAULT '0',
  `active_notification` tinyint(1) DEFAULT '0',
  `reject` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `z_user`
--

LOCK TABLES `z_user` WRITE;
/*!40000 ALTER TABLE `z_user` DISABLE KEYS */;
INSERT INTO `z_user` VALUES (1,'Nguyễn Thị Hải','hainguyenthi@gmail.com','nguyenthihai@cortekrbi.com','0433133133','Số 1 Đại Cổ Việt, Hai Bà Trưng, Hà Nội ','user5','pass5',NULL,'factory',NULL,1,0,0),(2,'Vũ Trọng Tới','toivutrong@gmail.com',NULL,'0901020304','Yen Bai','user2','pass2',NULL,'citizen',NULL,1,0,0),(3,'Lương Cương','luongvancuongkmhd1998@gmail.com','luongvancuongkmhd1998@cortekrbi.com','01223344551','Ha Noi ','user3','pass3',NULL,'manager',NULL,1,0,0),(4,'Nguyễn Vũ Đạt','luongvancuongkmhd1998@gmail.com','nguyenvudat1998@cortekrbi.com','0335025559','Số 245 Định Công, Hoàng Mai, Hà Nội ','user4','pass4',NULL,'factory',NULL,1,1,0),(32,'Phạm Thị Chiến','chienphamthi@gmail.com','luongvancuongkmhd1998@cortekrbi.com','0962199197','Số 24, Giai Phóng, Hai Bà Trưng,','user7','pass7',NULL,'factory','2018-08-30 14:10:36',1,0,0),(34,'Luong Van Cuong','luongvancuongkmhd1998@gmail.com','luongvancuongkmhd1998@cortekrbi.com','0337374949','So 288 Giai Phong','user1','pass1',NULL,'factory','2020-04-14 09:30:14',1,0,0),(35,'user0','luongvancuongkmhd1998@gmail.com',NULL,'0337374949','số 28 ,ngõ 41 tương mai, hoàng mai','TEST SAMPLE','testsample',NULL,'factory','2020-10-31 09:11:38',1,0,0),(37,'Amin','luongvancuongkmhd1998@gmail.com',NULL,'0337374949','Ha Noi','admin','admin',NULL,'admin','2020-12-24 07:20:45',1,0,0),(38,'Duc','nguyendangchungduc1999@gmail.com',NULL,'','','duc nguyen','Chungduc99@.com',NULL,'factory','2020-12-29 07:31:11',1,0,0),(39,'tung','phantungbk62@gmail.com',NULL,'0123456789','hanoi','phantung','0123456789',NULL,'factory','2021-01-27 21:39:48',1,0,0),(40,'Nguyễn Đình Tuấn','tuanabcxyz555@gmail.com',NULL,'0966590636','Long Biên, Hà Nội','user2000','00000000',NULL,'factory','2021-01-30 13:56:53',1,0,0),(50,'Anh Tuan Long Bien','tuanlongbien002@gmail.com',NULL,'0966590636','123123123','TuanLongBien2','Tuan1234',NULL,'factory','2021-04-07 09:50:48',0,0,0),(51,'Anh Tuan Long Bien','tuanlongbien001@gmail.com',NULL,'0966590636','123123123','TuanLongBien1','Tuan1234',NULL,'factory','2021-04-07 09:50:48',0,0,0),(52,'Anh Tuan Long Bien','tuanlongbien003@gmail.com',NULL,'0966590636','123123123','TuanLongBien3','Tuan1234',NULL,'factory','2021-04-07 09:50:48',0,0,0),(53,'Anh Tuan Long Bien','tuanlongbien004@gmail.com',NULL,'0966590636','123123123','TuanLongBien4','Tuan1234',NULL,'factory','2021-04-07 09:50:48',0,0,0),(54,'121212 1212','123123123@12',NULL,'0977678767','123123123','Tuanf1234','Tuan1234',NULL,'factory','2021-04-07 15:45:03',0,0,0);
/*!40000 ALTER TABLE `z_user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-04-07 17:32:15
