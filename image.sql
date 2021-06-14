CREATE TABLE `t_image` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `fid` varchar(8) NOT NULL COMMENT '分类ID',
  `cat_first_url` varchar(128) NOT NULL COMMENT '分类第一页',
  `cat_title` varchar(256) NOT NULL COMMENT '分类标题',
  `depth` INT NOT NULL COMMENT 'URL深度',
  `download_timeout` FLOAT NOT NULL COMMENT '下载时间',
  `download_slot` varchar(128) NOT NULL COMMENT 'download_slot',
  `download_latency` FLOAT DEFAULT NULL COMMENT 'download_latency',
  `max_page` INT DEFAULT NULL COMMENT '最大页数',
  `title` varchar(256) DEFAULT NULL COMMENT '标题',
  `photo_url` TEXT DEFAULT NULL COMMENT '图片地址',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='图片库';

