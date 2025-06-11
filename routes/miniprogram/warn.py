"""
@Author: zhang_zhiyi
@Date: 2025/4/21_15:18
@FileName:warn.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 小程序预警相关
"""
from PIL import Image
from flask import jsonify, request, Blueprint
from pymysql.cursors import DictCursor

from routes.local.status_code.baseHttpStatus import BaseHttpStatus
from utils.util_database import DBUtils
from utils.util_picture import IMGUtils

mp_warn_db = Blueprint('mp_warn_db', __name__)


@mp_warn_db.route('/selectWarn', methods=['POST'])
def log_select():
    try:
        data = request.json
        res = DBUtils.paging_display_condition_on_sql(data, 'anomaly_log', 1, 10, join=True)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查找失败', 'data': {'exception': str(e)}}), 200


@mp_warn_db.route('/searchWarn', methods=['POST'])
def desc_search_by_column():
    try:
        data = request.json
        identification = data.get('Identification')
    except Exception as e:
        return jsonify({'code': BaseHttpStatus.GET_DATA_ERROR.value, 'msg': '筛选失败', 'data': {'exception': str(e)}}), 200

    if not all([identification]):
        return jsonify({'code': BaseHttpStatus.PARAMETER.value, 'msg': '缺少必要的字段', 'data': {}}), 200

    con = None
    cursor = None
    try:
        dbu = DBUtils()
        con = dbu.connection(cursor_class=DictCursor)
        cursor = con.cursor()
        con.autocommit(False)

        # identification 是否已经存在
        id_sql = f"SELECT * FROM anomaly_log WHERE Identification = '{identification}'"
        res = DBUtils.project_is_exist(cursor, id_sql, BaseHttpStatus.OK.value, "预警记录不存在")
        if res:
            return jsonify(res), 200

        sql = """
            SELECT
                log.*, log_desc.*, log_img.*, p.ProName, t.TunName, w.WorkSurName, s.StruName, eq_c.ConEquipName, eq_d.DataAcqEquipName
            FROM
                anomaly_log log
            INNER JOIN anomaly_log_desc log_desc ON log.Identification = log_desc.Identification
            INNER JOIN anomaly_log_img log_img ON log.Identification = log_img.Identification
            INNER JOIN project p ON log.ProCode = p.ProCode
            INNER JOIN tunnel t ON log.TunCode = t.TunCode
            INNER JOIN work_surface w ON log.WorkSurCode = w.WorkSurCode
            INNER JOIN structure s ON log.StruCode = s.StruCode
            INNER JOIN eq_control eq_c ON log.ConEquipCode = eq_c.ConEquipCode
            INNER JOIN eq_data eq_d ON log.DataAcqEquipCode = eq_d.DataAcqEquipCode
            WHERE log.Identification = %s
        """
        cursor.execute(sql, identification)
        res = cursor.fetchall()
        con.commit()
        if res and len(res) == 1:
        #     item = res[0]
        #     if isinstance(item, dict) and item:
        #         pro_code = item.get('ProCode')
        #         tun_code = item.get('TunCode')
        #         work_sur_code = item.get('WorkSurCode')
        #         stru_code = item.get('StruCode')
        #         control_code = item.get('ConEquipCode')
        #         data_code = item.get('DataAcqEquipCode')
        #
        #         # project
        #         project = DBUtils.search_by_some_item('project', 'ProCode', pro_code)
        #         project_data = project.get('data')
        #         if project_data:  # 如果存在项目记录
        #             item['ProName'] = project_data.get('items')[0].get('ProName')
        #         else:
        #             return jsonify(
        #                 {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '项目信息存在问题', 'data': {}}), 200
        #
        #         # tunnel
        #         tunnel = DBUtils.search_by_some_item('tunnel', 'TunCode', tun_code)
        #         tunnel_data = tunnel.get('data')
        #         if tunnel_data:  # 如果存在项目记录
        #             item['TunName'] = tunnel_data.get('items')[0].get('TunName')
        #         else:
        #             return jsonify(
        #                 {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '隧道信息存在问题', 'data': {}}), 200
        #
        #         # work_surface
        #         work_surface = DBUtils.search_by_some_item('work_surface', 'WorkSurCode', work_sur_code)
        #         work_surface_data = work_surface.get('data')
        #         if work_surface_data:  # 如果存在项目记录
        #             item['WorkSurName'] = work_surface_data.get('items')[0].get('WorkSurName')
        #         else:
        #             return jsonify(
        #                 {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '工作面信息存在问题', 'data': {}}), 200
        #
        #         # structure
        #         structure = DBUtils.search_by_some_item('structure', 'StruCode', stru_code)
        #         structure_data = structure.get('data')
        #         if structure_data:  # 如果存在项目记录
        #             item['StruName'] = structure_data.get('items')[0].get('StruName')
        #         else:
        #             return jsonify(
        #                 {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '结构物信息存在问题', 'data': {}}), 200
        #
        #         # eq_control
        #         eq_control = DBUtils.search_by_some_item('eq_control', 'ConEquipCode', control_code)
        #         eq_control_data = eq_control.get('data')
        #         if eq_control_data:  # 如果存在项目记录
        #             item['ConEquipName'] = eq_control_data.get('items')[0].get('ConEquipName')
        #         else:
        #             return jsonify(
        #                 {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '总控设备信息存在问题', 'data': {}}), 200
        #
        #         # eq_data
        #         eq_data = DBUtils.search_by_some_item('eq_data', 'DataAcqEquipCode', data_code)
        #         eq_data_data = eq_data.get('data')
        #         if eq_data_data:  # 如果存在项目记录
        #             item['DataAcqEquipName'] = eq_data_data.get('items')[0].get('DataAcqEquipName')
        #         else:
        #             return jsonify(
        #                 {'code': BaseHttpStatus.EXCEPTION.value, 'msg': '采集设备信息存在问题', 'data': {}}), 200

            # avia_picture = Image.open(item.get('AviaPicturePath'))
            # camera_picture = Image.open(item.get('CameraPicturePath'))
            # item['AviaPicturePath'] = IMGUtils.img2base64(avia_picture)
            # item['CameraPicturePath'] = IMGUtils.img2base64(camera_picture)
            return jsonify({'code': BaseHttpStatus.OK.value, 'msg': '成功', 'data': res}), 200

        return {'code': BaseHttpStatus.ERROR.value, 'msg': '不存在符合要求的记录', 'data': {}}
    except Exception as e:
        if con:
            con.rollback()
        return jsonify({'code': BaseHttpStatus.EXCEPTION.value, 'msg': '查看失败', 'data': {'exception': str(e)}}), 200
    finally:
        if cursor:
            cursor.close()
        if con:
            DBUtils.close_connection(con)
