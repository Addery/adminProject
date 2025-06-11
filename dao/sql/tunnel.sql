CREATE TABLE `tunnel`  (
  ID int NOT NULL AUTO_INCREMENT COMMENT '自增主键，唯一标识',
  TunCode varchar(64) NOT NULL COMMENT '隧道编号，必须唯一',
  TunName varchar(64) NOT NULL COMMENT '隧道名称',
  LinkMan varchar(64) NOT NULL COMMENT '联系人姓名',
  Phone varchar(11) NOT NULL COMMENT '联系人电话',
  High varchar(16) NOT NULL COMMENT '隧道高度',
  TunStatus int NOT NULL DEFAULT 0 COMMENT '隧道状态，0表示未开始，1表示进行中，2表示已完成',
  ProCode varchar(128) NOT NULL COMMENT '项目编号，外键',
  TunCycle int NOT NULL COMMENT '工期',
  TunCreateTime datetime NOT NULL COMMENT '隧道创建时间',
  Length double NOT NULL COMMENT '隧道总长度',
  CurAdvancement double NULL DEFAULT NULL COMMENT '当前掘进',
  PRIMARY KEY (ID),
  UNIQUE (TunCode),
  FOREIGN KEY (ProCode) REFERENCES project (ProCode) ON DELETE CASCADE ON UPDATE CASCADE
) COMMENT = '隧道表，存储隧道的基本信息，(TunCode)唯一';