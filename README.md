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

20240104：  
变更如下  
变更breaking_result表id为自增  
```mysql
ALTER TABLE `breaking_result`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
```
数据基础工具：[database.py](database%2Fdatabase.py)新增批量处理逻辑；  
数据库操作方法：[other_data.py](database%2Fother_data.py)新增insert_breaking_results_batch数据批量插入函数；  
数据集合分割：[main.py](main.py)batchify函数，将一个大的数据集合分割成小的批次，便于批量处理；  
数据批量插入：[main.py](main.py)process_json_result函数，使用列表推导准备插入数据、数据插入。  
能够有效减少与数据库的通信次数，提升运算效率。

