-- 医院招标信息
CREATE TABLE `massage_hospital_procurement` (
  `id` varchar(50) NOT NULL COMMENT 'id',
  `title` varchar(200) NOT NULL COMMENT '标题',
  `content` longtext NOT NULL COMMENT '内容',
  `createTime` datetime DEFAULT NULL COMMENT '发布时间',
  `originalUrl` varchar(300) NOT NULL COMMENT '原文地址',
  `cityId` int(8) DEFAULT NULL COMMENT '城市ID',
  `cityName` varchar(10) DEFAULT NULL COMMENT '城市名称',
  `hospitalId` int(11) DEFAULT NULL COMMENT '医院ID',
  `hospitalName` varchar(50) DEFAULT NULL COMMENT '医院名称',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '通知状态：0：未通知，1：已通知',
  `type` tinyint(4) NOT NULL DEFAULT '1' COMMENT '招标类型：1：其它，2：护工',
  PRIMARY KEY (`id`),
  KEY `idx_cityId_hospitalId_createTime` (`cityId`,`hospitalId`,`createTime`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;