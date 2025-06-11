    CREATE TABLE eq_data_conf
(
    ID     int AUTO_INCREMENT COMMENT '自增主键，唯一标识',
    ConfCode   VARCHAR(255)  NOT NULL COMMENT '配置编号，必须唯一',
    DataAcqEquipCode VARCHAR(255) NOT NULL COMMENT '采集设备编号，外键',
    LidarParameterSTW   VARCHAR(255)  NOT NULL COMMENT 'secsToWait',
    LidarParameterDur VARCHAR(255)  NOT NULL COMMENT 'duration',
    LidarParameterCollInter   VARCHAR(255)  NOT NULL COMMENT 'lidarCollInterval',
    LidarParameterConnInter   VARCHAR(255)  NOT NULL COMMENT 'lidarConnInterval',
    computerIP   VARCHAR(255)  NOT NULL COMMENT '采集端PC设备IP',
    sensorIP   VARCHAR(255)  NOT NULL COMMENT '采集端雷达设备IP',
    RabbitmqParameterUsername   VARCHAR(255)  NOT NULL COMMENT 'rabbitmq username',
    RabbitmqParameterPassword   VARCHAR(255)  NOT NULL COMMENT 'rabbitmq password',
    RabbitmqParameterHost   VARCHAR(255)  NOT NULL COMMENT 'rabbitmq host',
    RabbitmqParameterPort   VARCHAR(255)  NOT NULL COMMENT 'rabbitmq port',
    RabbitmqParameterVirtualHost   VARCHAR(255)  NOT NULL COMMENT 'rabbitmq virtualHost',
    RabbitmqParameterExchange   VARCHAR(255)  NOT NULL COMMENT 'rabbitmq exchange',
    RabbitmqParameterExchangeType   VARCHAR(255)  NOT NULL COMMENT 'rabbitmq exchangeType',
    RabbitmqParameterConnInterval   VARCHAR(255)  NOT NULL COMMENT 'rabbitmq connInterval',
    RabbitmqParameterRoutingKey varchar(255) NOT NULL COMMENT 'rabbitmq exchange routingkey',
    RabbitmqParameterQueueName varchar(255) NOT NULL COMMENT 'RabbitmqParameterQueueName',
    PRIMARY KEY (ID),
    FOREIGN KEY (DataAcqEquipCode) REFERENCES eq_data (DataAcqEquipCode) ON UPDATE CASCADE ON DELETE CASCADE, -- eq_data DataAcqEquipCode
    UNIQUE (ConfCode)
) COMMENT ='采集设备配置文件表，存储采集设备配置文件的配置项信息，ConfCode唯一';