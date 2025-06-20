"""
@Author: zhang_zhiyi
@Date: 2024/10/11_9:46
@FileName:app.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: app启动脚本
"""

from flask import Flask
from flask_cors import CORS

from routes.local.basic.select import base_select_db
from routes.local.company.company import company_db
from routes.local.config.eq_control_conf import eq_con_conf_db
from routes.local.config.eq_data_conf import eq_data_conf_db
from routes.local.config.file import config_file_db
from routes.local.equipment.console import console_db
from routes.local.equipment.data import data_acq_db
from routes.local.log.anomaly import anomaly_db
from routes.local.log.history import history_db
from routes.local.pcd.pcd_db_op import pcd_db_op
from routes.local.project.project import project_db
from routes.local.project.structure import structure_db
from routes.local.project.tunnel import tunnel_db
from routes.local.project.work_surface import work_surface_db
from routes.local.pcd.pcd_file_op import pcd_file_op
from routes.local.user.user import user_db
from routes.local.user.role import role_db
from routes.local.wx.wx import wx_db
from routes.miniprogram.monitor_atten import monitor_db
from routes.miniprogram.property import property_db
from routes.miniprogram.user_info import info_db
from routes.miniprogram.warn import mp_warn_db

app = Flask(__name__)
CORS(app)


# app.register_blueprint(basic_local_db, url_prefix='/api/outer/basic_db')
app.register_blueprint(pcd_file_op, url_prefix='/api/outer/pcd_file_op')
app.register_blueprint(pcd_db_op, url_prefix='/api/outer/pcd_db_op')
app.register_blueprint(user_db, url_prefix='/api/outer/user_db')
app.register_blueprint(role_db, url_prefix='/api/outer/role_db')
app.register_blueprint(project_db, url_prefix='/api/outer/project_db')
app.register_blueprint(tunnel_db, url_prefix='/api/outer/tunnel_db')
app.register_blueprint(work_surface_db, url_prefix='/api/outer/work_surface_db')
app.register_blueprint(structure_db, url_prefix='/api/outer/structure_db')
app.register_blueprint(console_db, url_prefix='/api/outer/console_db')
app.register_blueprint(data_acq_db, url_prefix='/api/outer/data_acq_db')
app.register_blueprint(anomaly_db, url_prefix='/api/outer/anomaly_db')
app.register_blueprint(history_db, url_prefix='/api/outer/history_db')
app.register_blueprint(base_select_db, url_prefix='/api/outer/basic/select')
app.register_blueprint(config_file_db, url_prefix='/api/outer/config_file_db')
app.register_blueprint(mp_warn_db, url_prefix='/api/outer/mp_warn_db')
app.register_blueprint(eq_con_conf_db, url_prefix='/api/outer/eq_con_conf_db')
app.register_blueprint(eq_data_conf_db, url_prefix='/api/outer/eq_data_conf_db')
app.register_blueprint(company_db, url_prefix='/api/outer/company_db')
app.register_blueprint(property_db, url_prefix='/api/mp/property_db')
app.register_blueprint(info_db, url_prefix='/api/mp/info_db')
app.register_blueprint(monitor_db, url_prefix='/api/mp/monitor_db')
app.register_blueprint(wx_db, url_prefix='/api/wx/wx_db')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8023)

