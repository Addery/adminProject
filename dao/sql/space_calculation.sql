DROP TABLE IF EXISTS space_calculation;

CREATE TABLE space_calculation
(
    ID int AUTO_INCREMENT COMMENT '自增主键，唯一标识',
    CalculationUUID VARCHAR(255) NOT NULL COMMENT '净空计算uuid，外键',
    RegionPath VARCHAR(255) NOT NULL COMMENT '断面区域路径，存储断面前端数据及计算结果',
    Size int NOT NULL COMMENT '断面区域大小',
    CalculationTime DATETIME NOT NULL COMMENT '上次计算时间',
    PRIMARY KEY (ID),
    UNIQUE (CalculationUUID),
    FOREIGN KEY (CalculationUUID) REFERENCES pcd_log (CalculationUUID) ON DELETE CASCADE ON UPDATE CASCADE
) COMMENT ='净空计算结果表，记录每次净空计算的结果';