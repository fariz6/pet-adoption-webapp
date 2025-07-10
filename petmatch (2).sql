-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 01, 2025 at 07:36 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `petmatch`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `PASSWORD` varchar(40) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `admin_info`
--

CREATE TABLE `admin_info` (
  `admin_id` int(11) NOT NULL,
  `email` varchar(60) DEFAULT NULL,
  `pass` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin_info`
--

INSERT INTO `admin_info` (`admin_id`, `email`, `pass`) VALUES
(1, 'admin123', 'Fariz@2003');

-- --------------------------------------------------------

--
-- Table structure for table `adoption_app`
--

CREATE TABLE `adoption_app` (
  `adoptionid` int(10) NOT NULL,
  `petname` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `mob` bigint(10) NOT NULL,
  `address` varchar(50) NOT NULL,
  `city` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  `pin` int(6) NOT NULL,
  `housing` varchar(50) NOT NULL,
  `ownership` varchar(50) NOT NULL,
  `yard` varchar(20) NOT NULL,
  `household` varchar(50) NOT NULL,
  `owned` varchar(10) NOT NULL,
  `aboutprepet` varchar(500) NOT NULL,
  `dailyroutine` varchar(500) NOT NULL,
  `whyadopt` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `bookingid` int(11) NOT NULL,
  `id` int(10) NOT NULL,
  `name` varchar(30) NOT NULL,
  `mobno` bigint(10) NOT NULL,
  `email` varchar(50) NOT NULL,
  `product_id` int(10) NOT NULL,
  `sheltername` varchar(50) NOT NULL,
  `animalname` varchar(50) NOT NULL,
  `species` varchar(50) NOT NULL,
  `breed` varchar(50) NOT NULL,
  `animalprof` varchar(100) NOT NULL,
  `status` varchar(50) NOT NULL DEFAULT 'adopted',
  `day` date DEFAULT NULL,
  `bookingdate` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`bookingid`, `id`, `name`, `mobno`, `email`, `product_id`, `sheltername`, `animalname`, `species`, `breed`, `animalprof`, `status`, `day`, `bookingdate`) VALUES
(47, 20, '', 0, '', 33, '', 'Mike', 'Dog', 'Lab', '1746100016_labrodar.jpg', 'accepted', '2025-05-07', '2025-05-02 01:53:16'),
(50, 15, '', 0, '', 34, '', 'Groot', 'Dog', 'German shepard', '1746151765_shepard.jpg', 'rejected', '2025-07-29', '2025-05-04 08:48:33'),
(51, 15, '', 0, '', 32, '', 'jessie', 'Dog', 'husky', 'huskye.jpg', 'adopted', '2025-09-06', '2025-05-04 08:24:44'),
(52, 15, '', 0, '', 12, '', 'jack', 'cat', 'persian', 'cat.jpeg', 'rejected', '2025-09-06', '2025-05-04 08:28:13'),
(54, 15, '', 0, '', 34, '', 'Groot', 'Dog', 'German shepard', '1746151765_shepard.jpg', 'accepted', '2025-06-26', '2025-05-04 09:00:48'),
(55, 15, '', 0, '', 37, '', 'micky', 'Cat', 'persian', '1746521875_persian.jpg', 'cancelled', '2025-06-05', '2025-06-05 05:15:05'),
(56, 15, '', 0, '', 36, '', 'goldy', 'Rabbit', 'Netherland Dwarf', '1746521734_dwarf.jpg', 'cancelled', '2025-09-09', '2025-06-05 05:14:19'),
(57, 15, '', 0, '', 36, '', 'goldy', 'Rabbit', 'Netherland Dwarf', '1746521734_dwarf.jpg', 'adopted', '2025-06-25', '2025-05-06 10:18:17');

-- --------------------------------------------------------

--
-- Table structure for table `carebookings`
--

CREATE TABLE `carebookings` (
  `carebookingid` int(10) NOT NULL,
  `id` int(10) NOT NULL,
  `centerid` int(10) NOT NULL,
  `centername` varchar(50) NOT NULL,
  `caretype` varchar(50) NOT NULL,
  `species` varchar(50) NOT NULL,
  `breed` varchar(50) NOT NULL,
  `prof` varchar(50) NOT NULL,
  `location` varchar(50) NOT NULL,
  `notes` varchar(50) NOT NULL,
  `date` date NOT NULL,
  `userid` int(10) NOT NULL,
  `status` varchar(50) NOT NULL DEFAULT 'requested',
  `bookingdate` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `carebookings`
--

INSERT INTO `carebookings` (`carebookingid`, `id`, `centerid`, `centername`, `caretype`, `species`, `breed`, `prof`, `location`, `notes`, `date`, `userid`, `status`, `bookingdate`) VALUES
(38, 0, 4, 'Goodpet', 'Boarding', 'cat', 'Siamese', 'Best trainin center for ur pet', '5,alagasen', 'hgjhk', '2025-06-06', 15, 'paid', '2025-05-02 06:26:14'),
(39, 0, 8, 'Pets Grooming', 'Pet Grooming', 'dog', 'German Shepherd', '', 'sai baba colony', '', '2025-05-03', 20, 'paid', '2025-05-02 09:04:40'),
(40, 0, 10, 'Jamescare', 'Basic Commands Training', 'dog', 'Golden Retriever', 'jasperd2003@gmail.com', 'James', 'rdsfghvjbn', '2025-06-06', 15, 'paid', '2025-05-02 11:45:09'),
(41, 0, 10, 'Jamescare', 'Training', 'cat', 'Siamese', 'jasperd2003@gmail.com', 'James', 'dcfgvhbjn', '2025-06-06', 15, 'requested', '2025-05-03 07:00:15'),
(42, 0, 11, 'Richcare pet', 'Vaccination', 'dog', 'Bulldog', 'abdullahfariz613@gmail.com', 'Richard', 'estdfghjbknlm', '2025-05-23', 15, 'requested', '2025-05-06 09:20:07'),
(43, 0, 11, 'Richcare pet', 'Dental Care', 'cat', 'Abyssinian', 'abdullahfariz613@gmail.com', 'Richard', 'fdgfchgv', '2025-08-09', 15, 'approved', '2025-05-06 09:22:03'),
(44, 0, 11, 'Richcare pet', 'Behavior Consultation', 'dog', 'Labrador Retriever', 'abdullahfariz613@gmail.com', 'Richard', 'dfxfgcghvjbk', '2025-05-09', 15, 'rejected', '2025-05-06 09:24:45'),
(45, 0, 10, 'Jamescare', 'Basic Commands Training', 'cat', 'Bengal', 'jasperd2003@gmail.com', 'James', 'sdzfxgchjb', '2025-07-07', 15, 'rejected', '2025-05-06 09:27:19');

-- --------------------------------------------------------

--
-- Table structure for table `careresource_info`
--

CREATE TABLE `careresource_info` (
  `careid` int(10) NOT NULL,
  `centerid` int(10) NOT NULL,
  `centername` varchar(50) NOT NULL,
  `centertype` varchar(50) NOT NULL,
  `resourcername` varchar(30) NOT NULL,
  `address` varchar(50) NOT NULL,
  `city` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  `pin` int(6) NOT NULL,
  `mob` bigint(10) NOT NULL,
  `mail` varchar(50) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `description` varchar(500) NOT NULL,
  `Image` varchar(50) NOT NULL,
  `centerpic` varchar(100) NOT NULL,
  `idproof` varchar(100) NOT NULL,
  `license` varchar(100) NOT NULL,
  `price` int(10) NOT NULL,
  `status` varchar(10) NOT NULL DEFAULT 'pending',
  `registeredtime` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `careresource_info`
--

INSERT INTO `careresource_info` (`careid`, `centerid`, `centername`, `centertype`, `resourcername`, `address`, `city`, `state`, `pin`, `mob`, `mail`, `pass`, `description`, `Image`, `centerpic`, `idproof`, `license`, `price`, `status`, `registeredtime`) VALUES
(10, 0, 'Jamescare', 'Training Center', 'James', 'sai baba colony', 'Coimbatore', 'Tamil Nadu', 641011, 9345834365, 'jasperd2003@gmail.com', 'a3jhL0Ra', 'Pawfect Companions is a premier pet training center dedicated to helping pets and their owners build strong, lasting bonds through effective training and positive reinforcement. Located in a spacious, pet-friendly environment, we specialize in obedience training, behavioral correction, socialization, and specialty classes for dogs of all breeds, sizes, and ages.', 'prof.jpg', 'centerpic.jpg', 'idproof.png', 'idproof.png', 0, 'approved', '2025-05-06 05:56:45'),
(11, 0, 'Richcare pet', 'Veterinarian', 'Richard', '88,sai baba colony', 'Coimbatore', 'Tamil Nadu', 641011, 9345834365, 'abdullahfariz613@gmail.com', 'OQaO291g', 'A veterinary center is a specialized facility providing medical care, treatment, and preventive services for animals. Staffed by skilled veterinarians and technicians, it offers diagnostics, surgery, vaccinations, and wellness care. Focused on animal health and well-being, it ensures pets and livestock receive compassionate, expert attention to lead healthier, happier lives.', 'prof.jpg', 'germanshepard1.jpg', 'idproof.png', 'idproof.png', 0, 'pending', '2025-06-05 03:43:54'),
(12, 0, 'BeautyPetspa', 'Pet Groomer', 'Jasper', 'sai baba colony', 'Coimbatore', 'Tamil Nadu', 641011, 9345834365, 'jasperdevaraj@gmail.com', 'cmKdpOTm', 'A pet spa center offers grooming, relaxation, and wellness services for pets in a calm, hygienic environment. Trained professionals provide baths, haircuts, nail trimming, massages, and skin treatments. Focused on comfort and care, the spa enhances pets’ appearance, hygiene, and well-being, making them feel refreshed, healthy, and pampered.', 'jasper.jpg', 'petspa.jpg', 'idproof.png', 'idproof.png', 0, 'approved', '2025-06-04 17:20:24'),
(13, 0, 'Jamescare', 'Pet Groomer', 'James', 'sai baba colony', 'Madurai', 'Tamil Nadu', 641011, 9345834365, 'abdfarizharis2541@gmail.com', '', 'aewsrdtgfhbjknlm,', 'prof.jpg', 'cat2.jpg', 'idproof.png', 'idproof.png', 0, 'rejected', '2025-05-06 09:35:15');

-- --------------------------------------------------------

--
-- Table structure for table `care_reg`
--

CREATE TABLE `care_reg` (
  `centreid` int(11) NOT NULL,
  `careresourcerid` int(11) NOT NULL,
  `careresourcertype` varchar(50) DEFAULT NULL,
  `careresourcername` varchar(50) DEFAULT NULL,
  `careresourcetype` varchar(50) DEFAULT NULL,
  `carecentrename` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `mobile` bigint(20) DEFAULT NULL,
  `street` varchar(70) DEFAULT NULL,
  `pincode` int(6) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `Profile` varchar(100) NOT NULL,
  `thumbnail` varchar(100) NOT NULL,
  `idproof` varchar(100) NOT NULL,
  `status` varchar(20) NOT NULL DEFAULT 'pending',
  `registeredtime` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `care_reg`
--

INSERT INTO `care_reg` (`centreid`, `careresourcerid`, `careresourcertype`, `careresourcername`, `careresourcetype`, `carecentrename`, `email`, `password`, `mobile`, `street`, `pincode`, `state`, `city`, `Profile`, `thumbnail`, `idproof`, `status`, `registeredtime`) VALUES
(8, 0, 'Veterinarian', 'Jasper D', NULL, 'Onecare', 'jasperdevaraj@gmail.com', 'Jasper123@', 8903115145, '5,alagasen street', 628620, 'Tamil Nadu', 'Coimbatore', 'jasper.jpg', 'jasper.jpg', 'jd.jpg', 'approved', '2025-05-02 01:53:51'),
(10, 0, 'Pet Trainer', 'Harry', NULL, 'Harry Pet Training Center', 'abdullahfariz613@gmail.com', 'lmxClcCt', 6756453434, 'sai baba colony', 675678, 'Tamil Nadu', 'Coimbatore', 'prof.jpg', 'idproof.png', 'idproof.png', 'approved', '2025-05-02 01:53:51'),
(11, 0, 'Veterinarian', 'James', NULL, 'Jamescare', 'rashath2003@gmail.com', NULL, 9345834365, '88,sai baba colony', 641011, 'Tamil Nadu', 'Coimbatore', 'rasa.jpg', 'download (1).jpeg', 'idproof.png', 'pending', '2025-05-02 04:44:46'),
(12, 0, 'Pet Groomer', 'Richard', NULL, 'Richard Pets Grooming', 'abdullahfariz613@gmail.com', 'LWtsq9LF', 8765454545, 'sai baba colony', 654545, 'Tamil Nadu', 'Coimbatore', 'prof.jpg', 'petspa.jpg', 'idproof.png', 'approved', '2025-05-02 08:46:03');

-- --------------------------------------------------------

--
-- Table structure for table `cpass`
--

CREATE TABLE `cpass` (
  `passid` int(11) NOT NULL,
  `careid` int(10) NOT NULL,
  `email` varchar(100) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cpass`
--

INSERT INTO `cpass` (`passid`, `careid`, `email`, `timestamp`, `status`) VALUES
(1, 10, 'jasperd2003@gmail.com', '2025-05-06 01:06:02', 'sended'),
(2, 10, 'jasperd2003@gmail.com', '2025-05-06 05:56:45', 'sended'),
(3, 11, 'abdullahfariz613@gmail.com', '2025-05-06 09:34:34', 'pending');

-- --------------------------------------------------------

--
-- Table structure for table `pass`
--

CREATE TABLE `pass` (
  `passid` int(11) NOT NULL,
  `shelter_id` int(10) NOT NULL,
  `email` varchar(100) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pass`
--

INSERT INTO `pass` (`passid`, `shelter_id`, `email`, `timestamp`, `status`) VALUES
(1, 21, 'abdullahfariz613@gmail.com', '2025-05-06 01:00:44', 'pending');

-- --------------------------------------------------------

--
-- Table structure for table `payment`
--

CREATE TABLE `payment` (
  `payid` int(11) NOT NULL,
  `service` varchar(100) NOT NULL,
  `serviceprice` longtext NOT NULL,
  `serviceid` varchar(1000) NOT NULL,
  `careid` int(10) NOT NULL,
  `userid` int(10) NOT NULL,
  `paytime` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `paymethod` varchar(50) NOT NULL,
  `transid` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `payment`
--

INSERT INTO `payment` (`payid`, `service`, `serviceprice`, `serviceid`, `careid`, `userid`, `paytime`, `paymethod`, `transid`) VALUES
(21, 'Boarding', '2500.00', '21', 4, 15, '2025-05-02 05:22:26', '', ''),
(30, 'Dental Care', '20.00', '28', 1, 14, '2025-05-02 05:22:26', '', ''),
(35, 'Training', '2500.0', '30', 4, 14, '2025-05-02 05:22:26', '', ''),
(36, 'Boarding', '2500.0', '31', 4, 14, '2025-05-02 05:22:26', '', ''),
(37, 'Behavior Consultation', '30.0', '32', 1, 14, '2025-05-02 05:22:26', '', ''),
(38, 'Socialization Session', '4500.0', '33', 7, 15, '2025-05-02 05:22:26', '', ''),
(39, 'Behavior Consultation', '30.0', '35', 1, 15, '2025-05-02 05:22:26', '', ''),
(40, 'Socialization Session', '4500.0', '34', 7, 15, '2025-05-02 05:44:41', 'upi', 'abd@icci'),
(41, 'Behavior Consultation', '3500.0', '36', 4, 15, '2025-05-02 05:59:29', 'cash', 'CASH_36_1746165569'),
(42, 'Socialization Session', '4500.0', '37', 7, 15, '2025-05-02 06:05:40', 'upi', 'abd@icci'),
(43, 'Boarding', '2500.0', '38', 4, 15, '2025-05-02 06:26:14', 'cash', 'CASH_38_1746167174'),
(44, 'Pet Grooming', '300.0', '39', 8, 20, '2025-05-02 09:04:40', 'upi', 'abd@icci'),
(45, 'Basic Commands Training', '2000.0', '40', 10, 15, '2025-05-02 11:45:09', 'upi', 'abd@icci');

-- --------------------------------------------------------

--
-- Table structure for table `product_info`
--

CREATE TABLE `product_info` (
  `product_id` int(11) NOT NULL,
  `shelter_id` int(11) NOT NULL,
  `Ownername` varchar(30) DEFAULT NULL,
  `Sheltername` varchar(30) DEFAULT NULL,
  `Email` varchar(30) DEFAULT NULL,
  `Petname` varchar(20) DEFAULT NULL,
  `Species` varchar(30) DEFAULT NULL,
  `Breed` varchar(30) DEFAULT NULL,
  `gender` varchar(20) NOT NULL,
  `location` varchar(30) DEFAULT NULL,
  `Age` varchar(30) DEFAULT NULL,
  `description` varchar(100) NOT NULL,
  `Animalimg` varchar(30) NOT NULL,
  `Animalimg2` varchar(50) NOT NULL,
  `Animalimg3` varchar(50) NOT NULL,
  `Status` varchar(20) NOT NULL DEFAULT 'available',
  `registeredtime` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product_info`
--

INSERT INTO `product_info` (`product_id`, `shelter_id`, `Ownername`, `Sheltername`, `Email`, `Petname`, `Species`, `Breed`, `gender`, `location`, `Age`, `description`, `Animalimg`, `Animalimg2`, `Animalimg3`, `Status`, `registeredtime`) VALUES
(33, 21, 'Harry', 'Harry Pet Shelter', '6789876545', 'Mike', 'Dog', 'Lab', 'Male', 'Coimbatore', '4', 'A friendly dog', '1746100016_labrodar.jpg', '1746100016_labrodar.jpg', '1746100016_labrodar.jpg', 'available', '2025-05-02 01:54:26'),
(34, 21, 'Harry', 'Harry Pet Shelter', '6789876545', 'Groot', 'Dog', 'German shepard', 'Male', 'Coimbatore', '3', 'A friendly dog', '1746151765_shepard.jpg', '1746151765_shepard.jpg', '1746151765_shepard.jpg', 'adopted', '2025-05-04 09:00:53'),
(36, 21, 'Harry', 'Harry Pet Shelter', '6789876545', 'goldy', 'Rabbit', 'Netherland Dwarf', 'Male', 'Coimbatore', '2', 'Goldy, a Netherland Dwarf rabbit, is a tiny bundle of energy with a golden-hued coat. Curious and pl', '1746521734_dwarf.jpg', '1746521734_netherland.jpg', '1746521734_dwarfplaying.jpg', 'available', '2025-05-06 08:55:34'),
(37, 21, 'Harry', 'Harry Pet Shelter', '6789876545', 'micky', 'Cat', 'persian', 'Female', 'Coimbatore', '2', 'Micky, the Persian cat, exudes elegance with his long, luxurious fur and expressive eyes. Calm and a', '1746521875_persian.jpg', '1746521875_persiancat.jpg', '1746521875_persianplaying.jpg', 'available', '2025-05-06 08:57:55'),
(38, 21, 'Harry', 'Harry Pet Shelter', '6789876545', 'hassie', 'Bird', 'African grey', 'Male', 'Coimbatore', '1', 'Hassie, the African Grey parrot, is an intelligent and talkative companion known for her sharp memor', '1746522041_africangreybird.jpg', '1746522041_africangrey.jpg', '1746522041_africangreyplay.jpg', 'available', '2025-05-06 09:00:41');

-- --------------------------------------------------------

--
-- Table structure for table `serviceprice`
--

CREATE TABLE `serviceprice` (
  `id` int(11) NOT NULL,
  `serviceid` int(10) NOT NULL,
  `careid` varchar(50) NOT NULL,
  `servicetype` varchar(100) NOT NULL,
  `serviceprice` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `serviceprice`
--

INSERT INTO `serviceprice` (`id`, `serviceid`, `careid`, `servicetype`, `serviceprice`) VALUES
(16, 28, '1', 'Dental Care', 20.00),
(17, 35, '1', 'Behavior Consultation', 30.00),
(18, 32, '1', 'Behavior Consultation', 30.00),
(20, 24, '1', 'Dental Care', 20.00),
(23, 30, '4', 'Training', 2500.00),
(24, 38, '4', 'Boarding', 2500.00),
(26, 36, '4', 'Behavior Consultation', 3500.00),
(27, 37, '7', 'Socialization Session', 4500.00),
(28, 39, '8', 'Pet Grooming', 300.00),
(30, 41, '10', 'Training', 1000.00),
(31, 45, '10', 'Basic Commands Training', 2000.00),
(32, 44, '11', 'Behavior Consultation', 1500.00),
(33, 42, '11', 'Vaccination', 2000.00),
(34, 43, '11', 'Dental Care', 3000.00),
(35, 0, '10', 'Socialization Session', 3800.00);

-- --------------------------------------------------------

--
-- Table structure for table `shelter_info`
--

CREATE TABLE `shelter_info` (
  `shelter_id` int(10) NOT NULL,
  `sheltername` varchar(100) NOT NULL,
  `ownername` varchar(100) NOT NULL,
  `street` varchar(255) NOT NULL,
  `city` varchar(50) NOT NULL,
  `pin` varchar(10) NOT NULL,
  `state` varchar(50) NOT NULL,
  `mob` bigint(10) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `pass` varchar(255) NOT NULL,
  `profile_pic` varchar(200) NOT NULL,
  `proof_attachment` varchar(200) NOT NULL,
  `license` varchar(100) NOT NULL,
  `pid` int(10) DEFAULT NULL,
  `status` varchar(20) NOT NULL DEFAULT 'pending',
  `registeredtime` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `shelter_info`
--

INSERT INTO `shelter_info` (`shelter_id`, `sheltername`, `ownername`, `street`, `city`, `pin`, `state`, `mob`, `email`, `pass`, `profile_pic`, `proof_attachment`, `license`, `pid`, `status`, `registeredtime`) VALUES
(1, 'Happy Paws Shelter', 'Rashathi', '77', '123 Pet Street, New York, USA', '641011', 'Tamilnadu', 9597496759, 'rashath2003@gmail.com', 'QXbMMEvq', 'rasa.jpg', 'homepgimg.jpg', '', NULL, 'approved', '2025-05-04 10:08:30'),
(2, '24/7 Petcare', 'Jasper Devaraj', '95,bungalow street', 'coimbatore', '641011', 'Tamilnadu', 9894497015, 'jasperdevaraj@gmail.com', 'GqrP5uw3', 'jas.jpg', 'about.jpg', '', NULL, 'approved', '2025-05-02 01:55:28'),
(8, 'All in Onecare', 'RR8', '4/8,north street', 'coimbatore', '641011', 'Tamilnadu', 8220782541, 'abdfarizharis2541@gmail.com', '0OrfABRY', 'rasa.jpg', 'download.jpeg', '', NULL, 'pending', '2025-06-05 03:47:47'),
(16, 'WEcare pet', 'RR16', '4/8,north street', 'coimbatore', '641011', 'Tamilnadu', 8903115145, 'jasperd2003@gmail.com', 'I6HP3l0t', 'jasper.jpg', 'jd.jpg', '', NULL, 'approved', '2025-05-02 01:55:28'),
(18, 'Harry pet shelters', 'harry', 'sai baba colony', 'coimbatore', '767656', 'Tamilnadu', 6767676767, 'techvolt.devisri@gmail.com', 'RG3qRIPd', 'shel1.jpg', 'idproof.png', '', NULL, 'approved', '2025-05-02 01:55:28'),
(21, 'Harry Pet Shelter', 'Harry', 'sai baba colony', 'Coimbatore', '765656', 'Tamil Nadu', 6789876545, 'abdullahfariz613@gmail.com', 'bYAlmORj', 'prof.jpg', 'idproof.png', 'idproof.png', NULL, 'pending', '2025-06-05 03:45:14'),
(22, 'potterpet', 'Sam', '6,saibaba', 'Coimbatore', '641011', 'Tamil Nadu', 9345834365, 'jdtomjerry@gmail.com', '', 'prof.jpg', 'idproof.png', 'idproof.png', NULL, 'rejected', '2025-05-06 09:56:17'),
(23, 'muthu pet', 'muthu', '6,saibaba', 'Coimbatore', '641011', 'Tamil Nadu', 9345834365, 'smuthuramk444@gmail.com', 'OmjTHorp', 'prof.jpg', 'idproof.png', 'idproof.png', NULL, 'approved', '2025-06-04 17:08:42');

-- --------------------------------------------------------

--
-- Table structure for table `userdetail`
--

CREATE TABLE `userdetail` (
  `Email` varchar(50) DEFAULT NULL,
  `Password` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `usereg`
--

CREATE TABLE `usereg` (
  `id` int(11) NOT NULL,
  `name` varchar(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `mob` varchar(15) NOT NULL,
  `pass` varchar(255) NOT NULL,
  `dob` date NOT NULL,
  `gender` varchar(10) NOT NULL,
  `street` varchar(255) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `pin` varchar(10) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `profile_pic` varchar(20) NOT NULL,
  `proof_attachment` varchar(20) NOT NULL,
  `registeredtime` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `usereg`
--

INSERT INTO `usereg` (`id`, `name`, `email`, `mob`, `pass`, `dob`, `gender`, `street`, `city`, `pin`, `state`, `profile_pic`, `proof_attachment`, `registeredtime`) VALUES
(14, 'Rashathi', 'rashath2003@gmail.com', '9597496759', 'Rasathi@2003', '2003-12-10', 'Male', '4/8,north street', 'Tuticorin', '628620', 'Tamilnadu', 'rasathikalifa.jpg', 'darkwebcard.png', '2025-05-02 01:55:12'),
(15, 'Abdullah Fariz I', 'abdfarizharis2541@gmail.com', '9345834365', 'Fariz@123', '2003-11-28', 'Male', '4/8,north street', 'Coimbatore', '628620', 'Tamilnadu', 'fariz.jpg', 'debuggingcard.png', '2025-05-02 01:55:12'),
(20, 'Harish', 'abdullahfariz613@gmail.com', '7645342312', 'Harish1234@', '2001-12-12', 'Male', 'sai ram towers', 'Coimbatore', '675656', 'Tamil Nadu', 'prof.jpg', 'prof.jpg', '2025-05-02 01:55:12');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `userid` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `admin_info`
--
ALTER TABLE `admin_info`
  ADD PRIMARY KEY (`admin_id`);

--
-- Indexes for table `adoption_app`
--
ALTER TABLE `adoption_app`
  ADD PRIMARY KEY (`adoptionid`);

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`bookingid`);

--
-- Indexes for table `carebookings`
--
ALTER TABLE `carebookings`
  ADD PRIMARY KEY (`carebookingid`);

--
-- Indexes for table `careresource_info`
--
ALTER TABLE `careresource_info`
  ADD PRIMARY KEY (`careid`);

--
-- Indexes for table `care_reg`
--
ALTER TABLE `care_reg`
  ADD PRIMARY KEY (`centreid`),
  ADD UNIQUE KEY `centreid` (`centreid`,`careresourcerid`);

--
-- Indexes for table `cpass`
--
ALTER TABLE `cpass`
  ADD PRIMARY KEY (`passid`);

--
-- Indexes for table `pass`
--
ALTER TABLE `pass`
  ADD PRIMARY KEY (`passid`);

--
-- Indexes for table `payment`
--
ALTER TABLE `payment`
  ADD PRIMARY KEY (`payid`);

--
-- Indexes for table `product_info`
--
ALTER TABLE `product_info`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `serviceprice`
--
ALTER TABLE `serviceprice`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `shelter_info`
--
ALTER TABLE `shelter_info`
  ADD PRIMARY KEY (`shelter_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `usereg`
--
ALTER TABLE `usereg`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`userid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `admin_info`
--
ALTER TABLE `admin_info`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `adoption_app`
--
ALTER TABLE `adoption_app`
  MODIFY `adoptionid` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `bookingid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=58;

--
-- AUTO_INCREMENT for table `carebookings`
--
ALTER TABLE `carebookings`
  MODIFY `carebookingid` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `careresource_info`
--
ALTER TABLE `careresource_info`
  MODIFY `careid` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `care_reg`
--
ALTER TABLE `care_reg`
  MODIFY `centreid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `cpass`
--
ALTER TABLE `cpass`
  MODIFY `passid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `pass`
--
ALTER TABLE `pass`
  MODIFY `passid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `payment`
--
ALTER TABLE `payment`
  MODIFY `payid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `product_info`
--
ALTER TABLE `product_info`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT for table `serviceprice`
--
ALTER TABLE `serviceprice`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `shelter_info`
--
ALTER TABLE `shelter_info`
  MODIFY `shelter_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `usereg`
--
ALTER TABLE `usereg`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `userid` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
