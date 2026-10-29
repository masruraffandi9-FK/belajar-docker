-- phpMyAdmin SQL Dump
-- version 4.5.1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Oct 27, 2026 at 02:14 PM
-- Server version: 10.1.16-MariaDB
-- PHP Version: 7.0.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `kantin_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `menu`
--

CREATE TABLE `menu` (
  `id` int(11) NOT NULL,
  `nama` varchar(255) NOT NULL,
  `harga` int(11) NOT NULL,
  `kategori` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `menu`
--

INSERT INTO `menu` (`id`, `nama`, `harga`, `kategori`) VALUES
(2, 'Ayam Geprek Sambal Matah', 15000, 'Makanan'),
(3, 'Mie Ayam Bakso', 13000, 'Makanan'),
(4, 'Es Teh Manis Jumbo', 5000, 'Minuman'),
(5, 'Kopi Milk Brown Sugar', 12000, 'Minuman'),
(6, 'Matcha Latte Ice', 15000, 'Minuman'),
(7, 'Americano', 10000, 'Minuman'),
(8, 'Nasi Goreng Spesial', 20000, 'Makanan');

-- --------------------------------------------------------

--
-- Table structure for table `pesanan`
--

CREATE TABLE `pesanan` (
  `id` int(11) NOT NULL,
  `nama_pemesan` varchar(255) NOT NULL,
  `menu_id` int(11) NOT NULL,
  `jumlah` int(11) NOT NULL,
  `total_harga` int(11) NOT NULL,
  `metode_pembayaran` varchar(50) DEFAULT 'Tunai',
  `status_pembayaran` varchar(50) DEFAULT 'Belum Bayar',
  `status` varchar(50) DEFAULT 'Diproses'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pesanan`
--

INSERT INTO `pesanan` (`id`, `nama_pemesan`, `menu_id`, `jumlah`, `total_harga`, `metode_pembayaran`, `status_pembayaran`, `status`) VALUES
(1, 'ainy', 3, 1, 13000, 'QRIS', 'Lunas', 'Selesai'),
(2, 'ainy', 6, 1, 15000, 'Tunai', 'Lunas', 'Selesai'),
(3, 'dara', 3, 1, 13000, 'QRIS', 'Lunas', 'Selesai'),
(4, 'tri', 6, 2, 30000, 'QRIS', 'Belum Bayar', 'Selesai'),
(5, 'tri', 6, 2, 30000, 'Tunai', 'Lunas', 'Selesai'),
(6, 'zainal', 5, 1, 12000, 'QRIS', 'Lunas', 'Selesai'),
(7, 'tri', 4, 1, 5000, 'Tunai', 'Lunas', 'Selesai'),
(8, 'aa', 7, 1, 10000, 'QRIS', 'Lunas', 'Selesai'),
(9, 'aa', 6, 2, 30000, 'Tunai', 'Lunas', 'Selesai'),
(10, 'aura', 7, 3, 30000, 'QRIS', 'Lunas', 'Selesai'),
(11, 'arnof', 2, 3, 45000, 'QRIS', 'Lunas', 'Selesai'),
(12, 'fandi', 8, 1, 20000, 'QRIS', 'Lunas', 'Diproses'),
(13, 'aura', 6, 1, 15000, 'Tunai', 'Lunas', 'Diproses');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pesanan`
--
ALTER TABLE `pesanan`
  ADD PRIMARY KEY (`id`),
  ADD KEY `menu_id` (`menu_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `menu`
--
ALTER TABLE `menu`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
--
-- AUTO_INCREMENT for table `pesanan`
--
ALTER TABLE `pesanan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `pesanan`
--
ALTER TABLE `pesanan`
  ADD CONSTRAINT `pesanan_ibfk_1` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`id`) ON DELETE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
