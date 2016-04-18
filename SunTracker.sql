-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb2+deb7u2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 18, 2016 at 04:12 PM
-- Server version: 5.5.47
-- PHP Version: 5.4.45-0+deb7u2

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `SunTracker`
--

-- --------------------------------------------------------

--
-- Table structure for table `SolarPowerData`
--

DROP TABLE IF EXISTS `SolarPowerData`;
CREATE TABLE IF NOT EXISTS `SolarPowerData` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deviceid` int(20) NOT NULL,
  `currentSteps` int(11) NOT NULL DEFAULT '0',
  `currentDegrees` float NOT NULL DEFAULT '0',
  `battery_load_voltage` float NOT NULL,
  `battery_current` float NOT NULL,
  `solarcell_load_voltage` float NOT NULL,
  `solarcell_current` float NOT NULL,
  `output_load_voltage` float NOT NULL,
  `output_current` float NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=12769 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
