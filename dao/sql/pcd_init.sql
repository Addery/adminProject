DROP TABLE IF EXISTS pcd_init;

CREATE TABLE pcd_init
(
    ID     int AUTO_INCREMENT COMMENT '自增主键，唯一标识',
    ConEquipCode   VARCHAR(255)  NOT NULL COMMENT '总控设备编号，外键',
    InitPCDPath VARCHAR(255) NOT NULL COMMENT '初始化数据路径',
    InitRegionPath   VARCHAR(255)  NOT NULL COMMENT '初始化预处理后的的区域数据路径',
    PRIMARY KEY (ID),
    FOREIGN KEY (ConEquipCode) REFERENCES eq_control (ConEquipCode) ON UPDATE CASCADE ON DELETE CASCADE -- eq_control ConEquipCode
) COMMENT ='初始化信息表';