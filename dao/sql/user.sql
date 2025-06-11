CREATE TABLE user
(
    ID        int AUTO_INCREMENT COMMENT '自增主键，唯一标识',
    Name  VARCHAR(32)  NOT NULL COMMENT '用户名称',
    RealName  Varchar(32)  NOT NULL COMMENT '真实姓名',
    RoleClass INT DEFAULT 1 COMMENT '角色名称/职称 0: 管理员, 1: 普通用户',
    UserCode    INT DEFAULT 1 COMMENT '角色编号/工号',
    Phone     VARCHAR(11)  NOT NULL COMMENT '用户联系电话',
    CompanyCode   VARCHAR(128) NOT NULL COMMENT '公司编号，外键',
    Status    INT DEFAULT 0 COMMENT '用户状态，0表示禁用状态，1表示正常状态，2表示异常状态',
    AuthCode  VARCHAR(6)  DEFAULT NULL COMMENT '验证码',
    AuthCodeCreateTime  DATETIME DEFAULT NULL COMMENT '验证码生成时间',
    AuthCodeLimit INT DEFAULT NULL COMMENT '验证码生成时限',
    PRIMARY KEY (ID),
    FOREIGN KEY (CompanyCode) REFERENCES company (Code) ON UPDATE CASCADE ON DELETE CASCADE, -- company Code
    UNIQUE (Phone)
) COMMENT ='用户表，存储用户基本信息，Phone唯一';