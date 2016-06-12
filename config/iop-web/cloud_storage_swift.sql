/*
SQLyog Ultimate v9.63 
MySQL - 5.5.43-MariaDB-wsrep-log : Database - cloud_storage_swift
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`cloud_storage_swift` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `cloud_storage_swift`;

/*Table structure for table `account` */

DROP TABLE IF EXISTS `account`;

CREATE TABLE `account` (
  `id` varchar(64) NOT NULL,
  `account_name` varchar(100) NOT NULL,
  `created_at` varchar(25) NOT NULL,
  `updated_at` varchar(25) NOT NULL,
  `is_deleted` char(1) NOT NULL,
  `deleted_at` varchar(25) DEFAULT NULL,
  `status` varchar(25) DEFAULT NULL,
  `status_changed_at` varchar(25) DEFAULT NULL,
  `container_count` int(9) NOT NULL COMMENT 'int  -2147483648 to 2147483647',
  `object_count` int(9) NOT NULL COMMENT 'int  -2147483648 to 2147483647',
  `bytes_used` bigint(18) NOT NULL COMMENT 'long/bigint -9223372036854775808 to 9223372036854775807',
  `metadata` varchar(4096) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_unique` (`account_name`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `account` */

insert  into `account`(`id`,`account_name`,`created_at`,`updated_at`,`is_deleted`,`deleted_at`,`status`,`status_changed_at`,`container_count`,`object_count`,`bytes_used`,`metadata`) values ('04a75f41a20444608237f7a7bc12e194','AUTH_08668b4e79554e95bd02d551f8c1c55f','1460530161.983','1464078204.118','0',NULL,NULL,NULL,1,129,16523139104,'{\"x-account-meta-quota-bytes\":[\"644245094400\",\"1460530165.053\"]}'),('3d030bb11c984eb880e3f53daaa971d0','AUTH_26016ff86200496085ce380137299fa6','1464075911.770','1464076810.575','0',NULL,NULL,NULL,2,1,14,'{\"x-account-meta-quota-bytes\":[\"10737418240\",\"1464075911.771\"]}');

/*Table structure for table `container` */

DROP TABLE IF EXISTS `container`;

CREATE TABLE `container` (
  `id` varchar(36) NOT NULL,
  `account_name` varchar(100) NOT NULL,
  `container_name` varchar(100) NOT NULL,
  `created_at` varchar(25) NOT NULL,
  `updated_at` varchar(25) NOT NULL,
  `is_deleted` char(1) NOT NULL DEFAULT '0',
  `deleted_at` varchar(25) DEFAULT NULL,
  `status` varchar(25) DEFAULT NULL,
  `status_changed_at` varchar(25) DEFAULT NULL,
  `object_count` int(9) NOT NULL,
  `bytes_used` bigint(18) NOT NULL,
  `metadata` varchar(4096) DEFAULT NULL,
  `storage_policy_index` tinyint(3) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_container_unique` (`account_name`,`container_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `container` */

insert  into `container`(`id`,`account_name`,`container_name`,`created_at`,`updated_at`,`is_deleted`,`deleted_at`,`status`,`status_changed_at`,`object_count`,`bytes_used`,`metadata`,`storage_policy_index`) values ('0013e0b4874248a0a6b3eb2a836175a8','AUTH_08668b4e79554e95bd02d551f8c1c55f','swiftStoreTestContainer','1463033781.393','1464078204.115','0',NULL,NULL,NULL,111,13083632900,'{\"x-container-read\":[\".r:*\",\"1463380509.916\"]}',1),('0acaf0fac42c4aa09a80cc3665a6e950','AUTH_26016ff86200496085ce380137299fa6','test2','1460443728.331','1461844834.434','0',NULL,NULL,NULL,1,14,NULL,1),('e6cf2ea3a25e4cb2b7ea5a9b82169243','AUTH_26016ff86200496085ce380137299fa6','swiftStoreTestContainer','1464076810.571','1464076810.640','0',NULL,NULL,NULL,0,0,'{\"x-container-read\":[\".r:*\",\"1464076810.619\"]}',1),('lyx13e0b4874248a0a6b3eb2a83617lyx','AUTH_08668b4e79554e95bd02d551f8c1c55f','servicePackages','1463033781.393','1464316421.140','0',NULL,NULL,NULL,129,16523139104,'{\"x-container-read\":[\".r:*\",\"1463380509.916\"]}',1),('qqq13e0b4874248a0a6b3eb2a83617qqq','AUTH_08668b4e79554e95bd02d551f8c1c55f','RdsBackup','1463033781.393','1464078204.115','0',NULL,NULL,NULL,111,13083632900,'{\"x-container-read\":[\".r:*\",\"1463380509.916\"]}',1);

/*Table structure for table `object` */

DROP TABLE IF EXISTS `object`;

CREATE TABLE `object` (
  `id` varchar(36) NOT NULL,
  `account_name` varchar(256) NOT NULL,
  `container_name` varchar(256) NOT NULL,
  `object_name` varchar(1024) NOT NULL COMMENT 'linux max file path length: 4096',
  `created_at` varchar(25) NOT NULL,
  `updated_at` varchar(25) NOT NULL,
  `status` varchar(25) DEFAULT NULL,
  `size` bigint(18) NOT NULL,
  `content_type` varchar(255) NOT NULL,
  `md5` varchar(64) NOT NULL,
  `storage_name` varchar(25) DEFAULT NULL,
  `relative_path` varchar(95) DEFAULT NULL,
  `is_deleted` char(1) NOT NULL DEFAULT '0',
  `deleted_at` varchar(25) DEFAULT NULL,
  `metadata` varchar(4096) DEFAULT NULL,
  `file_hat_md5` varchar(64) DEFAULT NULL,
  `unique_hash` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `name_index` (`account_name`(40),`container_name`(30),`object_name`(128)) USING BTREE,
  KEY `md5_index` (`md5`,`file_hat_md5`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `object` */

insert  into `object`(`id`,`account_name`,`container_name`,`object_name`,`created_at`,`updated_at`,`status`,`size`,`content_type`,`md5`,`storage_name`,`relative_path`,`is_deleted`,`deleted_at`,`metadata`,`file_hat_md5`,`unique_hash`) values ('1c89bcb4e5344f6285a63e1283cf3f7d','AUTH_08668b4e79554e95bd02d551f8c1c55f','servicePackages','RabbitMQ','1464316284.550','1464316284.551','created',23262829,'application/octet-stream','c4924172cc5f5fd5ee0209417e6a23af','file','941/70e/e17fa88877ac47ff9cec391b23a8a4e2','0',NULL,'{\"x-object-meta-mtime\":[\"1464256331.000000\",\"1464316284.551\"]}','f32ac2282281ccdf879b9b5a1f8dc3ea','94170e1182571260d7496c13ce257ca1'),('22e1eb752a034c80bb983b7dfb488822','AUTH_08668b4e79554e95bd02d551f8c1c55f','servicePackages','Solr','1464316289.392','1464316289.393','created',198218849,'application/octet-stream','6c219cfea8559400dc7db9b2afac8a29','file','789/d11/2bc1e60567c9445cacde30cbca1eeb06','0',NULL,'{\"x-object-meta-mtime\":[\"1464256931.000000\",\"1464316289.392\"]}','864bca710d1b6e8a94951ffd26238a26','789d11224a4e1f5bd23ef6f17e953c50'),('2c99c988cbe946fe9c865159f9fb3edc','AUTH_08668b4e79554e95bd02d551f8c1c55f','servicePackages','EMR','1464316266.807','1464316266.808','created',148560106,'application/octet-stream','e44931cede827a5bba2f0f268bd5c9b0','file','515/c02/bf9fd8b1ba75445db5ab53383eced543','0',NULL,'{\"x-object-meta-mtime\":[\"1464256664.000000\",\"1464316266.807\"]}','0d8c1b8741d6f04aa0c595a0a7c02f03','515c02ee8d5cb8d4a66edf98739ee401'),('3650fa11fa354ec38e5f332975be62e4','AUTH_08668b4e79554e95bd02d551f8c1c55f','servicePackages','Storm','1464316298.889','1464316298.889','created',313162196,'application/octet-stream','678bf16cb5a0c0e5b5a9b5ab260ed676','file','adb/c4a/ef95b3fc2db24c9cb3304a04a393990c','0',NULL,'{\"x-object-meta-mtime\":[\"1464257150.000000\",\"1464316298.889\"]}','0a5356f74297badeac90b9907a99aad9','adbc4a46e562d0719ee3b97cefc1e6fc'),('377862b8025748418d3b706d2661457f','AUTH_08668b4e79554e95bd02d551f8c1c55f','servicePackages','TomcatCluster','1464316303.979','1464316303.980','created',152791821,'application/octet-stream','0505fe16111b225f6dbd4c19cb1e18d0','file','539/ada/606908c1dc2d4e9689a787fa8a114ec6','0',NULL,'{\"x-object-meta-mtime\":[\"1464256485.000000\",\"1464316303.979\"]}','a7c2df3fbba25a820c9bf007aefac6b5','539ada54a739066977dee8a710b26d27'),('45b567b2e9d74f9196f3e723496ad175','AUTH_08668b4e79554e95bd02d551f8c1c55f','servicePackages','MariaDBCluster','1464316281.875','1464316281.876','created',252109059,'application/octet-stream','0c6bbb9ab1797d343d99db36569a016e','file','058/3f8/2cbc334bb0b84cc2bfd14f9514c74cb2','0',NULL,'{\"x-object-meta-mtime\":[\"1464258990.000000\",\"1464316281.875\"]}','6249a5f0683b62cf973aeee64032f72c','0583f89858eee023e52848aab959d9a9'),('62ed4609f5044114bc1e6c51966ce7d5','AUTH_08668b4e79554e95bd02d551f8c1c55f','servicePackages','Haproxy','1464316267.684','1464316267.685','created',2519996,'application/octet-stream','bc7537b41e8a1eb660bd5004a87b28c5','file','a3a/94b/635bdb531124458a8c4a917e8c3e37b9','0',NULL,'{\"x-object-meta-mtime\":[\"1464255227.000000\",\"1464316267.684\"]}','2e47bdc72046dc37ff83b932276224f9','a3a94bfd83006f6dce61b41ff9a123f1'),('7556bb5ec7d24bdd9f87cf6b7c96d1de','AUTH_08668b4e79554e95bd02d551f8c1c55f','servicePackages','tpl.centos7.v1.0.zip','1464316438.686','1464316438.687','created',471371776,'application/octet-stream','3580a305dc6a6041ca85468dbb9c26e0','file','877/954/d41737656a4944afbfb7066f438a50de','0',NULL,'{\"x-object-meta-mtime\":[\"1464258644.171223\",\"1464316438.686\"]}','ef652d6e77737ee4fb8686f2d785da1b','877954e8faffbd57716e3cac80e65cd6'),('a25856c733bd4833a819d68018f66821','AUTH_08668b4e79554e95bd02d551f8c1c55f','servicePackages','iop_image_tpl.centos6.7.v1.0.zip','1464316420.283','1464316420.283','created',403801160,'application/octet-stream','820ee17f557bfb918dfc54fa0439dad9','file','24d/63f/e01ab09737fe4203a933177988cbc19d','0',NULL,'{\"x-object-meta-mtime\":[\"1464258645.430223\",\"1464316420.283\"]}','059c84960f3927808fd13dd78491e4a2','24d63fd891ad1e8b78fb9994eb002e14'),('ab1155e687944ec4bfef09d6d6dacb0c','AUTH_08668b4e79554e95bd02d551f8c1c55f','servicePackages','Hbase','1464316270.310','1464316270.310','created',148560106,'application/octet-stream','e44931cede827a5bba2f0f268bd5c9b0','file','515/c02/bf9fd8b1ba75445db5ab53383eced543','0',NULL,'{\"x-object-meta-mtime\":[\"1464256480.000000\",\"1464316270.310\"]}','0d8c1b8741d6f04aa0c595a0a7c02f03','6b217c45891b0a3ccdfdf13ffbfa0797'),('b9b196ab8592496f864d1bf1ae3654ef','AUTH_08668b4e79554e95bd02d551f8c1c55f','servicePackages','kafka','1464316275.419','1464316275.420','created',229825623,'application/octet-stream','0bd928adf522c1f7865c2f02972a386a','file','37d/d3a/97c20b0257a84ffebffcff959621bd1b','0',NULL,'{\"x-object-meta-mtime\":[\"1464263648.000000\",\"1464316275.420\"]}','c40cb5d159189afe38bb3aee040809b7','37dd3a20b74630ecaef907cd147f7cbe'),('c474044405004420a2dd062f59e1d434','AUTH_08668b4e79554e95bd02d551f8c1c55f','servicePackages','centos7-cloudAgent-python-v1.0.qcow2','1464316396.196','1464316396.197','created',656408576,'application/octet-stream','c2444e339f0285e1456a1abec8b3f6ff','file','920/a9e/454b8bf366b548eab4dd9b0bb39352e8','0',NULL,'{\"x-object-meta-mtime\":[\"1464258734.217223\",\"1464316396.196\"]}','2b260af7a8ded3a6dce18dc38e365300','920a9ec35107d1947747c57cf325d0cc'),('c5c1f57e098c4b63aa2dacd2623e877f','AUTH_08668b4e79554e95bd02d551f8c1c55f','servicePackages','postgresql','1464316283.858','1464316283.858','created',25320324,'application/octet-stream','8f991d5ed8f7d8c6a5f9c17f5bb82ca2','file','b01/934/71a6a73a305d4fc487aa80d2d63f9db7','0',NULL,'{\"x-object-meta-mtime\":[\"1464256301.000000\",\"1464316283.858\"]}','ee09946a8c8b9c12ea304a465e6f81d1','b0193446eb62707205cff23a9b249d1a'),('d5cc26a4ad464a78974457a8f6dba3eb','AUTH_08668b4e79554e95bd02d551f8c1c55f','servicePackages','Redis','1464316284.958','1464316284.959','created',6708327,'application/octet-stream','b6e839eaefcad408ec28d4adf2f707b6','file','6cf/3c0/8381634260d946a88f9e14c0114a22ee','0',NULL,'{\"x-object-meta-mtime\":[\"1464256571.000000\",\"1464316284.958\"]}','25c12fdc69e308a48b1aeb4dc594a5fe','6cf3c0cd528c0bb38a537225955ec905'),('e2997368ed98417392479800d877cd09','AUTH_08668b4e79554e95bd02d551f8c1c55f','servicePackages','ApachePhp','1464316264.059','1464316264.059','created',9208904,'application/octet-stream','62baeb101c01e730b595f7ea7874c4f5','file','b18/0b6/abc9df17db15483d8d3a5d8d3090d089','0',NULL,'{\"x-object-meta-mtime\":[\"1464258718.000000\",\"1464316264.059\"]}','ce9e70a7f9cdc96c557d23521bf9bd60','b180b674d8fe79b5ecf6a137aa27d0b9'),('e7460e41a9b44472a16d37e38b96c8e7','AUTH_08668b4e79554e95bd02d551f8c1c55f','servicePackages','centos6.7-cloudAgent-python-v1.0.qcow2','1464316375.214','1464316375.215','created',397676544,'application/octet-stream','12247b2ece7eee95c8915c842bfaed74','file','5af/01f/a00cb70ea3324acca154870bab9ee147','0',NULL,'{\"x-object-meta-mtime\":[\"1464258711.619223\",\"1464316375.214\"]}','2b260af7a8ded3a6dce18dc38e365300','5af01fcc7cc95874f1bbc2f0207ba858');

/*Table structure for table `storage` */

DROP TABLE IF EXISTS `storage`;

CREATE TABLE `storage` (
  `id` varchar(64) NOT NULL,
  `name` varchar(40) NOT NULL,
  `policy_index` smallint(3) NOT NULL,
  `root_path` varchar(1024) DEFAULT NULL,
  `writeable` char(1) DEFAULT NULL,
  `driver_name` varchar(50) DEFAULT NULL,
  `use_percentage_limit` int(3) DEFAULT NULL,
  `left_capacity_limit` int(4) DEFAULT NULL,
  `reserved` varchar(1024) DEFAULT NULL,
  `remark` varchar(1024) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `storage` */

insert  into `storage`(`id`,`name`,`policy_index`,`root_path`,`writeable`,`driver_name`,`use_percentage_limit`,`left_capacity_limit`,`reserved`,`remark`) values ('hsfksfusodfmskldfijsdf','file',1,'/storage','1','LocalStore',90,10,NULL,NULL);

/*Table structure for table `storage_policy` */

DROP TABLE IF EXISTS `storage_policy`;

CREATE TABLE `storage_policy` (
  `id` varchar(64) NOT NULL,
  `policy_index` smallint(3) NOT NULL,
  `name` varchar(120) CHARACTER SET utf8 NOT NULL,
  `is_default` char(1) DEFAULT '0',
  `remark` varchar(1024) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_index` (`policy_index`),
  UNIQUE KEY `unique_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `storage_policy` */

insert  into `storage_policy`(`id`,`policy_index`,`name`,`is_default`,`remark`) values ('shdfskfuskdjfskdfjskdfj',1,'local-file','0',NULL);

/*Table structure for table `tokenv2` */

DROP TABLE IF EXISTS `tokenv2`;

CREATE TABLE `tokenv2` (
  `id` varchar(36) NOT NULL,
  `token_id` varchar(32) NOT NULL,
  `tenant_id` varchar(32) NOT NULL,
  `tenant_name` varchar(64) NOT NULL,
  `user_id` varchar(32) NOT NULL,
  `user_name` varchar(64) NOT NULL,
  `user_roles` varchar(255) NOT NULL,
  `issued_at` varchar(40) NOT NULL,
  `expires` varchar(40) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `tokenv2` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
