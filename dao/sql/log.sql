# DROP TABLE IF EXISTS anomaly_log;

# DROP TABLE IF EXISTS anomaly_log_desc;

CREATE TABLE anomaly_log
(
    ID               int AUTO_INCREMENT COMMENT '自增主键',
    Identification   VARCHAR(255) NOT NULL COMMENT '详细信息标识，外键',
    ProCode          VARCHAR(64)  NOT NULL COMMENT '项目编号',
    TunCode          VARCHAR(64)  NOT NULL COMMENT '隧道编号',
    WorkSurCode      VARCHAR(64)  NOT NULL COMMENT '工作面编号',
    StruCode         VARCHAR(64)  NOT NULL COMMENT '结构物编号',
    Mileage          VARCHAR(64)  NOT NULL COMMENT '里程',
    ConEquipCode     VARCHAR(64)  NOT NULL COMMENT '中控设备编号',
    DataAcqEquipCode VARCHAR(64)  NOT NULL COMMENT '采集器设备编号',
    AnomalyTime      DATETIME     NOT NULL COMMENT '异常发生时间',
    Year             int          NOT NULL COMMENT '异常发生时间-年',
    Month            int          NOT NULL COMMENT '异常发生时间-月',
    Day              int          NOT NULL COMMENT '异常发生时间-日',
    Hour             int          NOT NULL COMMENT '异常发生时间-时',
    Minute           int          NOT NULL COMMENT '异常发生时间-分',
    Second           int          NOT NULL COMMENT '异常发生时间-秒',
    PRIMARY KEY (ID),
    UNIQUE (Identification)
) COMMENT ='预警信息记录表';


CREATE TABLE anomaly_log_desc
(
    ID             int AUTO_INCREMENT COMMENT '自增主键',
#     DescCode       VARCHAR(255) NOT NULL COMMENT '详细信息编号',
    Identification VARCHAR(255) NOT NULL COMMENT '标识',
    Degree         VARCHAR(32)  NOT NULL COMMENT '异常等级',
    Region         VARCHAR(64)  NOT NULL COMMENT '异常区域索引',
    Position       VARCHAR(64)  NOT NULL COMMENT '异常区域位置',
    Bas            VARCHAR(128) NOT NULL COMMENT '异常区域偏移量',
    PRIMARY KEY (ID),
    FOREIGN KEY (Identification) REFERENCES anomaly_log (Identification) ON UPDATE CASCADE ON DELETE CASCADE, -- anomaly_log Identification
#     UNIQUE (DescCode),
    INDEX (Identification) -- 添加索引
) COMMENT ='预警信息详情表';



