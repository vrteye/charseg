# 使用指南

### 安装项目包
`pip install -r requirements.txt`


### 查看参数含义
`python main.py -h`


### 使用示例
覆盖同名文件（仅覆盖输出的txt文件）  
python main.py input.txt 1.txt yes

不覆盖同名文件  
python main.py input.txt 1.txt no 

### 数据库配置
configs文件下config.py中配置自己的数据库信息  


### 数据表创建
拆字json表：  
```mysql
CREATE TABLE `teardown_json` (
  `id` bigint(20) NOT NULL,
  `file_name` varchar(50) DEFAULT NULL COMMENT '文件名',
  `json_result` json DEFAULT NULL COMMENT 'json结果',
  `processing_time` datetime DEFAULT NULL COMMENT '数据处理时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```


拆字结果表：
```mysql
CREATE TABLE `breaking_result` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `file_name` varchar(100) DEFAULT NULL COMMENT '文件名',
  `paragraph_no` int(10) DEFAULT NULL COMMENT '段落号',
  `sentence_no` int(10) DEFAULT NULL COMMENT '句子号',
  `dismantling_record_no` int(11) DEFAULT NULL COMMENT '拆字号',
  `teardown_character` longtext COMMENT '拆字字符',
  `teardown_json_id` bigint(20) DEFAULT NULL COMMENT '拆字json表id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

20231220：新增PDF文档解析，段落还原方法。
