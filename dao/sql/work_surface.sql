CREATE TABLE work_surface  (
    ID int NOT NULL AUTO_INCREMENT COMMENT '自增主键，唯一标识',
    WorkSurCode varchar(64) NOT NULL COMMENT '工作面代码，必须唯一',
    WorkSurName varchar(64) NOT NULL COMMENT '工作面名称',
    ProCode varchar(64) NOT NULL COMMENT '项目编号，外键',
    TunCode varchar(64) NOT NULL COMMENT '隧道编号，外键',
    StruCode varchar(64) NOT NULL COMMENT '结构物编号',
    Distance double NOT NULL COMMENT '工作面起点位置',
    PRIMARY KEY (ID) USING BTREE,
    FOREIGN KEY (ProCode) REFERENCES project (ProCode) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (TunCode) REFERENCES tunnel (TunCode) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE (WorkSurCode)
) COMMENT = '工作面表，存储工作面的基本信息，(WorkSurCode)唯一';