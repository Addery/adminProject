DROP TABLE IF EXISTS pcd_log;


CREATE TABLE pcd_log
(
    ID               int AUTO_INCREMENT COMMENT '自增主键',
    ProCode          VARCHAR(64)  NOT NULL COMMENT '项目编号',
    TunCode          VARCHAR(64)  NOT NULL COMMENT '隧道编号',
    WorkSurCode      VARCHAR(64)  NOT NULL COMMENT '工作面编号',
    StruCode         VARCHAR(64)  NOT NULL COMMENT '结构物编号',
    Mileage          VARCHAR(64)  NOT NULL COMMENT '里程',
    ConEquipCode     VARCHAR(64)  NOT NULL COMMENT '中控设备编号',
    DataAcqEquipCode VARCHAR(64)  NOT NULL COMMENT '采集器设备编号',
    AnomalyTime      DATETIME     NOT NULL COMMENT 'pcd采集时间',
    Year             int          NOT NULL COMMENT 'pcd采集时间-年',
    Month            int          NOT NULL COMMENT 'pcd采集时间-月',
    Day              int          NOT NULL COMMENT 'pcd采集时间-日',
    Hour             int          NOT NULL COMMENT 'pcd采集时间-时',
    Minute           int          NOT NULL COMMENT 'pcd采集时间-分',
    Second           int          NOT NULL COMMENT 'pcd采集时间-秒',
    Path VARCHAR(128) DEFAULT NULL COMMENT 'pcd文件路径',
    PRIMARY KEY (ID)
) COMMENT ='pcd文件路径记录表';