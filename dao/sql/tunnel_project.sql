DROP DATABASE IF EXISTS tunnel_project;

CREATE DATABASE tunnel_project;

USE tunnel_project;

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
    PRIMARY KEY (ProID),
    UNIQUE (ProCode)
) COMMENT ='项目表，存储项目的基本信息，(ProCode)唯一';

CREATE TABLE tunnel
(
    TunID     int AUTO_INCREMENT COMMENT '自增主键，唯一标识',
    TunCode   VARCHAR(64)  NOT NULL COMMENT '隧道编号，必须唯一',
    TunName   VARCHAR(64)  NOT NULL COMMENT '隧道名称',
    LinkMan   VARCHAR(64)  NOT NULL COMMENT '联系人姓名',
    Phone     VARCHAR(11)  NOT NULL COMMENT '联系人电话',
    High      VARCHAR(16)  NOT NULL COMMENT '隧道高度',
    TunStatus INT DEFAULT 0 COMMENT '隧道状态，0表示未开始，1表示进行中，2表示已完成',
    ProCode   VARCHAR(128) NOT NULL COMMENT '项目编号，外键',
    PRIMARY KEY (TunID),
    FOREIGN KEY (ProCode) REFERENCES project (ProCode) ON UPDATE CASCADE ON DELETE CASCADE, -- project ProCode
    UNIQUE (TunCode, ProCode)
) COMMENT ='隧道表，存储隧道的基本信息，(TunCode, ProCode)唯一';

CREATE TABLE structure
(
    StruID           int AUTO_INCREMENT COMMENT '自增主键，唯一标识',
    StruCode         VARCHAR(64)    NOT NULL COMMENT '结构物编号，必须唯一',
    StruName         VARCHAR(64)    NOT NULL COMMENT '结构物名称',
    FirWarningLevel  DECIMAL(10, 9) NOT NULL COMMENT '一级预警阈值，单位米',
    SecWarningLevel  DECIMAL(10, 9) NOT NULL COMMENT '二级预警阈值，单位米',
    ThirWarningLevel DECIMAL(10, 9) NOT NULL COMMENT '三级预警阈值，单位米',
#     ProCode VARCHAR(128) NOT NULL COMMENT '项目编号，外键',
#     TunCode VARCHAR(128) NOT NULL COMMENT '隧道编号，外键',
#     WorkSurCode VARCHAR(128) NOT NULL COMMENT '工作面编号，外键',
    PRIMARY KEY (StruID),
#     FOREIGN KEY (ProCode) REFERENCES project(ProCode) ON UPDATE CASCADE ON DELETE CASCADE,  -- project ProCode
#     FOREIGN KEY (TunCode) REFERENCES tunnel(TunCode) ON UPDATE CASCADE ON DELETE CASCADE,  -- tunnel TunCode
#     FOREIGN KEY (WorkSurCode) REFERENCES work_surface(WorkSurCode) ON UPDATE CASCADE ON DELETE CASCADE,  -- work_surface WorkSurCode
    UNIQUE (StruCode)
) COMMENT ='结构物表，存储结构物的基本信息，(StruCode, WorkSurCode)唯一';

CREATE TABLE work_surface
(
    WorkSurID   int AUTO_INCREMENT COMMENT '自增主键，唯一标识',
    WorkSurCode VARCHAR(64) NOT NULL COMMENT '工作面代码，必须唯一',
    WorkSurName VARCHAR(64) NOT NULL COMMENT '工作面名称',
    ProCode     VARCHAR(64) NOT NULL COMMENT '项目编号，外键',
    TunCode     VARCHAR(64) NOT NULL COMMENT '隧道编号，外键',
    StruCode    VARCHAR(64) NOT NULL COMMENT '结构物编号，外键',
    PRIMARY KEY (WorkSurID),
    FOREIGN KEY (StruCode) REFERENCES structure (StruCode) ON UPDATE CASCADE ON DELETE CASCADE, -- structure StruCode
    FOREIGN KEY (ProCode) REFERENCES project (ProCode) ON UPDATE CASCADE ON DELETE CASCADE,     -- project ProCode
    FOREIGN KEY (TunCode) REFERENCES tunnel (TunCode) ON UPDATE CASCADE ON DELETE CASCADE,      -- tunnel TunCode

    UNIQUE (WorkSurCode, TunCode)
) COMMENT ='工作面表，存储工作面的基本信息，(WorkSurCode, TunCode)唯一';

