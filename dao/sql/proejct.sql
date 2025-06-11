CREATE TABLE project
(
    ProID         int AUTO_INCREMENT COMMENT '自增主键，唯一标识',
    ProCode       VARCHAR(64)  NOT NULL COMMENT '项目编号，必须唯一',
    ProName       VARCHAR(64)  NOT NULL COMMENT '项目名称',
    ProAddress    VARCHAR(255) NOT NULL COMMENT '项目地址',
    LinkMan       VARCHAR(32)  NOT NULL COMMENT '联系人姓名',
    Phone         VARCHAR(11)  NOT NULL COMMENT '联系人电话',
    ProCreateTime DATETIME DEFAULT NULL COMMENT '项目创建时间，默认值为null',
    ProStatus     INT      DEFAULT 0 COMMENT '项目状态，0表示未开始，1表示进行中，2表示已完成',
    ProCycle      INT      NULL DEFAULT NULL COMMENT '项目周期/天',
    CompanyCode   VARCHAR(255) NOT NULL COMMENT '项目所属公司编号',
    PRIMARY KEY (ProID),
    FOREIGN KEY (CompanyCode) REFERENCES company (Code) ON UPDATE CASCADE ON DELETE CASCADE, -- company Code
    UNIQUE (ProCode)
) COMMENT ='项目表，存储项目的基本信息，(ProCode)唯一';