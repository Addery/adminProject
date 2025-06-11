CREATE TABLE company
(
    ID     int AUTO_INCREMENT COMMENT '自增主键，唯一标识',
    Code   VARCHAR(255)  NOT NULL COMMENT '所属公司编号，外键',
    Name VARCHAR(255) NOT NULL COMMENT '所属公司名称',
    Address   VARCHAR(255)  NOT NULL COMMENT '所属公司地址',
    BuyTime   DATETIME     NOT NULL COMMENT '购买时间',
    PRIMARY KEY (ID),
    UNIQUE (Code)
) COMMENT ='公司信息表';