CREATE TABLE eq_control
(
    ConEquipID   int AUTO_INCREMENT COMMENT '自增主键，唯一标识',
    ConEquipCode VARCHAR(64) NOT NULL COMMENT '中控设备编号，必须唯一',
    ConEquipName VARCHAR(64) NOT NULL COMMENT '中控设备名称',
    ConEquipIP   VARCHAR(20) NOT NULL COMMENT '中控设备ip地址',
    ProCode      VARCHAR(64) NOT NULL COMMENT '项目编号，外键',
    TunCode      VARCHAR(64) NOT NULL COMMENT '隧道编号，外键',
    WorkSurCode  VARCHAR(64) NOT NULL COMMENT '工作面编号，外键',
    StruCode     VARCHAR(64) NOT NULL COMMENT '结构物编号，外键',
    PRIMARY KEY (ConEquipID),
    FOREIGN KEY (ProCode) REFERENCES project (ProCode) ON UPDATE CASCADE ON DELETE CASCADE,              -- project ProCode
    FOREIGN KEY (TunCode) REFERENCES tunnel (TunCode) ON UPDATE CASCADE ON DELETE CASCADE,               -- tunnel TunCode
    FOREIGN KEY (WorkSurCode) REFERENCES work_surface (WorkSurCode) ON UPDATE CASCADE ON DELETE CASCADE, -- work_surface WorkSurCode
    FOREIGN KEY (StruCode) REFERENCES structure (StruCode) ON UPDATE CASCADE ON DELETE CASCADE,          -- structure StruCode
#     UNIQUE (ConEquipCode, WorkSurCode)
    UNIQUE (ConEquipCode)
# ) COMMENT ='中控设备表，存储中控设备的基本信息，(ConEquipCode, WorkSurCode)唯一';
) COMMENT ='中控设备表，存储中控设备的基本信息，ConEquipCode唯一';

CREATE TABLE eq_data
(
    DataAcqEquipID       int AUTO_INCREMENT COMMENT '自增主键，唯一标识',
    DataAcqEquipCode     VARCHAR(64)  NOT NULL COMMENT '采集器设备编号，必须唯一',
    DataAcqEquipName     VARCHAR(64)  NOT NULL COMMENT '采集器设备名称',
    DataAcqEquipIP       VARCHAR(20)  NOT NULL COMMENT '采集器设备ip地址',
    DataAcqEquipInterval INT          NOT NULL COMMENT '数据采集时间间隔',
    Distance             FLOAT DEFAULT 0 COMMENT '采集器所处里程',
    DataAcaEquipStatus   INT   DEFAULT 0 COMMENT '中控设备状态，0表示关闭，1表示开启，2表示损坏',
    ConEquipCode         VARCHAR(128) NOT NULL COMMENT '中控设备编号，外键',
    PRIMARY KEY (DataAcqEquipID),
    FOREIGN KEY (ConEquipCode) REFERENCES eq_control (ConEquipCode) ON UPDATE CASCADE ON DELETE CASCADE, -- central_control_equipment ConEquipCode
#     UNIQUE (DataAcqEquipCode, ConEquipCode)
    UNIQUE (DataAcqEquipCode)
# ) COMMENT ='数据采集设备表，存储数据采集设备的基本信息，(DataAcqEquipCode, ConEquipCode)唯一';
) COMMENT ='数据采集设备表，存储数据采集设备的基本信息，DataAcqEquipCode唯一';

CREATE TABLE user
(
    ID        int AUTO_INCREMENT COMMENT '自增主键，唯一标识',
    UserName  VARCHAR(32)  NOT NULL COMMENT '用户名称',
    PassWord  VARCHAR(16)  NOT NULL COMMENT '用户密码',
    RealName  Varchar(32)  NOT NULL COMMENT '真实姓名',
    RoleClass INT DEFAULT 1 COMMENT '角色名称/职称 0: 管理员, 1: 普通用户',
    RoleID    INT DEFAULT 1 COMMENT '角色编号/工号',
    Phone     VARCHAR(11)  NOT NULL COMMENT '用户联系电话',
    ProCode   VARCHAR(128) NOT NULL COMMENT '项目编号，外键',
    Status    INT DEFAULT 0 COMMENT '用户状态，0表示禁用状态，1表示正常状态，2表示异常状态',
    PRIMARY KEY (ID),
    FOREIGN KEY (ProCode) REFERENCES project (ProCode) ON UPDATE CASCADE ON DELETE CASCADE, -- project ProCode
    UNIQUE (UserName, ProCode)
) COMMENT ='用户表，存储用户基本信息，(UserName, ProCode)唯一';

