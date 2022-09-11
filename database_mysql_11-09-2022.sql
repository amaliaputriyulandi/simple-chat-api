-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Sep 11, 2022 at 04:24 PM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 7.3.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `chat_rakamin`
--

-- --------------------------------------------------------

--
-- Table structure for table `chat`
--

CREATE TABLE `chat` (
  `id_chat` int(11) NOT NULL,
  `from_id_user` int(11) DEFAULT NULL,
  `to_id_user` int(11) DEFAULT NULL,
  `text` text NOT NULL,
  `is_group` int(11) NOT NULL DEFAULT 0 COMMENT '0 = bukan chat di group. 1 = iya',
  `id_group` int(11) DEFAULT NULL COMMENT 'Kalau is_group = 1 wajib isi',
  `datetime` datetime NOT NULL DEFAULT current_timestamp(),
  `is_read` int(11) NOT NULL DEFAULT 0 COMMENT '0 = belum di read. 1 = sudah di read',
  `is_delete` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `chat_reply`
--

CREATE TABLE `chat_reply` (
  `id_chat_reply` int(11) NOT NULL,
  `id_chat` int(11) NOT NULL,
  `from_id_user` int(11) NOT NULL,
  `text` text NOT NULL,
  `datetime` datetime NOT NULL DEFAULT current_timestamp(),
  `is_read` int(11) NOT NULL DEFAULT 0 COMMENT '0 = belum dibaca, 1 = sudah dibaca',
  `is_delete` int(11) NOT NULL DEFAULT 0 COMMENT '0 = belum dihapus, 1 = sudah dihapus'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `group_chat`
--

CREATE TABLE `group_chat` (
  `id_group` int(11) NOT NULL,
  `nama_group` varchar(30) NOT NULL,
  `is_delete` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `group_chat_member`
--

CREATE TABLE `group_chat_member` (
  `id_member` int(11) NOT NULL,
  `id_group` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `is_delete` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id_user` int(11) NOT NULL,
  `username` varchar(64) NOT NULL,
  `password` varchar(256) DEFAULT NULL,
  `no_hp` varchar(14) NOT NULL,
  `datetime` datetime NOT NULL DEFAULT current_timestamp(),
  `is_delete` int(11) NOT NULL DEFAULT 0 COMMENT '1 = sudah di delete, 0 = belum di delete'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `chat`
--
ALTER TABLE `chat`
  ADD PRIMARY KEY (`id_chat`),
  ADD KEY `id_user` (`from_id_user`),
  ADD KEY `id_group` (`id_group`),
  ADD KEY `to_id_user` (`to_id_user`),
  ADD KEY `id_group_2` (`id_group`);

--
-- Indexes for table `chat_reply`
--
ALTER TABLE `chat_reply`
  ADD PRIMARY KEY (`id_chat_reply`),
  ADD KEY `id_chat` (`id_chat`),
  ADD KEY `id_user` (`from_id_user`);

--
-- Indexes for table `group_chat`
--
ALTER TABLE `group_chat`
  ADD PRIMARY KEY (`id_group`);

--
-- Indexes for table `group_chat_member`
--
ALTER TABLE `group_chat_member`
  ADD PRIMARY KEY (`id_member`),
  ADD KEY `id_group` (`id_group`),
  ADD KEY `id_user` (`id_user`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `chat`
--
ALTER TABLE `chat`
  MODIFY `id_chat` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `chat_reply`
--
ALTER TABLE `chat_reply`
  MODIFY `id_chat_reply` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `group_chat`
--
ALTER TABLE `group_chat`
  MODIFY `id_group` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `group_chat_member`
--
ALTER TABLE `group_chat_member`
  MODIFY `id_member` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `chat`
--
ALTER TABLE `chat`
  ADD CONSTRAINT `chat_ibfk_1` FOREIGN KEY (`from_id_user`) REFERENCES `user` (`id_user`),
  ADD CONSTRAINT `chat_ibfk_2` FOREIGN KEY (`id_group`) REFERENCES `group_chat` (`id_group`),
  ADD CONSTRAINT `chat_ibfk_3` FOREIGN KEY (`to_id_user`) REFERENCES `user` (`id_user`);

--
-- Constraints for table `chat_reply`
--
ALTER TABLE `chat_reply`
  ADD CONSTRAINT `chat_reply_ibfk_1` FOREIGN KEY (`id_chat`) REFERENCES `chat` (`id_chat`),
  ADD CONSTRAINT `chat_reply_ibfk_2` FOREIGN KEY (`from_id_user`) REFERENCES `user` (`id_user`);

--
-- Constraints for table `group_chat_member`
--
ALTER TABLE `group_chat_member`
  ADD CONSTRAINT `group_chat_member_ibfk_1` FOREIGN KEY (`id_group`) REFERENCES `group_chat` (`id_group`),
  ADD CONSTRAINT `group_chat_member_ibfk_2` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
