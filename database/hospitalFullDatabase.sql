-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: hospitalmanagement
-- ------------------------------------------------------
-- Server version	8.0.45

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
-- Table structure for table `appointment`
--

DROP TABLE IF EXISTS `appointment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointment` (
  `AppointmentID` int NOT NULL AUTO_INCREMENT,
  `DoctorID` varchar(10) NOT NULL,
  `PatientID` varchar(10) NOT NULL,
  `NurseID` varchar(10) DEFAULT NULL,
  `SlotID` int NOT NULL,
  `AppointmentStatus` enum('Upcoming','VitalsSaved','Completed','Missed') DEFAULT NULL,
  `Diagnosis` text,
  `Prescriptions` text,
  `Temperature` varchar(45) DEFAULT NULL,
  `BloodPressure` varchar(45) DEFAULT NULL,
  `HeartRate` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`AppointmentID`),
  KEY `DoctorID_idx` (`DoctorID`),
  KEY `PatientID_idx` (`PatientID`),
  KEY `NurseID_idx` (`NurseID`),
  KEY `SlotID_idx` (`SlotID`),
  CONSTRAINT `fk_appointment_slot` FOREIGN KEY (`SlotID`) REFERENCES `doctorslots` (`SlotID`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointment`
--

LOCK TABLES `appointment` WRITE;
/*!40000 ALTER TABLE `appointment` DISABLE KEYS */;
INSERT INTO `appointment` VALUES (1,'DOC01','PAT07','NUR03',506,'Completed','Common Cold','Paracetamol 500mg','99.7','120/80','75'),(2,'DOC01','PAT01','NUR02',505,'Completed','Diabetes Checkup','Metformin 500mg','99.2','130/85','73'),(3,'DOC01','PAT02','NUR10',508,'Completed','Early-stage Parkinson’s disease','Levodopa / Carbidopa (e.g., Sinemet)\n(25/100 mg – Three times daily)',NULL,NULL,NULL),(4,'DOC02','PAT06','NUR10',509,'Completed','Common Cold','Paracetamol 500mg','98.6','118/76','76'),(5,'DOC02','PAT08','NUR04',510,'Missed',NULL,NULL,'98','121/90','78'),(6,'DOC02','PAT09','NUR08',511,'Completed','Acute viral pharyngitis (likely viral upper respiratory infection)','Paracetamol 500mg, 1 tablet every 6 hours as needed for fever or pain',NULL,NULL,NULL),(7,'DOC02','PAT10','NUR05',513,'Completed','Mild hypertension with occasional palpitations','Amlodipine 5mg orally once \n(Engage in moderate exercise (e.g., 30 minutes brisk walk, 5 days/week))',NULL,NULL,NULL),(8,'DOC03','PAT03','NUR07',514,'Completed','Hypertension','Amlodipine 5mg OD','97.9','140/90','78'),(9,'DOC03','PAT05','NUR04',516,'Missed',NULL,NULL,'39','126/85','99'),(10,'DOC04','PAT04','NUR06',519,'Completed','Flu','Oseltamivir 75mg BID','99.1','118/76','80'),(27,'DOC05','PAT02','NUR10',524,'Missed',NULL,NULL,'99','120/85','82'),(28,'DOC06','PAT03','NUR03',531,'Missed',NULL,NULL,NULL,NULL,NULL),(29,'DOC01','PAT03','NUR05',664,'Missed',NULL,NULL,NULL,NULL,NULL),(30,'DOC03','PAT01','NUR02',518,'Missed',NULL,NULL,NULL,NULL,NULL),(31,'DOC01','PAT01','NUR07',655,'Missed',NULL,NULL,'38','120/85','180'),(32,'DOC01','PAT11','NUR01',677,'Missed',NULL,NULL,NULL,NULL,NULL),(33,'DOC02','PAT11','NUR01',685,'Upcoming',NULL,NULL,NULL,NULL,NULL),(36,'DOC03','PAT11','NUR09',693,'Upcoming',NULL,NULL,NULL,NULL,NULL),(37,'DOC01','PAT05','NUR01',678,'Upcoming',NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `appointment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctor`
--

DROP TABLE IF EXISTS `doctor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctor` (
  `DoctorID` varchar(10) NOT NULL,
  `Username` varchar(45) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `Name` varchar(45) NOT NULL,
  `Email` varchar(45) NOT NULL,
  `TelNo` varchar(45) DEFAULT NULL,
  `Department` varchar(45) NOT NULL,
  PRIMARY KEY (`DoctorID`),
  UNIQUE KEY `Email_UNIQUE` (`Email`),
  UNIQUE KEY `Username_UNIQUE` (`Username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor`
--

LOCK TABLES `doctor` WRITE;
/*!40000 ALTER TABLE `doctor` DISABLE KEYS */;
INSERT INTO `doctor` VALUES ('DOC01','james01','scrypt:32768:8:1$8CXgXYBAsBcp30qV$b2989686edaac5af529203fb6f16519a644ccf77d5cf5652e1579aaaf5fdd791eb632f04241e01273f2ae3d69015c010ebaff4c5ddafebf65b69623f64f1a434','James Holland','james@example.com','+447200189542','Neurology'),('DOC02','sarah02','scrypt:32768:8:1$TsTtm9XQOx6IZ7UH$f11b654680bd07acaa32afddbe017c169f8810a8cc6d411c0da6e1e390844737f74f1bf508f86f0c44eab802f066763cefaa3fbfc464515025da579fed1ed010','Sarah Williams','sarah@example.com','+47344002352','General Medicine'),('DOC03','daniel03','scrypt:32768:8:1$OqSLCH8mGmF27ZF8$6f97aec1051fa9106e5fe13f507717efa28a7ca455d33a22f38a4487c2905183b46937b141a2160e6ef5778e9fd41c7472cd1a94f230d5f39af5537d856982d7','Daniel Thompson','daniel@example.com','+47110394477','General Medicine'),('DOC04',NULL,NULL,'Emily Carter','emily@example.com',NULL,'Cardiology'),('DOC05','john05','scrypt:32768:8:1$Selzv2CWBfStYyEY$57e99572b6a1271fb5e8ba428527fac61a08c2769feefe741e63c809fe7d971258d81a7ef392daa72cbe2d61e5143b04c17cfa575d1bb39d1c50f97194ec5b2d','John Smith','john@example.com','+47312903488','Neurology'),('DOC06',NULL,NULL,'Michael Brown','michael@example.com',NULL,'Cardiology'),('DOC07',NULL,NULL,'Laura Green','laura@example.com',NULL,'Orthopaedics'),('DOC08',NULL,NULL,'David Taylor','david@example.com',NULL,'General Medicine'),('DOC09',NULL,NULL,'Chloe Martin','chloe@example.com',NULL,'Orthopaedics'),('DOC10',NULL,NULL,'Noah Harris','noah@example.com',NULL,'Cardiology');
/*!40000 ALTER TABLE `doctor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctorslots`
--

DROP TABLE IF EXISTS `doctorslots`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctorslots` (
  `SlotID` int NOT NULL AUTO_INCREMENT,
  `DoctorID` varchar(10) NOT NULL,
  `Date` date NOT NULL,
  `Time` time NOT NULL,
  `IsBooked` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`SlotID`),
  UNIQUE KEY `unique_doctor_slot` (`DoctorID`,`Date`,`Time`),
  KEY `DoctorID_idx` (`DoctorID`),
  CONSTRAINT `DoctorID` FOREIGN KEY (`DoctorID`) REFERENCES `doctor` (`DoctorID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=697 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctorslots`
--

LOCK TABLES `doctorslots` WRITE;
/*!40000 ALTER TABLE `doctorslots` DISABLE KEYS */;
INSERT INTO `doctorslots` VALUES (504,'DOC01','2026-02-10','09:30:00',1),(505,'DOC01','2026-02-10','11:00:00',1),(506,'DOC01','2026-02-10','11:30:00',1),(507,'DOC01','2026-02-11','13:00:00',1),(508,'DOC01','2026-02-11','14:30:00',1),(509,'DOC02','2026-02-10','10:00:00',1),(510,'DOC02','2026-02-11','10:00:00',1),(511,'DOC02','2026-02-11','11:30:00',1),(512,'DOC02','2026-02-11','13:00:00',0),(513,'DOC02','2026-02-11','14:00:00',1),(514,'DOC03','2026-02-10','09:30:00',1),(515,'DOC03','2026-02-10','13:00:00',0),(516,'DOC03','2026-02-11','11:30:00',1),(517,'DOC03','2026-02-12','13:00:00',0),(518,'DOC03','2026-02-12','13:30:00',1),(519,'DOC04','2026-02-10','10:30:00',1),(520,'DOC04','2026-02-11','11:00:00',1),(521,'DOC04','2026-02-11','11:30:00',1),(522,'DOC04','2026-02-12','15:00:00',0),(523,'DOC04','2026-02-12','15:30:00',1),(524,'DOC05','2026-02-11','09:30:00',1),(525,'DOC05','2026-02-11','14:00:00',0),(526,'DOC05','2026-02-12','15:30:00',1),(527,'DOC05','2026-02-12','16:00:00',0),(528,'DOC05','2026-02-13','10:30:00',1),(529,'DOC06','2026-02-10','15:30:00',1),(530,'DOC06','2026-02-11','13:00:00',1),(531,'DOC06','2026-02-12','10:00:00',1),(532,'DOC06','2026-02-13','15:00:00',0),(533,'DOC06','2026-02-13','16:30:00',1),(534,'DOC07','2026-02-10','16:00:00',1),(535,'DOC07','2026-02-12','15:00:00',1),(536,'DOC07','2026-02-13','10:30:00',1),(537,'DOC07','2026-02-13','13:00:00',0),(538,'DOC07','2026-02-13','15:30:00',1),(539,'DOC08','2026-02-10','09:30:00',1),(540,'DOC08','2026-02-10','13:00:00',0),(541,'DOC08','2026-02-10','16:30:00',0),(542,'DOC08','2026-02-11','14:00:00',0),(543,'DOC08','2026-02-11','14:30:00',1),(544,'DOC09','2026-02-12','11:30:00',0),(545,'DOC09','2026-02-12','15:00:00',0),(546,'DOC09','2026-02-13','11:00:00',1),(547,'DOC09','2026-02-14','10:00:00',0),(548,'DOC09','2026-02-14','09:30:00',1),(549,'DOC10','2026-02-10','16:00:00',0),(550,'DOC10','2026-02-12','10:00:00',1),(551,'DOC10','2026-02-13','13:30:00',1),(552,'DOC10','2026-02-13','14:00:00',0),(553,'DOC10','2026-02-14','15:30:00',0),(655,'DOC01','2026-02-24','16:30:00',1),(656,'DOC01','2026-04-08','09:10:00',0),(657,'DOC01','2026-02-20','13:30:00',1),(658,'DOC01','2026-02-18','14:00:00',1),(659,'DOC01','2026-02-19','15:00:00',1),(661,'DOC01','2026-02-17','13:00:00',1),(662,'DOC01','2026-02-24','16:00:00',1),(663,'DOC01','2026-02-18','16:30:00',1),(664,'DOC01','2026-02-26','10:30:00',1),(665,'DOC02','2026-03-12','14:00:00',0),(666,'DOC02','2026-03-12','17:00:00',0),(667,'DOC02','2026-03-19','13:00:00',0),(668,'DOC02','2026-03-06','16:00:00',0),(669,'DOC02','2026-03-19','16:00:00',0),(675,'DOC01','2026-04-05','15:30:00',0),(677,'DOC01','2026-04-23','10:00:00',1),(678,'DOC01','2026-06-30','14:00:00',1),(680,'DOC01','2026-06-30','10:30:00',0),(681,'DOC02','2026-05-15','13:30:00',0),(682,'DOC02','2026-06-24','16:00:00',0),(684,'DOC02','2026-05-28','10:30:00',0),(685,'DOC02','2026-05-15','08:30:00',1),(687,'DOC03','2026-06-03','17:00:00',0),(693,'DOC03','2026-06-30','10:30:00',1),(694,'DOC03','2026-05-20','16:30:00',0),(695,'DOC03','2026-05-20','11:00:00',0);
/*!40000 ALTER TABLE `doctorslots` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nurse`
--

DROP TABLE IF EXISTS `nurse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nurse` (
  `NurseID` varchar(10) NOT NULL,
  `Username` varchar(45) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `Name` varchar(45) NOT NULL,
  `Email` varchar(45) NOT NULL,
  `TelNo` varchar(45) DEFAULT NULL,
  `Ward` varchar(45) NOT NULL,
  PRIMARY KEY (`NurseID`),
  UNIQUE KEY `Email_UNIQUE` (`Email`),
  UNIQUE KEY `Username_UNIQUE` (`Username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nurse`
--

LOCK TABLES `nurse` WRITE;
/*!40000 ALTER TABLE `nurse` DISABLE KEYS */;
INSERT INTO `nurse` VALUES ('NUR01',NULL,NULL,'Sam Miller','sam@example.com',NULL,'A'),('NUR02',NULL,NULL,'Emma Sterling','emma@example.com',NULL,'B'),('NUR03',NULL,NULL,'Alice Kennedy','alice@example.com',NULL,'C'),('NUR04','grace04','scrypt:32768:8:1$xZgQnf0JyCLP6r42$a070831a992d579c0e3789670f73b6aea2d1db0da1d419d1dd2c19a65ff14fb4c8ee4e2b035edf07155b30ec9037174e7a6c19ba7af86b40b719de967f7e08f6','Grace Morgan','grace@example.com','07712900120','B'),('NUR05',NULL,NULL,'David Jackson','davidj@example.com',NULL,'D'),('NUR06',NULL,NULL,'Alice Bennett','bennett@example.com',NULL,'D'),('NUR07','jessica07','scrypt:32768:8:1$nupoR0YT1IKr71ba$d7c93b469530a79465239ee83762f01bf195b121333cc0a67907cc5d14cbc54570fc40e62f128ddcaa46d6e1f614d77d0b46196c9d8176da1f0f674a043e1b67','Jessica Moore','jessica@example.com','07224466889','C'),('NUR08',NULL,NULL,'James Carter','jcarter@example.com',NULL,'A'),('NUR09',NULL,NULL,'Aisha Khan','aisha@example.com',NULL,'A'),('NUR10',NULL,NULL,'Hannah Wilson','hannah@example.com',NULL,'B');
/*!40000 ALTER TABLE `nurse` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient` (
  `PatientID` varchar(10) NOT NULL,
  `Username` varchar(45) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Name` varchar(45) NOT NULL,
  `Email` varchar(45) NOT NULL,
  `TelNo` varchar(45) NOT NULL,
  PRIMARY KEY (`PatientID`),
  UNIQUE KEY `Username_UNIQUE` (`Username`),
  UNIQUE KEY `Email_UNIQUE` (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient`
--

LOCK TABLES `patient` WRITE;
/*!40000 ALTER TABLE `patient` DISABLE KEYS */;
INSERT INTO `patient` VALUES ('PAT01','PAT01','scrypt:32768:8:1$EPrzjrqZmb4dCEg7$77809e47e037cbf7e64d8319da731a5155bc8d5285ab618fddfbb63fc2a1813da44f72d6eb6c270d3c33cc59bec735a2340cee725636aa19a3f238b5699ee9f1','Ahmed Ali','ahmed@example.com','+447100233493'),('PAT02','PAT02','scrypt:32768:8:1$IqKALqQVuojJOm62$f624a4234eb8055be05b77827f9301d3e8628ab04fb9d0bc60db1e0228dc29540eacc696f6745c112c288b33c764bd43e602d4de20608e7d4eea30e44de6fe09','Luke Walker','luke@example.com','+447213388453'),('PAT03','PAT03','scrypt:32768:8:1$zmjZC3BCUNhzI8BI$e74e4f5587657b28de773bd27ce543ec42d67b99c1afa1a466e0d6d196e72ff62e1e2c00c2f072d4700833e11db936042510dd34ba254076b99453602aa04a05','Sarah Collins','sCollins@example.com','+447389442713'),('PAT04','PAT04','scrypt:32768:8:1$EiS9JpVxwslxLL6q$94f76c417b4b10a3f359094c9f879d4b869fd46c562fbff951dfdacccf3d7e19468760e12ec1acd6512f954e033789e5b30c9d6baec9c0b8cfb1b51e228ad1e2','Olivia Brown','olivia@example.com','+447120047329'),('PAT05','PAT05','scrypt:32768:8:1$HewA5lebySr0HGUz$66c18c5254e40162b6118725003d57bafc475bedfdc58732dbe046f09071e841a03538cf61a9dd3556be46a2e2ea17ba6ceb32c8fd17b69f8458e822ea6d85b5','Liam Johnson','liam@example.com','+447038233749'),('PAT06','PAT06','scrypt:32768:8:1$hM0i7nyKYNX02Gv5$77bea21ad76dc0c04a73549832463e833d16e53706b0c85d90a225ffc17969547a28c8dc807869a95f0c23b612f8d50155242c94a5878e0b671f5dfc97457c99','Emma Thompson','ethompson@example.com','+447350649332'),('PAT07','PAT07','scrypt:32768:8:1$HACqh9JhVPNHpkXP$852eb64db6eda06c4c217251f8e15c3762a6c3f8c7c2c657822357dbe2172c8a5d5ab63ce1ca95a9a1e48d18aa6c4bd41a601236e850cab75fc6c9444be9cfdc','Chloe Wilson','cwilson@example.com','+4471298348756'),('PAT08','PAT08','scrypt:32768:8:1$VKkMmUWgcYLFjRZE$046177d211f42e58b6a758de1bcf356dce55e5239b16ade20ade0b784ac01d072435c52f1ffb80ccafcaecc08dd65e2b397525e4be08b9fed9b7ab00d494a683','Mohammed Rahman','mohammed@example.com','+447203992128'),('PAT09','PAT09','scrypt:32768:8:1$uYvXVKHOEYbRUT3k$92b9a70ce5cfb80047dddd93b8d28cab6b1100b0ab8654c8a9a4c97aee643d8f73c64b17baaef543cc7c93d3b210de1b1bc9761f2a84d1d1d5e422a7457b8b5f','Robert Taylor','robert@example.com','+447034885239'),('PAT10','PAT10','scrypt:32768:8:1$wvZa9jDSVwqeoDQQ$076d492e8700660f81c28414cfa0f56d73ee916a8f02ef4c648675e3e0ff920a9fe9c69fcf803a57b375e58e78e0a96d189dd45e21dff526de47f3fb5dfa55c9','John Williams','jwilliams@example.com','+447650112938'),('PAT11','PAT11','scrypt:32768:8:1$xjH6fCSqNzAZ993w$a6eb6543cafa324e0aa9ce0be7c78ded112a5e69e10effd31fe2d2ac9c963d8dbffff7fc19e9f709ab804db5339a3c074669d1e4822e53923cad1c44cfcaec61','Hay Thar','haythar@gmail.com','+447112233441');
/*!40000 ALTER TABLE `patient` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-29 19:50:18
