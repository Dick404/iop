/*
SQLyog Ultimate v9.63 
MySQL - 5.5.8-mycat-1.5-RELEASE-20160301083012 : Database - iop_dev_monitor
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`iop_dev_monitor` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `iop_dev_monitor`;

/*Table structure for table `mon_statistic_day` */

DROP TABLE IF EXISTS `mon_statistic_day`;

CREATE TABLE `mon_statistic_day` (
  `id` varchar(36) NOT NULL,
  `resource_id` varchar(36) DEFAULT NULL,
  `meter_id` varchar(36) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `meter_volume` float DEFAULT NULL,
  `virtual_env_id` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `res_id_meter_id_day_ctime` (`resource_id`,`meter_id`,`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='ÿ��900sͳ��һ��';

/*Table structure for table `mon_statistic_hours` */

DROP TABLE IF EXISTS `mon_statistic_hours`;

CREATE TABLE `mon_statistic_hours` (
  `id` varchar(36) NOT NULL,
  `resource_id` varchar(36) DEFAULT NULL,
  `meter_id` varchar(36) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `meter_volume` float DEFAULT NULL,
  `virtual_env_id` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `res_id_meter_id_hour_ctime` (`resource_id`,`meter_id`,`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='\r\n300';

/*Table structure for table `mon_statistic_month` */

DROP TABLE IF EXISTS `mon_statistic_month`;

CREATE TABLE `mon_statistic_month` (
  `id` varchar(36) NOT NULL,
  `resource_id` varchar(36) DEFAULT NULL,
  `meter_id` varchar(36) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `meter_volume` float DEFAULT NULL,
  `virtual_env_id` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `res_id_meter_id_month_ctime` (`resource_id`,`meter_id`,`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='ÿ��21600sͳ��\r\n';

/*Table structure for table `mon_statistic_week` */

DROP TABLE IF EXISTS `mon_statistic_week`;

CREATE TABLE `mon_statistic_week` (
  `id` varchar(36) NOT NULL,
  `resource_id` varchar(36) DEFAULT NULL,
  `meter_id` varchar(36) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `meter_volume` float DEFAULT NULL,
  `virtual_env_id` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `res_id_meter_id_week_ctime` (`resource_id`,`meter_id`,`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='ÿ��3600s����ͳ��\r\n';

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
