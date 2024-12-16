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
    def __init__(self):
        self.ID = 'ID'
        self.UserName = 'UserName'
        self.PassWord = 'PassWord'
        self.RealName = 'RealName'
        self.RoleClass = 'RoleClass'
        self.RoleID = 'RoleID'
        self.Phone = 'Phone'
        self.ProCode = 'ProCode'
        self.Status = 'Status'

    def columns_dict(self):
        return {
            "ID": self.ID,
            "UserName": self.UserName,
            "PassWord": self.PassWord,
            "RealName": self.RealName,
            "RoleClass": self.RoleClass,
            "RoleID": self.RoleID,
            "Phone": self.Phone,
            "ProCode": self.ProCode,
            "Status": self.Status
        }


class ProjectTable(object):
    def __init__(self):
        self.ProID = 'ProID'
        self.ProCode = 'ProCode'
        self.ProName = 'ProName'
        self.ProAddress = 'ProAddress'
        self.LinkMan = 'LinkMan'
        self.Phone = 'Phone'
        self.ProCreateTime = 'ProCreateTime'
        self.ProStatus = 'ProStatus'

    def columns_dict(self):
        return {
            "ProID": self.ProID,
            "ProCode": self.ProCode,
            "ProName": self.ProName,
            "ProAddress": self.ProAddress,
            "LinkMan": self.LinkMan,
            "Phone": self.Phone,
            "ProCreateTime": self.ProCreateTime,
            "ProStatus": self.ProStatus
        }


class TunnelTable(object):
    def __init__(self):
        self.TunID = "TunID"
        self.TunCode = "TunCode"
        self.TunName = "TunName"
        self.LinkMan = "LinkMan"
        self.Phone = "Phone"
        self.TunStatus = "TunStatus"
        self.ProCode = "ProCode"

    def columns_dict(self):
        return {
            "TunID": self.TunID,
            "TunCode": self.TunCode,
            "TunName": self.TunName,
            "LinkMan": self.LinkMan,
            "Phone": self.Phone,
            "TunStatus": self.TunStatus,
            "ProCode": self.ProCode
        }


class WorkSurfaceTable(object):
    def __init__(self):
        self.WorkSurID = "WorkSurID"
        self.WorkSurCode = "WorkSurCode"
        self.WorkSurName = "WorkSurName"
        self.ProCode = "ProCode"
        self.TunCode = "TunCode"

    def columns_dict(self):
        return {
            "WorkSurID": self.WorkSurID,
            "WorkSurCode": self.WorkSurCode,
            "WorkSurName": self.WorkSurName,
            "ProCode": self.ProCode,
            "TunCode": self.TunCode
        }


class StructureTable(object):
    def __init__(self):
        self.StruID = "StruID"
        self.StruCode = "StruCode"
        self.StruName = "StruName"
        self.FirWarningLevel = "FirWarningLevel"
        self.SecWarningLevel = "SecWarningLevel"
        self.ThirWarningLevel = "ThirWarningLevel"
        self.ProCode = "ProCode"
        self.TunCode = "TunCode"
        self.WorkSurCode = "WorkSurCode"

    def columns_dict(self):
        return {
            "StruID": self.StruID,
            "StruCode": self.StruCode,
            "StruName": self.StruName,
            "FirWarningLevel": self.FirWarningLevel,
            "SecWarningLevel": self.SecWarningLevel,
            "ThirWarningLevel": self.ThirWarningLevel,
            "ProCode": self.ProCode,
            "TunCode": self.TunCode,
            "WorkSurCode": self.WorkSurCode
        }




