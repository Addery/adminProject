CREATE TABLE eq_data  (
  ID int NOT NULL AUTO_INCREMENT COMMENT '自增主键，唯一标识',
  DataAcqEquipCode varchar(64) NOT NULL COMMENT '采集器设备编号，必须唯一',
  DataAcqEquipName varchar(64) NOT NULL COMMENT '采集器设备名称',
  DataAcqEquipIP varchar(20) NOT NULL COMMENT '采集器设备ip地址',
  DataAcqEquipInterval int NOT NULL COMMENT '数据采集时间间隔',
  Distance float NULL DEFAULT 0 COMMENT '采集器所处里程',
  DataAcaEquipStatus int NULL DEFAULT 0 COMMENT '采集器设备状态，0表示关闭，1表示开启，2表示损坏',
  ConEquipCode varchar(128) NOT NULL COMMENT '中控设备编号，外键',
  Init int NULL DEFAULT NULL COMMENT '0表示未初始化，1表示已初始化',
  PRIMARY KEY (ID),
  UNIQUE INDEX (DataAcqEquipCode),
  FOREIGN KEY (ConEquipCode) REFERENCES eq_control (ConEquipCode) ON DELETE CASCADE ON UPDATE CASCADE
) COMMENT = '数据采集设备表，存储数据采集设备的基本信息，DataAcqEquipCode唯一';