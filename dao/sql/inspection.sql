DROP DATABASE IF EXISTS inspection;

CREATE DATABASE inspection;

USE inspection;

CREATE TABLE inspections
(
    ID              INT AUTO_INCREMENT COMMENT '自增主键，唯一标识',
    StartTime       DATETIME NOT NULL COMMENT '开始时间',
    EndTime         DATETIME     DEFAULT NULL COMMENT '结束时间',
    Duration        DATETIME     DEFAULT NULL COMMENT '时长',
    WidthSection    INT      NOT NULL COMMENT '幅面,  0-左、1-右、2-双',
    lane            INT      NOT NULL COMMENT '车道,  0-应急车道、1-1、2-2、3-3',
    reportPath      VARCHAR(255) DEFAULT NULL COMMENT '报告路径',
    inspectionsType INT          DEFAULT NULL COMMENT '巡检类型, 0-巡检、1-复检',
    Status          INT          DEFAULT 0 COMMENT '巡检状态， 0-巡检中、1-巡检结束/报告生成中、2-报告已生成',
    PRIMARY KEY (ID)
) COMMENT ='巡检表';

CREATE TABLE defects
(
    ID           INT AUTO_INCREMENT COMMENT '自增主键，唯一标识',
    inspectionID INT          NOT NULL COMMENT 'inspections ID 外键，同步更新删除',
    defectType   INT          NOT NULL COMMENT '病害类型: 1-缝、2-坑、3-标志线模糊',
    defectLevel  INT          NOT NULL COMMENT '病害等级',
    location     VARCHAR(255) NOT NULL COMMENT 'GPS定位信息',
    timestamp    VARCHAR(255) NOT NULL COMMENT '病害发生时间',
    cameraPath   VARCHAR(255) NOT NULL COMMENT '相机影像地址',
    cameraBbox   VARCHAR(255) NOT NULL COMMENT '病害锚框',
    mileage      VARCHAR(255) NOT NULL COMMENT '里程',
    PRIMARY KEY (ID),
    FOREIGN KEY (inspectionID) REFERENCES inspections (ID) ON DELETE CASCADE ON UPDATE CASCADE
) COMMENT ='病害表，存储巡检过程中发现的病害信息，inspectionID 外键，同步更新删除';