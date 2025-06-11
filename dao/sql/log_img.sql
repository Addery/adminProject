CREATE TABLE anomaly_log_img
(
    ID     int AUTO_INCREMENT COMMENT '自增主键，唯一标识',
    Identification   VARCHAR(255)  NOT NULL COMMENT '日志信息标识，外键',
    AviaPicturePath VARCHAR(255) NOT NULL COMMENT '雷达影像地址',
    CameraPicturePath   VARCHAR(255)  NOT NULL COMMENT '相机影像地址',
    PRIMARY KEY (ID),
    FOREIGN KEY (Identification) REFERENCES anomaly_log (Identification) ON UPDATE CASCADE ON DELETE CASCADE -- anomaly_log Identification
) COMMENT ='日志记录图像数据表';