"""
@Author: zhang_zhiyi
@Date: 2024/10/12_11:26
@FileName:local_db_table.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description:
"""


class UserTable(object):
    """
    user table
    """

    def __init__(self):
        self.ID = 'ID'
        self.UserName = 'UserName'
        self.PassWord = 'PassWord'
        self.RealName = 'RealName'
        self.RoleClass = 'RoleClass'
        self.UserCode = 'UserCode'
        self.Phone = 'Phone'
        self.ProCode = 'ProCode'
        self.Status = 'Status'

    def columns_dict(self):
        return [self.ID, self.UserName, self.PassWord, self.RealName, self.RoleClass, self.UserCode, self.Phone,
                self.ProCode, self.Status]
        # return {
        #     "ID": self.ID,
        #     "UserName": self.UserName,
        #     "PassWord": self.PassWord,
        #     "RealName": self.RealName,
        #     "RoleClass": self.RoleClass,
        #     "RoleID": self.RoleID,
        #     "Phone": self.Phone,
        #     "ProCode": self.ProCode,
        #     "Status": self.Status
        # }


class ProjectTable(object):
    """
    project table
    """

    def __init__(self):
        self.ID = 'ID'
        self.ProCode = 'ProCode'
        self.ProName = 'ProName'
        self.ProAddress = 'ProAddress'
        self.LinkMan = 'LinkMan'
        self.Phone = 'Phone'
        self.ProCreateTime = 'ProCreateTime'
        self.ProStatus = 'ProStatus'
        self.ProCycle = 'ProCycle'

    def columns_dict(self):
        return [self.ID, self.ProCode, self.ProName, self.ProAddress, self.LinkMan, self.Phone,
                self.ProCreateTime, self.ProStatus, self.ProCycle]
        # return {
        #     "ProID": self.ProID,
        #     "ProCode": self.ProCode,
        #     "ProName": self.ProName,
        #     "ProAddress": self.ProAddress,
        #     "LinkMan": self.LinkMan,
        #     "Phone": self.Phone,
        #     "ProCreateTime": self.ProCreateTime,
        #     "ProStatus": self.ProStatus
        # }


class TunnelTable(object):
    """
    tunnel table
    """

    def __init__(self):
        self.ID = "ID"
        self.TunCode = "TunCode"
        self.TunName = "TunName"
        self.LinkMan = "LinkMan"
        self.Phone = "Phone"
        self.High = "High"
        self.TunStatus = "TunStatus"
        self.ProCode = "ProCode"
        self.TunCycle = "TunCycle"
        self.TunCreateTime = "TunCreateTime"

    def columns_dict(self):
        return [self.ID, self.TunCode, self.TunName, self.LinkMan, self.Phone, self.High, self.TunStatus,
                self.ProCode, self.TunCycle, self.TunCreateTime]
        # return {
        #     "TunID": self.TunID,
        #     "TunCode": self.TunCode,
        #     "TunName": self.TunName,
        #     "LinkMan": self.LinkMan,
        #     "Phone": self.Phone,
        #     "High": self.High,
        #     "TunStatus": self.TunStatus,
        #     "ProCode": self.ProCode
        # }


class WorkSurfaceTable(object):
    """
    work_surface table
    """

    def __init__(self):
        self.ID = "ID"
        self.WorkSurCode = "WorkSurCode"
        self.WorkSurName = "WorkSurName"
        self.ProCode = "ProCode"
        self.TunCode = "TunCode"
        self.StruCode = "StruCode"

    def columns_dict(self):
        return [self.ID, self.WorkSurCode, self.WorkSurName, self.ProCode, self.TunCode, self.StruCode]
        # return {
        #     "WorkSurID": self.WorkSurID,
        #     "WorkSurCode": self.WorkSurCode,
        #     "WorkSurName": self.WorkSurName,
        #     "ProCode": self.ProCode,
        #     "TunCode": self.TunCode
        # }


class StructureTable(object):
    """
    structure table
    """

    def __init__(self):
        self.ID = "ID"
        self.StruCode = "StruCode"
        self.StruName = "StruName"
        self.FirWarningLevel = "FirWarningLevel"
        self.SecWarningLevel = "SecWarningLevel"
        self.ThirWarningLevel = "ThirWarningLevel"
        # self.ProCode = "ProCode"
        # self.TunCode = "TunCode"
        # self.WorkSurCode = "WorkSurCode"

    def columns_dict(self):
        return [self.ID, self.StruCode, self.StruName, self.FirWarningLevel, self.SecWarningLevel,
                self.ThirWarningLevel]
        # return {
        #     "StruID": self.StruID,
        #     "StruCode": self.StruCode,
        #     "StruName": self.StruName,
        #     "FirWarningLevel": self.FirWarningLevel,
        #     "SecWarningLevel": self.SecWarningLevel,
        #     "ThirWarningLevel": self.ThirWarningLevel,
        #     "ProCode": self.ProCode,
        #     "TunCode": self.TunCode,
        #     "WorkSurCode": self.WorkSurCode
        # }


