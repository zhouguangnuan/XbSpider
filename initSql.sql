-- ҽԺ�б���Ϣ
CREATE TABLE `massage_hospital_procurement` (
  `id` varchar(50) NOT NULL COMMENT 'id',
  `title` varchar(200) NOT NULL COMMENT '����',
  `content` longtext NOT NULL COMMENT '����',
  `createTime` datetime DEFAULT NULL COMMENT '����ʱ��',
  `originalUrl` varchar(300) NOT NULL COMMENT 'ԭ�ĵ�ַ',
  `cityId` int(8) DEFAULT NULL COMMENT '����ID',
  `cityName` varchar(10) DEFAULT NULL COMMENT '��������',
  `hospitalId` int(11) DEFAULT NULL COMMENT 'ҽԺID',
  `hospitalName` varchar(50) DEFAULT NULL COMMENT 'ҽԺ����',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '֪ͨ״̬��0��δ֪ͨ��1����֪ͨ',
  `type` tinyint(4) NOT NULL DEFAULT '1' COMMENT '�б����ͣ�1��������2������',
  PRIMARY KEY (`id`),
  KEY `idx_cityId_hospitalId_createTime` (`cityId`,`hospitalId`,`createTime`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;