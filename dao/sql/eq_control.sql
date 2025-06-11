CREATE TABLE eq_control  (
  ID int NOT NULL AUTO_INCREMENT COMMENT '自增主键，唯一标识',
  ConEquipCode varchar(64) NOT NULL COMMENT '中控设备编号，必须唯一',
  ConEquipName varchar(64) NOT NULL COMMENT '中控设备名称',
  ConEquipIP varchar(20) NOT NULL COMMENT '中控设备ip地址',
  ProCode varchar(64) NOT NULL COMMENT '项目编号，外键',
  TunCode varchar(64) NOT NULL COMMENT '隧道编号，外键',
  WorkSurCode varchar(64) NOT NULL COMMENT '工作面编号，外键',
  StruCode varchar(64) NOT NULL COMMENT '结构物编号',
  ConStatus int NOT NULL COMMENT '0表示离线，1表示在线，2表示故障',
  Init int NOT NULL COMMENT '0表示未初始化，1表示已初始化',
  PRIMARY KEY (ID) USING BTREE,
  UNIQUE (ConEquipCode),
  FOREIGN KEY (ProCode) REFERENCES project (ProCode) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (TunCode) REFERENCES tunnel (TunCode) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (WorkSurCode) REFERENCES work_surface (WorkSurCode) ON DELETE CASCADE ON UPDATE CASCADE
) COMMENT = '中控设备表，存储中控设备的基本信息，ConEquipCode唯一';