class AnomalyLogTable(object):
    """
    anomaly_log table
    """

    def __init__(self):
        self.ID = "ID"
        self.Identification = "Identification"
        self.ProCode = "ProCode"
        self.TunCode = "TunCode"
        self.WorkSurCode = "WorkSurCode"
        self.StruCode = "StruCode"
        self.Mileage = "Mileage"
        self.ConEquipCode = "ConEquipCode"
        self.DataAcqEquipCode = "DataAcqEquipCode"
        self.AnomalyTime = "AnomalyTime"
        self.Year = "Year"
        self.Month = "Month"
        self.Day = "Day"
        self.Hour = "Hour"
        self.Minute = "Minute"
        self.Second = "Second"

    def columns_dict(self):
        return [self.ID, self.Identification, self.ProCode, self.TunCode, self.WorkSurCode, self.StruCode,
                self.Mileage, self.ConEquipCode, self.DataAcqEquipCode, self.AnomalyTime, self.Year,
                self.Month, self.Day, self.Hour, self.Minute, self.Second]


class AnomalyLodDescTable(object):
    """
    anomaly_lod_desc table
    """

    def __init__(self):
        self.ID = "ID"
        self.DescCode = "DescCode"
        self.Identification = "Identification"
        self.Degree = "Degree"
        self.Region = "Region"
        self.Position = "Position"
        self.Bas = "Bas"

    def columns_dict(self):
        return [self.ID, self.DescCode, self.Identification, self.Degree, self.Region, self.Position, self.Bas]


class EqControlTable(object):
    """
    eq_control table
    """

    def __init__(self):
        self.ID = "ID"
        self.ConEquipCode = "ConEquipCode"
        self.ConEquipName = "ConEquipName"
        self.ConEquipIP = "ConEquipIP"
        self.ProCode = "ProCode"
        self.TunCode = "TunCode"
        self.WorkSurCode = "WorkSurCode"
        self.StruCode = "StruCode"

    def columns_dict(self):
        return [self.ID, self.ConEquipCode, self.ConEquipName, self.ConEquipIP, self.ProCode, self.TunCode,
                self.WorkSurCode, self.StruCode]


class EqDataTable(object):
    """
    eq_data table
    """
    def __init__(self):
        self.ID = "ID"
        self.DataAcqEquipCode = "DataAcqEquipCode"
        self.DataAcqEquipName = "DataAcqEquipName"
        self.DataAcqEquipIP = "DataAcqEquipIP"
        self.DataAcqEquipInterval = "DataAcqEquipInterval"
        self.Distance = "Distance"
        self.DataAcaEquipStatus = "DataAcaEquipStatus"
        self.ConEquipCode = "ConEquipCode"

    def columns_dict(self):
        return [self.ID, self.DataAcqEquipCode, self.DataAcqEquipName, self.DataAcqEquipIP,
                self.DataAcqEquipInterval, self.Distance, self.DataAcaEquipStatus, self.ConEquipCode]


class PcdLogTable(object):
    """
    pcd_log table
    """
    def __init__(self):
        self.ID = "ID"
        self.ProCode = "ProCode"
        self.TunCode = "TunCode"
        self.WorkSurCode = "WorkSurCode"
        self.StruCode = "StruCode"
        self.Mileage = "Mileage"
        self.ConEquipCode = "ConEquipCode"
        self.DataAcqEquipCode = "DataAcqEquipCode"
        self.PcdLogTime = "AnomalyTime"
        self.Year = "Year"
        self.Month = "Month"
        self.Day = "Day"
        self.Hour = "Hour"
        self.Minute = "Minute"
        self.Second = "Second"

    def columns_dict(self):
        return [self.ID, self.ProCode, self.TunCode, self.WorkSurCode, self.StruCode, self.Mileage, self.ConEquipCode,
                self.DataAcqEquipCode, self.PcdLogTime, self.Year, self.Month, self.Day, self.Hour, self.Minute,
                self.Second]


class RoleTable(object):
    """
    role table
    """

    def __init__(self):
        self.ID = 'ID'
        self.RoleClass = 'RoleClass'
        self.Creator = 'Creator'
        self.CreateTime = 'CreateTime'
        self.Status = 'Status'
        self.UserCode = 'UserCode'

    def columns_dict(self):
        return [self.ID, self.RoleClass, self.Creator, self.CreateTime, self.Status, self.UserCode]
