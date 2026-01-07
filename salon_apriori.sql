-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Oct 09, 2024 at 02:55 PM
-- Server version: 8.0.30
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `salon_apriori`
--

-- --------------------------------------------------------

--
-- Table structure for table `association`
--

CREATE TABLE `association` (
  `id` bigint UNSIGNED NOT NULL,
  `antecedents` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `consequents` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `antecedent_support` float NOT NULL,
  `consequent_support` float NOT NULL,
  `support` float NOT NULL,
  `confidence` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `association`
--

INSERT INTO `association` (`id`, `antecedents`, `consequents`, `antecedent_support`, `consequent_support`, `support`, `confidence`) VALUES
(80, '[\"nail art\"]', '[\"press on\"]', 0.852174, 0.391304, 0.391304, 0.459184),
(81, '[\"press on\"]', '[\"nail art\"]', 0.391304, 0.852174, 0.391304, 1),
(82, '[\"nail art\"]', '[\"remove\"]', 0.852174, 0.565217, 0.530435, 0.622449),
(83, '[\"remove\"]', '[\"nail art\"]', 0.565217, 0.852174, 0.530435, 0.938462),
(84, '[\"nail art\"]', '[\"retouch\"]', 0.852174, 0.426087, 0.356522, 0.418367),
(85, '[\"retouch\"]', '[\"nail art\"]', 0.426087, 0.852174, 0.356522, 0.836735),
(86, '[\"press on\"]', '[\"remove\"]', 0.391304, 0.565217, 0.391304, 1),
(87, '[\"remove\"]', '[\"press on\"]', 0.565217, 0.391304, 0.391304, 0.692308),
(88, '[\"retouch\"]', '[\"remove\"]', 0.426087, 0.565217, 0.147826, 0.346939),
(89, '[\"remove\"]', '[\"retouch\"]', 0.565217, 0.426087, 0.147826, 0.261538),
(90, '[\"nail art\", \"press on\"]', '[\"remove\"]', 0.391304, 0.565217, 0.391304, 1),
(91, '[\"nail art\", \"remove\"]', '[\"press on\"]', 0.530435, 0.391304, 0.391304, 0.737705),
(92, '[\"press on\", \"remove\"]', '[\"nail art\"]', 0.391304, 0.852174, 0.391304, 1),
(93, '[\"nail art\"]', '[\"press on\", \"remove\"]', 0.852174, 0.391304, 0.391304, 0.459184),
(94, '[\"press on\"]', '[\"nail art\", \"remove\"]', 0.391304, 0.530435, 0.391304, 1),
(95, '[\"remove\"]', '[\"nail art\", \"press on\"]', 0.565217, 0.391304, 0.391304, 0.692308),
(96, '[\"nail art\", \"retouch\"]', '[\"remove\"]', 0.356522, 0.565217, 0.130435, 0.365854),
(97, '[\"nail art\", \"remove\"]', '[\"retouch\"]', 0.530435, 0.426087, 0.130435, 0.245902),
(98, '[\"retouch\", \"remove\"]', '[\"nail art\"]', 0.147826, 0.852174, 0.130435, 0.882353),
(99, '[\"nail art\"]', '[\"retouch\", \"remove\"]', 0.852174, 0.147826, 0.130435, 0.153061),
(100, '[\"retouch\"]', '[\"nail art\", \"remove\"]', 0.426087, 0.530435, 0.130435, 0.306122),
(101, '[\"remove\"]', '[\"nail art\", \"retouch\"]', 0.565217, 0.356522, 0.130435, 0.230769);

-- --------------------------------------------------------

--
-- Table structure for table `settings`
--

CREATE TABLE `settings` (
  `id` tinyint NOT NULL,
  `min_support` float NOT NULL,
  `min_confidence` float NOT NULL,
  `durasi` tinyint DEFAULT NULL,
  `tanggal_mulai` date DEFAULT NULL,
  `tanggal_selesai` date DEFAULT NULL,
  `status` enum('active','non active') COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'non active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `settings`
--

INSERT INTO `settings` (`id`, `min_support`, `min_confidence`, `durasi`, `tanggal_mulai`, `tanggal_selesai`, `status`) VALUES
(1, 0.1, 0.2, 10, '2023-01-01', '2024-10-09', 'non active'),
(3, 0.1, 0.3, 20, '2023-01-01', '2024-10-09', 'non active');

-- --------------------------------------------------------

--
-- Table structure for table `strategies`
--

CREATE TABLE `strategies` (
  `id` tinyint NOT NULL,
  `nama` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `keterangan` text COLLATE utf8mb4_general_ci NOT NULL,
  `status` enum('active','non active') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'non active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `strategies`
--

INSERT INTO `strategies` (`id`, `nama`, `keterangan`, `status`) VALUES
(1, 'Paket Perawatan Wajah', 'Menawarkan paket perawatan wajah yang menggabungkan facial, masker, dan pijat wajah dengan harga khusus.', 'active'),
(3, 'Diskon untuk Pelanggan Setia', 'Memberikan diskon 20% untuk pelanggan yang melakukan lebih dari 5 transaksi dalam sebulan.', 'non active'),
(4, 'Rekomendasi Perawatan', 'Menggunakan data transaksi untuk merekomendasikan perawatan lain berdasarkan perawatan yang sering dibeli bersamaan, seperti pijat dan lulur.', 'non active'),
(5, 'Promo Musiman', 'Menawarkan promo khusus untuk layanan tertentu selama musim tertentu, seperti potongan rambut gratis untuk setiap pembelian perawatan tubuh.', 'non active'),
(6, 'Loyalty Program', 'Mengimplementasikan program loyalitas yang memberikan poin untuk setiap transaksi, yang dapat ditukarkan dengan layanan gratis atau potongan harga.', 'non active');

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` bigint UNSIGNED NOT NULL,
  `id_user` tinyint UNSIGNED NOT NULL,
  `tanggal` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `customer` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `treatment` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `total` varchar(255) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`id`, `id_user`, `tanggal`, `customer`, `treatment`, `total`) VALUES
(256, 1, '2023-05-01 00:00:00', 'mbk risa', 'eyelash + nail art', '140000'),
(257, 1, '2023-05-02 00:00:00', 'hakim kim', 'nail art + eyelash', '300000'),
(258, 1, '2023-05-03 00:00:00', 'fina fap', 'nail art + retouch', '170000'),
(259, 1, '2023-05-04 00:00:00', 'ita', 'nail art + remove + retouch', '200000'),
(260, 1, '2023-05-05 00:00:00', 'cho eccopark', 'nail art + press on + remove', '85000'),
(261, 1, '2023-05-06 00:00:00', 'isna', 'nail art + remove + retouch', '80000'),
(262, 1, '2023-05-07 00:00:00', 'angela', 'nail art + retouch', '80000'),
(263, 1, '2023-05-08 00:00:00', 'maria', 'hairdo + lashlift + eyelash', '50000'),
(264, 1, '2023-05-09 00:00:00', 'rara', 'nail art + lashlift', '120000'),
(265, 1, '2023-05-10 00:00:00', 'haerani', 'nail art + eyelash', '300000'),
(266, 1, '2023-05-11 00:00:00', 'lerystya', 'make up + hairdo', '110000'),
(267, 1, '2023-05-12 00:00:00', 'miscele', 'nail art + press on + remove', '175000'),
(268, 1, '2023-05-13 00:00:00', 'saskiaamalia', 'nail art + press on + remove', '100000'),
(269, 1, '2023-05-14 00:00:00', 'jihan', 'eyelash + remove + make up', '150000'),
(270, 1, '2023-05-15 00:00:00', 'awa', 'nail art + retouch', '60000'),
(271, 1, '2023-05-16 00:00:00', 'lashlift', 'lashlift + retouch + remove', '150000'),
(272, 1, '2023-05-17 00:00:00', 'nail art', 'nail art + remove + press on', '60000'),
(273, 1, '2023-05-18 00:00:00', 'nail art 4 orang', 'nail art + remove + press on', '495000'),
(274, 1, '2023-05-19 00:00:00', 'nail art', 'nail art + retouch', '170000'),
(275, 1, '2023-05-20 00:00:00', 'nail art', 'nail art + retouch', '75000'),
(276, 1, '2023-06-01 00:00:00', 'sukma', 'nail art + remove + retouch', '95000'),
(277, 1, '2023-06-01 00:00:00', 'Hakim', 'nail art + remove + retouch', '200000'),
(278, 1, '2023-06-01 00:00:00', 'Vinza', 'nail art + retouch', '90000'),
(279, 1, '2023-06-02 00:00:00', 'lidia ', 'nail art + remove + press on', '120000'),
(280, 1, '2023-06-02 00:00:00', 'maya', 'nail art + retouch', '200000'),
(281, 1, '2023-06-03 00:00:00', 'dinda ', 'nail art + retouch', '85000'),
(282, 1, '2023-06-04 00:00:00', 'ahyar', 'nail art + press on + remove', '80000'),
(283, 1, '2023-06-04 00:00:00', 'cici', 'nail art + press on + remove', '35000'),
(284, 1, '2023-06-05 00:00:00', 'klarita', 'nail art + lashlift', '94000'),
(285, 1, '2023-06-07 00:00:00', 'resti', 'nail art + press on + remove', '75000'),
(286, 1, '2023-06-07 00:00:00', 'klarita', 'nail art + eyelash', '140000'),
(287, 1, '2023-06-08 00:00:00', 'luci', 'nail art + retouch', '90000'),
(288, 1, '2023-06-09 00:00:00', 'elsa', 'nail art + remove + retouch', '84000'),
(289, 1, '2023-06-09 00:00:00', 'mina', 'nail art + remove + press on', '60000'),
(290, 1, '2023-06-15 00:00:00', 'septina', 'nail art + press on + remove', '55000'),
(291, 1, '2023-06-16 00:00:00', 'mbk nia', 'nail art + retouch', '130000'),
(292, 1, '2023-06-17 00:00:00', 'maria', 'nail art + remove + press on', '66000'),
(293, 1, '2023-06-17 00:00:00', 'dian novita', 'nail art + remove + press on', '65000'),
(294, 1, '2023-06-18 00:00:00', 'jihan fatin', 'nail art + lashlift + eyelash', '275000'),
(295, 1, '2023-06-18 00:00:00', 'shinta', 'nail art + remove + press on', '75000'),
(296, 1, '2023-06-19 00:00:00', 'dwi elsiyani', 'nail art + press on + remove', '86000'),
(297, 1, '2023-06-21 00:00:00', 'hakim', 'nail art + remove', '200000'),
(298, 1, '2023-06-21 00:00:00', 'shintia', 'nail art + remove + press on', '70000'),
(299, 1, '2023-06-22 00:00:00', 'naya', 'nail art + press on + remove', '95000'),
(300, 1, '2023-06-24 00:00:00', 'galuh', 'nail art + press on + remove', '40000'),
(301, 1, '2023-06-27 00:00:00', 'cho eco park', 'nail art + press on + remove', '172000'),
(302, 1, '2023-07-03 00:00:00', 'kak inggar', 'nail art + remove + retouch', '165000'),
(303, 1, '2023-07-12 00:00:00', 'miscel ', 'lashlift + hairdo + retouch', '240000'),
(304, 1, '2023-07-13 00:00:00', 'rara', 'lashlift + hairdo + eyelash', '80000'),
(305, 1, '2023-07-16 00:00:00', 'mbk iggar', 'make up + hairdo', '100000'),
(306, 1, '2023-07-19 00:00:00', 'miscel ', 'make up + hairdo', '480000'),
(307, 1, '2023-07-21 00:00:00', 'kanaya', 'nail art + remove + retouch', '88000'),
(308, 1, '2023-07-21 00:00:00', 'alya', 'nail art + retouch', '80000'),
(309, 1, '2023-07-28 00:00:00', 'dian', 'nail art + press on + remove', '77000'),
(310, 1, '2023-07-28 00:00:00', 'maya', 'nail art + press on + remove', '80000'),
(311, 1, '2023-08-06 00:00:00', 'sintia', 'nail art + press on + remove', '90000'),
(312, 1, '2023-08-07 00:00:00', 'mbk inggar', 'nail art + press on + remove', '170000'),
(313, 1, '2023-08-10 00:00:00', 'hakim', 'nail art + remove + press on', '200000'),
(314, 1, '2023-08-11 00:00:00', 'mbk inggar', 'nail art + retouch', '50000'),
(315, 1, '2023-09-10 00:00:00', 'mbk inggar', 'nail art + retouch', '182000'),
(316, 1, '2023-09-12 00:00:00', 'jihan', 'eyelash + hairdo + remove', '240000'),
(317, 1, '2023-09-13 00:00:00', 'nail', 'nail art + remove + press on', '65000'),
(318, 1, '2023-09-14 00:00:00', 'putri tasya', 'nail art + press on + remove', '85000'),
(319, 1, '2023-09-15 00:00:00', 'resa', 'make up + hairdo + retouch', '100000'),
(320, 1, '2023-09-17 00:00:00', 'jihan', 'retouch + eyelash + nail art', '120000'),
(321, 1, '2023-09-17 00:00:00', 'inggar', 'make up + nail art', '160000'),
(322, 1, '2023-09-18 00:00:00', 'make up', 'make up + hairdo + eyelash', '690000'),
(323, 1, '2023-09-20 00:00:00', 'make up wisuda sttkd', 'make up + retouch + hairdo', '350000'),
(324, 1, '2023-09-21 00:00:00', 'jihan', 'nail art + lashlift', '246000'),
(325, 1, '2023-10-01 00:00:00', 'jihan/beti', 'eyelash + hairdo + retouch', '170000'),
(326, 1, '2023-10-02 00:00:00', 'desty', 'nail art + press on + remove', '48000'),
(327, 1, '2023-10-06 00:00:00', 'masya', 'nail art + remove + retouch', '62000'),
(328, 1, '2023-10-07 00:00:00', 'anis', 'nail art + press on + remove', '31000'),
(329, 1, '2023-10-07 00:00:00', 'amel', 'nail art + remove + retouch', '65000'),
(330, 1, '2023-10-11 00:00:00', 'mbk emi', 'eyelash + retouch + make up', '150000'),
(331, 1, '2023-10-16 00:00:00', 'farida', 'nail art + press on + remove', '175000'),
(332, 1, '2023-10-18 00:00:00', 'make up among tamu', 'make up + retouch + lashlift', '500000'),
(333, 1, '2023-10-09 00:00:00', 'septiana', 'nail art + press on + remove', '145000'),
(334, 1, '2023-10-10 00:00:00', 'bengkel', 'kramas', '10000'),
(335, 1, '2023-10-11 00:00:00', 'dwi elsi', 'nail art + retouch', '71000'),
(336, 1, '2023-10-12 00:00:00', 'feni', 'nail art + remove + press on', '99000'),
(337, 1, '2023-11-01 00:00:00', 'temen risma', 'nail art + remove + retouch', '39000'),
(338, 1, '2023-11-04 00:00:00', 'fina fap', 'nail art + retouch', '200000'),
(339, 1, '2023-11-04 00:00:00', 'cut', 'nail art + press on + remove', '60000'),
(340, 1, '2023-11-06 00:00:00', 'nail junior', 'nail art + press on + remove', '40000'),
(341, 1, '2023-11-08 00:00:00', 'nail metal', 'nail art + retouch', '129000'),
(342, 1, '2023-11-11 00:00:00', 'deris', 'nail art + remove + press on', '39000'),
(343, 1, '2023-11-12 00:00:00', 'wedding', 'nail art + press on + remove', '185000'),
(344, 1, '2023-11-13 00:00:00', 'mbk emi', 'eyelash + nail art', '280000'),
(345, 1, '2023-11-17 00:00:00', 'nail', 'nail art + retouch', '39000'),
(346, 1, '2023-11-19 00:00:00', 'nail', 'nail art + remove + press on', '69000'),
(347, 1, '2023-11-20 00:00:00', 'dita', 'nail art + press on + remove', '99000'),
(348, 1, '2023-11-21 00:00:00', 'wedding', 'nail art + remove + press on', '185000'),
(349, 1, '2023-11-24 00:00:00', 'nail', 'nail art + retouch', '65000'),
(350, 1, '2023-11-25 00:00:00', 'nail junior member', 'nail art + press on + remove', '49000'),
(351, 1, '2023-11-26 00:00:00', 'fap fina', 'nail art + remove + retouch', '100000'),
(352, 1, '2023-11-28 00:00:00', 'tatan & member', 'nail art + press on + remove', '80000'),
(353, 1, '2023-11-28 00:00:00', 'alfa & member', 'nail art + remove + retouch', '119000'),
(354, 1, '2023-11-29 00:00:00', 'deris member', 'nail art + retouch', '59000'),
(355, 1, '2023-12-02 00:00:00', 'jihan', 'nail art + press on + remove', '91000'),
(356, 1, '2023-12-04 00:00:00', 'airin', 'nail art + retouch', '130000'),
(357, 1, '2023-12-06 00:00:00', 'feby', 'nail art + retouch', '100000'),
(358, 1, '2023-12-07 00:00:00', 'lisa', 'nail art + retouch', '70000'),
(359, 1, '2023-12-07 00:00:00', 'maisa', 'nail art + remove + retouch', '115000'),
(360, 1, '2023-12-07 00:00:00', 'anisa', 'nail art + press on + remove', '119000'),
(361, 1, '2023-12-07 00:00:00', 'astri', 'remove + eyelash + retouch', '20000'),
(362, 1, '2023-12-08 00:00:00', 'irma', 'nail art + remove + retouch', '123000'),
(363, 1, '2023-12-08 00:00:00', 'zahra', 'nail art + retouch', '140000'),
(364, 1, '2023-12-08 00:00:00', 'seelli', 'nail art + press on + remove', '60000'),
(365, 1, '2023-12-09 00:00:00', 'rahma', 'nail art + press on + remove', '97000'),
(366, 1, '2023-12-09 00:00:00', 'nafda', 'nail art + retouch', '95000'),
(367, 1, '2023-12-11 00:00:00', 'tata', 'nail art + retouch', '70000'),
(368, 1, '2023-12-11 00:00:00', 'clara', 'nail art + remove + retouch', '184000'),
(369, 1, '2023-12-12 00:00:00', 'anggik', 'nail art + press on + remove', '71000'),
(370, 1, '2023-12-12 00:00:00', 'nadia', 'nail art + eyelash', '170000'),
(371, 1, '2023-12-13 00:00:00', 'helsa', 'nail art + press on + remove', '63000'),
(372, 1, '2023-12-13 00:00:00', 'nona', 'retouch + lashlift + hairdo', '10000'),
(373, 1, '2023-12-14 00:00:00', 'ika', 'nail art + retouch', '190000'),
(374, 1, '2023-12-14 00:00:00', 'intan', 'nail art + eyelash', '312000'),
(375, 1, '2023-12-14 00:00:00', 'yezika', 'nail art + retouch', '79000'),
(376, 1, '2023-12-15 00:00:00', 'linda', 'nail art + remove', '53000'),
(377, 1, '2023-12-15 00:00:00', 'widya', 'eyelash + hairdo + lashlift', '210000'),
(378, 1, '2023-12-15 00:00:00', 'venti', 'nail art + retouch', '41000'),
(379, 1, '2023-12-15 00:00:00', 'wayan', 'nail art + press on + remove', '61000'),
(380, 1, '2023-12-16 00:00:00', 'infanta', 'nail art + retouch', '140000'),
(381, 1, '2023-12-17 00:00:00', 'vin', 'nail art + press on + remove', '170000'),
(382, 1, '2023-12-17 00:00:00', 'dian', 'nail art + remove + press on', '120000'),
(383, 1, '2023-12-18 00:00:00', 'putri', 'nail art + remove + press on', '150000'),
(384, 1, '2023-12-18 00:00:00', 'maya', 'nail art + remove + retouch', '140000'),
(385, 1, '2023-12-19 00:00:00', 'evi', 'nail art + press on + remove', '77000'),
(386, 1, '2023-12-19 00:00:00', 'vegha', 'nail art + press on + remove', '75000'),
(387, 1, '2023-12-19 00:00:00', 'lia', 'nail art + retouch', '213000'),
(388, 1, '2023-12-20 00:00:00', 'rizka', 'nail art + retouch', '174000'),
(389, 1, '2023-12-20 00:00:00', 'rafi', 'nail art + press on + remove', '70000'),
(390, 1, '2023-12-20 00:00:00', 'repta', 'nail art + press on + remove', '85000'),
(391, 1, '2023-12-20 00:00:00', 'stefani', 'nail art + press on + remove', '90000'),
(392, 1, '2023-12-21 00:00:00', 'rizka', 'nail art + press on + remove', '111000'),
(393, 1, '2023-12-21 00:00:00', 'kesiaa', 'nail art + retouch', '150000'),
(394, 1, '2023-12-22 00:00:00', 'anisa', 'nail art + remove', '43000'),
(395, 1, '2023-12-22 00:00:00', 'zilka', 'nail art + retouch', '94000'),
(396, 1, '2023-12-22 00:00:00', 'afriani', 'nail art + press on + remove', '60000'),
(397, 1, '2023-12-23 00:00:00', 'adel', 'nail art + remove', '207000'),
(398, 1, '2023-12-23 00:00:00', 'carolin', 'nail art + press on + remove', '45000'),
(399, 1, '2023-12-23 00:00:00', 'putrri', 'nail art + retouch', '318000'),
(400, 1, '2023-12-23 00:00:00', 'ulfa', 'nail art + press on + remove', '103000'),
(401, 1, '2023-12-24 00:00:00', 'winda', 'make up + eyelash + remove', '100000'),
(402, 1, '2023-12-24 00:00:00', 'anisa', 'eyelash + retouch + lashlift', '90000'),
(403, 1, '2023-12-24 00:00:00', 'grace', 'eyelash + make up + remove', '100000'),
(404, 1, '2023-12-26 00:00:00', 'destri', 'nail art + press on + remove', '147000'),
(405, 1, '2023-12-26 00:00:00', 'rika', 'nail art + retouch', '105000'),
(406, 1, '2023-12-26 00:00:00', 'alhamidah', 'nail art + retouch', '185000'),
(407, 1, '2023-12-27 00:00:00', 'agnes', 'nail art + press on + remove', '73500'),
(408, 1, '2023-12-27 00:00:00', 'hana', 'nail art + remove + press on', '80500'),
(409, 1, '2023-12-27 00:00:00', 'anisa', 'nail art + remove + retouch', '165000'),
(410, 1, '2023-12-28 00:00:00', 'teresia', 'nail art + retouch', '91000'),
(411, 1, '2023-12-29 00:00:00', 'raina', 'nail art + press on + remove', '63000'),
(412, 1, '2023-12-29 00:00:00', 'yusri', 'nail art + press on + remove', '89000'),
(413, 1, '2023-12-29 00:00:00', 'el', 'nail art + remove + press on', '44000'),
(414, 1, '2023-12-30 00:00:00', 'rini', 'nail art + remove + press on', '111000'),
(415, 1, '2023-12-30 00:00:00', 'ineke', 'nail art + retouch', '70500'),
(416, 1, '2024-01-02 00:00:00', 'linda', 'nail art + retouch', '163000'),
(417, 1, '2024-01-02 00:00:00', 'indah', 'nail art + press on + remove', '70000'),
(418, 1, '2024-01-02 00:00:00', 'stefhani', 'nail art + remove + press on', '45000'),
(419, 1, '2024-01-02 00:00:00', 'fina ', 'nail art + press on + remove', '180000'),
(420, 1, '2024-01-03 00:00:00', 'indri', 'nail art + remove + retouch', '126000'),
(421, 1, '2024-01-03 00:00:00', 'cintya', 'nail art + remove + retouch', '35000'),
(422, 1, '2024-01-04 00:00:00', 'bagas', 'nail art + retouch', '99000'),
(423, 1, '2024-01-05 00:00:00', 'farida', 'nail art + press on + remove', '220000'),
(424, 1, '2024-01-06 00:00:00', 'rahma', 'nail art + press on + remove', '172000'),
(425, 1, '2024-01-06 00:00:00', 'jihan', 'nail art + retouch', '53000'),
(426, 1, '2024-01-08 00:00:00', 'lia', 'nail art + remove + press on', '95000'),
(427, 1, '2024-01-10 00:00:00', 'zahra', 'nail art + remove + press on', '110000'),
(428, 1, '2024-01-15 00:00:00', 'stefani', 'nail art + press on + remove', '99000'),
(429, 1, '2024-01-16 00:00:00', 'tatan', 'nail art + press on + remove', '89000'),
(430, 1, '2024-01-18 00:00:00', 'sakwa', 'nail art + remove + press on', '65000'),
(431, 1, '2024-01-19 00:00:00', 'dita', 'nail art + remove + retouch', '135000'),
(432, 1, '2024-01-20 00:00:00', 'deris', 'nail art + retouch', '90000'),
(433, 1, '2024-01-22 00:00:00', 'erika', 'nail art + retouch', '61000'),
(434, 1, '2024-01-22 00:00:00', 'ira', 'nail art + retouch', '181000'),
(435, 1, '2024-01-24 00:00:00', 'nessa', 'nail art + remove + retouch', '108000'),
(436, 1, '2024-01-24 00:00:00', 'tatan', 'nail art + retouch', '81000'),
(437, 1, '2024-01-24 00:00:00', 'widi', 'nail art + press on + remove', '103000'),
(438, 1, '2024-01-24 00:00:00', 'dina', 'nail art + press on + remove', '95000'),
(439, 1, '2024-01-25 00:00:00', 'maya', 'nail art + retouch', '136000'),
(440, 1, '2024-01-25 00:00:00', 'helsa', 'nail art + retouch', '76000'),
(441, 1, '2024-01-25 00:00:00', 'widi', 'nail art + press on + remove', '110000'),
(442, 1, '2024-01-26 00:00:00', 'tatan', 'nail art + retouch', '60000'),
(443, 1, '2024-01-26 00:00:00', 'sri', 'nail art + retouch', '131000'),
(444, 1, '2024-01-30 00:00:00', 'iin', 'nail art + press on + remove', '115000'),
(445, 1, '2024-02-03 00:00:00', 'shea', 'eyelash + hairdo + remove', '95000'),
(446, 1, '2024-04-02 00:00:00', 'jihan', 'remove + eyelash + hairdo', '131000'),
(447, 1, '2024-02-09 00:00:00', 'zahrra', 'eyelash + hairdo + remove', '81000'),
(448, 1, '2024-02-09 00:00:00', 'ecy', 'remove + eyelash + make up', '110000'),
(449, 1, '2024-02-10 00:00:00', 'shafie', 'lashlift + remove + make up', '103500'),
(450, 1, '2024-02-16 00:00:00', 'desi', 'hairdo + retouch + eyelash', '49000'),
(451, 1, '2024-02-16 00:00:00', 'mida', 'retouch + lashlift + eyelash', '134000'),
(452, 1, '2024-02-18 00:00:00', 'wulan', 'hairdo + eyelash + remove', '110000'),
(453, 1, '2024-02-18 00:00:00', 'tia', 'make up + eyelash + remove', '85000'),
(454, 1, '2024-02-22 00:00:00', 'keisa', 'make up + remove + retouch', '194000'),
(455, 1, '2024-02-23 00:00:00', 'yuliana', 'eyelash + remove + retouch', '85000'),
(456, 1, '2024-02-23 00:00:00', 'tya', 'lashlift + hairdo + remove', '190000'),
(457, 1, '2024-02-24 00:00:00', 'ratu', 'hairdo + make up + retouch', '209000'),
(458, 1, '2024-02-26 00:00:00', 'chata', 'make up + hairdo + lashlift', '45000'),
(459, 1, '2024-02-01 00:00:00', 'desi', 'make up + remove + eyelash', '81000'),
(460, 1, '2024-02-02 00:00:00', 'sri', 'nail art + eyelash', '270000'),
(461, 1, '2024-02-03 00:00:00', 'fina', 'make up + lashlift + remove', '205000'),
(462, 1, '2024-02-06 00:00:00', 'caca', 'retouch + eyelash + lashlift', '129000'),
(463, 1, '2024-02-09 00:00:00', 'mara', 'eyelash + make up + remove', '69000'),
(464, 1, '2024-02-07 00:00:00', 'anisa', 'retouch + eyelash + make up', '119000'),
(465, 1, '2024-02-13 00:00:00', 'sendu/dian', 'hairdo + retouch + make up', '107000'),
(466, 1, '2024-02-13 00:00:00', 'mey', 'hairdo + eyelash + make up', '44100'),
(467, 1, '2024-02-13 00:00:00', 'rahmina', 'hairdo + retouch + make up', '44100'),
(468, 1, '2024-02-15 00:00:00', 'ayu', 'make up + eyelash + retouch', '85000'),
(469, 1, '2024-02-17 00:00:00', 'wayan', 'make up + hairdo + remove', '60000'),
(470, 1, '2024-02-17 00:00:00', 'deris', 'lashlift + hairdo + eyelash', '30000'),
(471, 1, '2024-02-18 00:00:00', 'deris', 'nail art + lashlift', '105000'),
(472, 1, '2024-02-19 00:00:00', 'dayu', 'retouch + make up + lashlift', '15000'),
(473, 1, '2024-02-21 00:00:00', 'jihan', 'make up + lashlift + eyelash', '90000'),
(474, 1, '2024-02-22 00:00:00', 'anisa', 'remove + make up + retouch', '35000'),
(475, 1, '2024-02-22 00:00:00', 'mey', 'remove + eyelash + hairdo', '45000'),
(476, 1, '2024-02-22 00:00:00', 'sinta', 'remove + eyelash + hairdo', '61000'),
(477, 1, '2024-02-23 00:00:00', 'mely', 'remove + retouch + hairdo', '160000'),
(478, 1, '2024-02-23 00:00:00', 'deli', 'hairdo + eyelash + make up', '150000'),
(479, 1, '2024-02-23 00:00:00', 'diyana', 'lashlift + eyelash + hairdo', '150000'),
(480, 1, '2024-02-26 00:00:00', 'syifa', 'remove + lashlift + eyelash', '75000'),
(481, 1, '2024-02-28 00:00:00', 'diyana', 'remove + make up + retouch', '70000'),
(482, 1, '2024-03-01 00:00:00', 'indah', 'remove + retouch + eyelash', '99000'),
(483, 1, '2024-03-04 00:00:00', 'tia', 'make up + remove + hairdo', '140000'),
(484, 1, '2024-03-05 00:00:00', 'feby', 'remove + make up + lashlift', '20000'),
(485, 1, '2024-03-05 00:00:00', 'elsy', 'eyelash + retouch + lashlift', '110000'),
(486, 1, '2024-03-08 00:00:00', 'tika', 'lashlift + make up + hairdo', '85000'),
(487, 1, '2024-03-10 00:00:00', 'rere', 'remove + hairdo + lashlift', '61000'),
(488, 1, '2024-03-10 00:00:00', 'hamida', 'hairdo + remove + lashlift', '65000'),
(489, 1, '2024-03-10 00:00:00', 'lucky', 'remove + make up + eyelash', '132000'),
(490, 1, '2024-03-12 00:00:00', 'anisa', 'remove + eyelash + lashlift', '30000'),
(491, 1, '2024-03-14 00:00:00', 'tia', 'retouch + hairdo + remove', '70000'),
(492, 1, '2024-03-20 00:00:00', 'erika', 'lashlift + remove + hairdo', '75000'),
(493, 1, '2024-03-21 00:00:00', 'destri', 'eyelash + remove + hairdo', '140000'),
(494, 1, '2024-03-21 00:00:00', 'iin', 'remove + lashlift + eyelash', '16000'),
(495, 1, '2024-03-21 00:00:00', 'agnes', 'hairdo + make up + remove', '85000'),
(496, 1, '2024-03-23 00:00:00', 'pedra', 'hairdo + lashlift + remove', '160000'),
(497, 1, '2024-03-26 00:00:00', 'indah', 'make up + retouch + hairdo', '75000'),
(498, 1, '2024-03-26 00:00:00', 'lisa', 'make up + eyelash + lashlift', '145000'),
(499, 1, '2024-03-29 00:00:00', 'vinensia', 'retouch + eyelash + remove', '166000'),
(500, 1, '2024-03-30 00:00:00', 'karin', 'remove + lashlift + retouch', '67000'),
(501, 1, '2024-03-30 00:00:00', 'chata', 'hairdo + make up + lashlift', '52000'),
(502, 1, '2024-03-01 00:00:00', 'ayu', 'lashlift + eyelash + remove', '161000'),
(503, 1, '2024-03-01 00:00:00', 'neta', 'lashlift + hairdo + retouch', '70000'),
(504, 1, '2024-03-01 00:00:00', 'devina', 'remove + retouch + make up', '76000'),
(505, 1, '2024-03-04 00:00:00', 'gea', 'make up + eyelash + remove', '67000'),
(506, 1, '2024-03-07 00:00:00', 'echa', 'make up + eyelash + retouch', '60000'),
(507, 1, '2024-03-15 00:00:00', 'eve', 'eyelash + hairdo + lashlift', '69000'),
(508, 1, '2024-03-16 00:00:00', 'deris', 'remove + lashlift + make up', '69000'),
(509, 1, '2024-03-17 00:00:00', 'jelita', 'make up + lashlift + eyelash', '74000'),
(510, 1, '2024-03-18 00:00:00', 'chealse', 'make up + lashlift + retouch', '93500'),
(511, 1, '2024-03-22 00:00:00', 'restu', 'lashlift + eyelash + retouch', '49000'),
(512, 1, '2024-03-26 00:00:00', 'heni', 'hairdo + retouch + remove', '108000'),
(513, 1, '2024-03-26 00:00:00', 'gea', 'remove + eyelash + make up', '39000'),
(514, 1, '2024-03-27 00:00:00', 'diyana', 'retouch + hairdo + remove', '146000'),
(515, 1, '2024-03-28 00:00:00', 'zahra', 'make up + retouch + remove', '126000'),
(516, 1, '2024-04-02 00:00:00', 'jihan', 'hairdo + make up + eyelash', '133000'),
(517, 1, '2024-04-02 00:00:00', 'emi', 'nail art + eyelash', '338000'),
(518, 1, '2024-04-03 00:00:00', 'echi', 'hairdo + remove + make up', '95000'),
(519, 1, '2024-04-04 00:00:00', 'helen', 'nail art + eyelash', '290000'),
(520, 1, '2024-04-04 00:00:00', 'roro', 'make up + eyelash + remove', '124000'),
(521, 1, '2024-04-04 00:00:00', 'kiki', 'make up + eyelash + retouch', '131000'),
(522, 1, '2024-04-04 00:00:00', 'deris', 'make up + retouch + remove', '27500'),
(523, 1, '2024-04-05 00:00:00', 'zahra', 'lashlift + remove + retouch', '55000'),
(524, 1, '2024-04-05 00:00:00', 'pelangi', 'retouch + make up + remove', '81000'),
(525, 1, '2024-04-05 00:00:00', 'ifon', 'retouch + remove + eyelash', '74000'),
(526, 1, '2024-04-05 00:00:00', 'cathrin', 'hairdo + eyelash + lashlift', '74000'),
(527, 1, '2024-04-05 00:00:00', 'anjani', 'retouch + lashlift + hairdo', '83000'),
(528, 1, '2024-04-05 00:00:00', 'febiani', 'eyelash + lashlift + make up', '145000'),
(529, 1, '2024-04-05 00:00:00', 'winda', 'remove + hairdo + eyelash', '130000'),
(530, 1, '2024-04-05 00:00:00', 'kadek maya', 'lashlift + make up + eyelash', '125000'),
(531, 1, '2024-04-05 00:00:00', 'jihan', 'retouch + hairdo + remove', '230000'),
(532, 1, '2024-04-06 00:00:00', 'intania', 'make up + remove + hairdo', '125000'),
(533, 1, '2024-04-06 00:00:00', 'kinaya', 'retouch + make up + remove', '158000'),
(534, 1, '2024-04-07 00:00:00', 'keisa', 'retouch + lashlift + eyelash', '201000'),
(535, 1, '2024-04-07 00:00:00', 'anisa', 'nail art + eyelash', '175000'),
(536, 1, '2024-04-07 00:00:00', 'septi', 'retouch + hairdo + eyelash', '201000'),
(537, 1, '2024-04-07 00:00:00', 'reida', 'make up + remove + lashlift', '138000'),
(538, 1, '2024-04-07 00:00:00', 'vania', 'retouch + hairdo + remove', '324000'),
(539, 1, '2024-04-07 00:00:00', 'khansa', 'eyelash + make up + remove', '224000'),
(540, 1, '2024-04-07 00:00:00', 'devi', 'eyelash + remove + lashlift', '210000'),
(541, 1, '2024-04-07 00:00:00', 'silvia', 'remove + eyelash + hairdo', '188000'),
(542, 1, '2024-04-07 00:00:00', 'nabila', 'make up + retouch + hairdo', '145000'),
(543, 1, '2024-04-07 00:00:00', 'kiki', 'hairdo + eyelash + make up', '131000'),
(544, 1, '2024-04-07 00:00:00', 'luluk', 'retouch + lashlift + hairdo', '77000'),
(545, 1, '2024-04-08 00:00:00', 'angelina', 'make up + retouch + lashlift', '110000'),
(546, 1, '2024-04-08 00:00:00', 'alivia', 'lashlift + remove + retouch', '196000'),
(547, 1, '2024-04-08 00:00:00', 'anis', 'eyelash + retouch + remove', '61000'),
(548, 1, '2024-04-08 00:00:00', 'cantika', 'make up + hairdo + eyelash', '244000'),
(549, 1, '2024-04-08 00:00:00', 'dita', 'retouch + remove + lashlift', '154000'),
(550, 1, '2024-04-08 00:00:00', 'nesya', 'hairdo + retouch + make up', '181000'),
(551, 1, '2024-04-08 00:00:00', 'hera', 'lashlift + eyelash + retouch', '140000'),
(552, 1, '2024-04-08 00:00:00', 'tika', 'remove + retouch + hairdo', '76000'),
(553, 1, '2024-04-08 00:00:00', 'mina', 'lashlift + make up + hairdo', '58000'),
(554, 1, '2024-04-08 00:00:00', 'anara', 'remove + hairdo + eyelash', '86000'),
(555, 1, '2024-04-08 00:00:00', 'elvi', 'eyelash + lashlift + make up', '105000'),
(556, 1, '2024-04-09 00:00:00', 'galih', 'remove + lashlift + retouch', '91000'),
(557, 1, '2024-04-09 00:00:00', 'tya', 'eyelash + make up + retouch', '90000'),
(558, 1, '2024-04-09 00:00:00', 'ayu', 'hairdo + lashlift + eyelash', '145000'),
(559, 1, '2024-04-09 00:00:00', 'winda', 'eyelash + hairdo + retouch', '205000'),
(560, 1, '2024-04-09 00:00:00', 'feby', 'make up + remove + hairdo', '55000'),
(561, 1, '2024-04-09 00:00:00', 'destri', 'make up + lashlift + eyelash', '280000'),
(562, 1, '2024-04-09 00:00:00', 'keisya', 'lashlift + hairdo + eyelash', '61000'),
(563, 1, '2024-04-09 00:00:00', 'nisa', 'hairdo + retouch + eyelash', '45000'),
(564, 1, '2024-04-09 00:00:00', 'wida', 'retouch + hairdo + eyelash', '186000'),
(565, 1, '2024-04-02 00:00:00', 'meta', 'hairdo + eyelash + remove', '89000'),
(566, 1, '2024-04-03 00:00:00', 'nevi', 'lashlift + make up + retouch', '47000'),
(567, 1, '2024-04-03 00:00:00', 'beatrice', 'remove + retouch + hairdo', '84000'),
(568, 1, '2024-04-03 00:00:00', 'tatan', 'eyelash + make up + retouch', '77000'),
(569, 1, '2024-04-03 00:00:00', 'manda', 'eyelash + remove + lashlift', '107000'),
(570, 1, '2024-04-03 00:00:00', 'safira', 'make up + lashlift + retouch', '57000'),
(571, 1, '2024-04-03 00:00:00', 'sela', 'remove + lashlift + eyelash', '99000'),
(572, 1, '2024-04-05 00:00:00', 'abel', 'eyelash + lashlift + retouch', '96000'),
(573, 1, '2024-04-05 00:00:00', 'rara', 'remove + make up + retouch', '112000'),
(574, 1, '2024-04-06 00:00:00', 'gracelea', 'retouch + hairdo + eyelash', '75000'),
(575, 1, '2024-05-02 00:00:00', 'jihan', 'remove + eyelash + retouch', '91000'),
(576, 1, '2024-05-04 00:00:00', 'airin', 'eyelash + remove + lashlift', '130000'),
(577, 1, '2024-05-06 00:00:00', 'feby', 'lashlift + retouch + eyelash', '100000'),
(578, 1, '2024-05-07 00:00:00', 'lisa', 'lashlift + make up + retouch', '70000'),
(579, 1, '2024-05-07 00:00:00', 'maisa', 'lashlift + remove + make up', '115000'),
(580, 1, '2024-05-07 00:00:00', 'anisa', 'eyelash + remove + lashlift', '119000'),
(581, 1, '2024-05-07 00:00:00', 'astri', 'remove + lashlift + retouch', '20000'),
(582, 1, '2024-05-08 00:00:00', 'irma', 'make up + eyelash + lashlift', '123000'),
(583, 1, '2024-05-08 00:00:00', 'zahra', 'hairdo + eyelash + make up', '140000'),
(584, 1, '2024-05-08 00:00:00', 'seelli', 'hairdo + eyelash + remove', '60000'),
(585, 1, '2024-05-09 00:00:00', 'rahma', 'make up + retouch + eyelash', '97000'),
(586, 1, '2024-05-09 00:00:00', 'nafda', 'make up + hairdo + remove', '95000'),
(587, 1, '2024-05-11 00:00:00', 'tata', 'make up + lashlift + remove', '70000'),
(588, 1, '2024-05-11 00:00:00', 'clara', 'lashlift + retouch + hairdo', '184000'),
(589, 1, '2024-05-12 00:00:00', 'anggik', 'retouch + remove + eyelash', '71000'),
(590, 1, '2024-05-12 00:00:00', 'nadia', 'nail art + eyelash', '170000'),
(591, 1, '2024-05-13 00:00:00', 'helsa', 'make up + hairdo + lashlift', '63000'),
(592, 1, '2024-05-13 00:00:00', 'nona', 'retouch + make up + lashlift', '10000'),
(593, 1, '2024-05-14 00:00:00', 'ika', 'lashlift + make up + hairdo', '190000'),
(594, 1, '2024-05-14 00:00:00', 'intan', 'nail art + eyelash', '312000'),
(595, 1, '2024-05-14 00:00:00', 'yezika', 'retouch + make up + hairdo', '79000'),
(596, 1, '2024-05-15 00:00:00', 'linda', 'nail art + remove', '53000'),
(597, 1, '2024-05-15 00:00:00', 'widya', 'eyelash + retouch + make up', '210000'),
(598, 1, '2024-05-15 00:00:00', 'venti', 'hairdo + make up + retouch', '41000'),
(599, 1, '2024-05-15 00:00:00', 'wayan', 'lashlift + hairdo + eyelash', '61000'),
(600, 1, '2024-05-16 00:00:00', 'infanta', 'hairdo + lashlift + eyelash', '140000'),
(601, 1, '2024-05-17 00:00:00', 'vin', 'eyelash + remove + lashlift', '170000'),
(602, 1, '2024-05-17 00:00:00', 'dian', 'make up + remove + hairdo', '120000'),
(603, 1, '2024-05-18 00:00:00', 'putri', 'lashlift + eyelash + hairdo', '150000'),
(604, 1, '2024-05-18 00:00:00', 'maya', 'make up + lashlift + eyelash', '140000'),
(605, 1, '2024-05-19 00:00:00', 'evi', 'retouch + make up + eyelash', '77000'),
(606, 1, '2024-05-19 00:00:00', 'vegha', 'eyelash + remove + retouch', '75000'),
(607, 1, '2024-05-19 00:00:00', 'lia', 'lashlift + retouch + remove', '213000'),
(608, 1, '2024-05-20 00:00:00', 'rizka', 'retouch + remove + eyelash', '174000'),
(609, 1, '2024-05-20 00:00:00', 'rafi', 'hairdo + make up + lashlift', '70000'),
(610, 1, '2024-05-20 00:00:00', 'repta', 'retouch + lashlift + hairdo', '85000'),
(611, 1, '2024-05-20 00:00:00', 'stefani', 'make up + hairdo + eyelash', '90000'),
(612, 1, '2024-05-21 00:00:00', 'rizka', 'make up + lashlift + remove', '111000'),
(613, 1, '2024-05-21 00:00:00', 'kesiaa', 'remove + make up + retouch', '150000'),
(614, 1, '2024-05-22 00:00:00', 'anisa', 'nail art + remove', '43000'),
(615, 1, '2024-05-22 00:00:00', 'zilka', 'remove + make up + hairdo', '94000'),
(616, 1, '2024-05-22 00:00:00', 'afriani', 'hairdo + lashlift + eyelash', '60000'),
(617, 1, '2024-05-23 00:00:00', 'adel', 'nail art + remove', '207000'),
(618, 1, '2024-05-23 00:00:00', 'carolin', 'eyelash + lashlift + retouch', '45000'),
(619, 1, '2024-05-23 00:00:00', 'putrri', 'remove + lashlift + eyelash', '318000'),
(620, 1, '2024-05-23 00:00:00', 'ulfa', 'lashlift + eyelash + hairdo', '103000'),
(621, 1, '2024-05-24 00:00:00', 'winda', 'make up + retouch + remove', '100000'),
(622, 1, '2024-05-24 00:00:00', 'anisa', 'eyelash + lashlift + remove', '90000'),
(623, 1, '2024-05-24 00:00:00', 'grace', 'eyelash + make up + remove', '100000'),
(624, 1, '2024-05-26 00:00:00', 'destri', 'eyelash + remove + retouch', '147000'),
(625, 1, '2024-05-26 00:00:00', 'rika', 'eyelash + remove + hairdo', '105000'),
(626, 1, '2024-05-26 00:00:00', 'alhamidah', 'eyelash + hairdo + lashlift', '185000'),
(627, 1, '2024-05-27 00:00:00', 'agnes', 'retouch + eyelash + make up', '73500'),
(628, 1, '2024-05-27 00:00:00', 'hana', 'retouch + hairdo + remove', '80500'),
(629, 1, '2024-05-27 00:00:00', 'anisa', 'hairdo + make up + lashlift', '165000'),
(630, 1, '2024-05-28 00:00:00', 'teresia', 'hairdo + retouch + remove', '91000'),
(631, 1, '2024-05-29 00:00:00', 'eyelash hmc', 'eyelash + make up + retouch', '130000'),
(632, 1, '2024-05-30 00:00:00', 'make up 7 org', 'make up + lashlift + eyelash', '550000'),
(633, 1, '2024-05-30 00:00:00', 'inggar hmc', 'lashlift + retouch + make up', '200000'),
(634, 1, '2024-05-30 00:00:00', 'hmc ika', 'nail art + eyelash', '272000'),
(635, 1, '2024-05-30 00:00:00', 'fina hmc', 'hairdo + eyelash + remove', '250000'),
(636, 1, '2024-05-02 00:00:00', 'jihan', 'remove + make up + retouch', '91000'),
(637, 1, '2024-05-04 00:00:00', 'airin', 'remove + lashlift + hairdo', '130000'),
(638, 1, '2024-05-06 00:00:00', 'feby', 'lashlift + eyelash + retouch', '100000'),
(639, 1, '2024-05-07 00:00:00', 'lisa', 'lashlift + remove + eyelash', '70000'),
(640, 1, '2024-05-07 00:00:00', 'maisa', 'retouch + eyelash + remove', '115000'),
(641, 1, '2024-05-07 00:00:00', 'anisa', 'hairdo + remove + make up', '119000'),
(642, 1, '2024-05-07 00:00:00', 'astri', 'remove + retouch + eyelash', '20000'),
(643, 1, '2024-05-08 00:00:00', 'irma', 'make up + eyelash + lashlift', '123000'),
(644, 1, '2024-05-08 00:00:00', 'zahra', 'eyelash + remove + lashlift', '140000'),
(645, 1, '2024-05-08 00:00:00', 'seelli', 'remove + hairdo + retouch', '60000'),
(646, 1, '2024-05-09 00:00:00', 'rahma', 'eyelash + lashlift + make up', '97000'),
(647, 1, '2024-05-09 00:00:00', 'nafda', 'eyelash + remove + retouch', '95000'),
(648, 1, '2024-05-11 00:00:00', 'tata', 'retouch + hairdo + eyelash', '70000'),
(649, 1, '2024-05-11 00:00:00', 'clara', 'retouch + lashlift + eyelash', '184000'),
(650, 1, '2024-05-12 00:00:00', 'anggik', 'retouch + eyelash + hairdo', '71000'),
(651, 1, '2024-05-12 00:00:00', 'nadia', 'nail art + eyelash', '170000'),
(652, 1, '2024-05-13 00:00:00', 'helsa', 'eyelash + hairdo + remove', '63000'),
(653, 1, '2024-05-13 00:00:00', 'nona', 'retouch + make up + lashlift', '10000'),
(654, 1, '2024-05-14 00:00:00', 'ika', 'retouch + lashlift + make up', '190000'),
(655, 1, '2024-05-14 00:00:00', 'intan', 'nail art + eyelash', '312000'),
(656, 1, '2024-05-14 00:00:00', 'yezika', 'eyelash + remove + retouch', '79000'),
(657, 1, '2024-05-15 00:00:00', 'linda', 'nail art + remove', '53000'),
(658, 1, '2024-05-15 00:00:00', 'widya', 'eyelash + remove + retouch', '210000'),
(659, 1, '2024-05-15 00:00:00', 'venti', 'retouch + lashlift + remove', '41000'),
(660, 1, '2024-05-15 00:00:00', 'wayan', 'remove + hairdo + make up', '61000'),
(661, 1, '2024-05-16 00:00:00', 'infanta', 'make up + hairdo + retouch', '140000'),
(662, 1, '2024-05-17 00:00:00', 'vin', 'retouch + hairdo + lashlift', '170000'),
(663, 1, '2024-05-17 00:00:00', 'dian', 'make up + remove + lashlift', '120000'),
(664, 1, '2024-05-18 00:00:00', 'putri', 'retouch + remove + hairdo', '150000'),
(665, 1, '2024-05-18 00:00:00', 'maya', 'eyelash + retouch + lashlift', '140000'),
(666, 1, '2024-05-19 00:00:00', 'evi', 'retouch + make up + remove', '77000'),
(667, 1, '2024-05-19 00:00:00', 'vegha', 'lashlift + remove + hairdo', '75000'),
(668, 1, '2024-05-19 00:00:00', 'lia', 'lashlift + hairdo + eyelash', '213000'),
(669, 1, '2024-05-20 00:00:00', 'rizka', 'retouch + hairdo + remove', '174000'),
(670, 1, '2024-05-20 00:00:00', 'rafi', 'lashlift + make up + eyelash', '70000'),
(671, 1, '2024-05-20 00:00:00', 'repta', 'remove + eyelash + lashlift', '85000'),
(672, 1, '2024-05-20 00:00:00', 'stefani', 'hairdo + make up + retouch', '90000'),
(673, 1, '2024-05-21 00:00:00', 'rizka', 'hairdo + remove + lashlift', '111000'),
(674, 1, '2024-05-21 00:00:00', 'kesiaa', 'remove + lashlift + make up', '150000'),
(675, 1, '2024-05-22 00:00:00', 'anisa', 'nail art + remove', '43000'),
(676, 1, '2024-05-22 00:00:00', 'zilka', 'lashlift + remove + hairdo', '94000'),
(677, 1, '2024-05-22 00:00:00', 'afriani', 'eyelash + make up + remove', '60000'),
(678, 1, '2024-05-23 00:00:00', 'adel', 'nail art + remove', '207000'),
(679, 1, '2024-05-23 00:00:00', 'carolin', 'eyelash + hairdo + retouch', '45000'),
(680, 1, '2024-05-23 00:00:00', 'putrri', 'eyelash + make up + hairdo', '318000'),
(681, 1, '2024-05-23 00:00:00', 'ulfa', 'retouch + lashlift + hairdo', '103000'),
(682, 1, '2024-05-24 00:00:00', 'winda', 'make up + remove + lashlift', '100000'),
(683, 1, '2024-05-24 00:00:00', 'anisa', 'eyelash + retouch + make up', '90000'),
(684, 1, '2024-05-24 00:00:00', 'grace', 'eyelash + hairdo + remove', '100000'),
(685, 1, '2024-05-26 00:00:00', 'destri', 'eyelash + retouch + make up', '147000'),
(686, 1, '2024-05-26 00:00:00', 'rika', 'eyelash + retouch + make up', '105000'),
(687, 1, '2024-05-26 00:00:00', 'alhamidah', 'remove + hairdo + retouch', '185000'),
(688, 1, '2024-05-27 00:00:00', 'agnes', 'remove + hairdo + retouch', '73500'),
(689, 1, '2024-05-27 00:00:00', 'hana', 'eyelash + hairdo + make up', '80500'),
(690, 1, '2024-05-27 00:00:00', 'anisa', 'hairdo + make up + eyelash', '165000'),
(691, 1, '2024-05-28 00:00:00', 'teresia', 'lashlift + remove + hairdo', '91000'),
(692, 1, '2024-05-29 00:00:00', 'eyelash hmc', 'eyelash + remove + make up', '130000'),
(693, 1, '2024-05-30 00:00:00', 'make up 7 org', 'make up + hairdo + lashlift', '550000'),
(694, 1, '2024-05-30 00:00:00', 'inggar hmc', 'lashlift + eyelash + retouch', '200000'),
(695, 1, '2024-05-30 00:00:00', 'hmc ika', 'nail art + eyelash', '272000');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` tinyint UNSIGNED NOT NULL,
  `username` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `nama` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `alamat` varchar(200) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `telp` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `role` enum('admin','user') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `nama`, `alamat`, `telp`, `role`) VALUES
(1, 'user1', 'scrypt:32768:8:1$7yHi7vmsSermoosA$d078d7ace6c2f68ffa59825f2f40775fde7bfc084eefa4439fd6f7a09e27a5af5d78712e2e1fe729fe05e29c117f052a1427964bc76b40f5fab797ab439399a2', 'user1', 'Jl. Merdeka No. 123', '081234567890', 'user'),
(3, 'admin1', 'scrypt:32768:8:1$DnRo2fx1iJiD79TO$58e26ed7d0496e3d4821cd93e97a8448a1b9d945ad2c86f76fda04e061fabe751b9c66bd76b2243bc8e8a323f1f4427e70e3c0ffc7da705137d636c82dc19430', 'admin1', 'Jl. Berlubang No. 123', '543537656', 'admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `association`
--
ALTER TABLE `association`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `settings`
--
ALTER TABLE `settings`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `strategies`
--
ALTER TABLE `strategies`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `transactions_ibfk_1` (`id_user`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `association`
--
ALTER TABLE `association`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=102;

--
-- AUTO_INCREMENT for table `settings`
--
ALTER TABLE `settings`
  MODIFY `id` tinyint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `strategies`
--
ALTER TABLE `strategies`
  MODIFY `id` tinyint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=696;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` tinyint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
