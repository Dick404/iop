/*
Navicat MySQL Data Transfer

Source Server         : 10.110.20.20
Source Server Version : 50544
Source Host           : 10.110.20.20:3306
Source Database       : cloud_storage_swift

Target Server Type    : MYSQL
Target Server Version : 50544
File Encoding         : 65001

Date: 2016-04-18 11:12:33
*/
create database cloud_storage_swift;
use cloud_storage_swift;

SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
-- Table structure for `account`
-- ----------------------------
DROP TABLE IF EXISTS `account`;
CREATE TABLE `account` (
  `id` varchar(64) NOT NULL,
  `account_name` varchar(256) NOT NULL,
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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for `container`
-- ----------------------------
DROP TABLE IF EXISTS `container`;
CREATE TABLE `container` (
  `id` varchar(36) NOT NULL,
  `account_name` varchar(256) NOT NULL,
  `container_name` varchar(256) NOT NULL,
  `created_at` varchar(25) NOT NULL,
  `updated_at` varchar(25) NOT NULL,
  `is_deleted` char(1) NOT NULL DEFAULT '0',
  `deleted_at` varchar(25) DEFAULT NULL,
  `status` varchar(25) DEFAULT NULL,
  `status_changed_at` varchar(25) DEFAULT NULL,
  `object_count` int(9) NOT NULL,
  `bytes_used` bigint(18) NOT NULL,
  `metadata` varchar(4096) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for `object`
-- ----------------------------
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
  PRIMARY KEY (`id`),
  KEY `name_index` (`account_name`(40),`container_name`(30),`object_name`(128)) USING BTREE,
  KEY `md5_index` (`md5`,`file_hat_md5`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for `tokenv2`
-- ----------------------------
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
