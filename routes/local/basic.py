"""
@Author: zhang_zhiyi
@Date: 2024/10/11_10:05
@FileName:basic.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 数据库基础操作路由 未使用
"""
from flask import jsonify, request, Blueprint

from outer.utils.util_database import DBUtils


basic_local_db = Blueprint('basic_local_db', __name__)


@basic_local_db.route('/select', methods=['POST'])
def select_from_table():
    con = None
    try:
        """
        config = {
            'database_name': 'database_name',
            'table_name': 'table_name',
            'table_columns': [table_column1, table_column2, table_column3, ...]
        }
        如果table_columns为空列表，则默认执行select * from table_name，返回全部数据
        """
        data = request.json
        database_name = data.get('database_name')
        table_name, table_columns = data.get('table_name'), tuple(data.get('table_columns'))
        dbu = DBUtils()
        if database_name is None:
            con = dbu.connection()
        else:
            con = dbu.connection(database_name)
        res, status = DBUtils.select_table(con, table_name, table_columns)
        if res is None:
            return jsonify({'res': 'database select error'}), status
        return jsonify({'res': list(res)}), status
    except Exception as e:
        print(f"{e}, a error in /api/project/select")
        return jsonify({'res': 'Exception, defeat'}), 200
    finally:
        if con:
            DBUtils.close_connection(con)


@basic_local_db.route("/insert", methods=['POST'])
def insert_into_table():
    con = None
    try:
        """
        config = {
            'database_name': 'database_name',
            'table_name': 'table_name',
            'insert_data': {
                'column1': 'value1',
                'column2': 'value2',
                'column3': 'value3',
                ...
            }
        }
        """
        data = request.json
        database_name, table_name = data.get('database_name'), data.get('table_name')
        insert_data = data.get('insert_data')
        dbu = DBUtils()
        if database_name is None:
            con = dbu.connection()
        else:
            con = dbu.connection(database_name)
        res, status = DBUtils.insert_table(con, table_name, insert_data)
        return jsonify({'res': res}), status
    except Exception as e:
        print(f"{e}, a error in /api/project/insert")
        return jsonify({'res': 'Exception, defeat'}), 200
    finally:
        if con:
            DBUtils.close_connection(con)


@basic_local_db.route('/delete', methods=['POST'])
def delete_any_table():
    con = None
    try:
        """
        config = {
            'database_name': 'database_name',
            'table_name': 'table_name',
            'delete_condition': {
                'column': 'value'
            }
        }
        如果没有delete_condition字段，则默认执行delete from table_name，删除全部数据
        """
        data = request.json
        database_name, table_name = data.get('database_name'), data.get('table_name')
        delete_condition = data.get('delete_condition')
        dbu = DBUtils()
        if database_name is None:
            con = dbu.connection()
        else:
            con = dbu.connection(database_name)
        res, status = DBUtils.delete_table(con, table_name, delete_condition)
        return jsonify({'res': res}), status
    except Exception as e:
        print(f"{e}, a error in /api/project/delete")
        return jsonify({'res': 'Exception, defeat'}), 200
    finally:
        if con:
            DBUtils.close_connection(con)


@basic_local_db.route("/update", methods=['POST'])
def update_table():
    con = None
    try:
        """
        config = {
            'database_name': 'database_name',
            'table_name': 'table_name',
            'update_column': '...',
            'update_value': '...',
            'column': '...',
            'value': '...'
        }
        """
        data = request.json
        database_name, table_name = data.get('database_name'), data.get('table_name')
        update_column, update_value = data.get('update_column'), data.get('update_value')
        column, value = data.get('column'), data.get('value')
        dbu = DBUtils()
        if database_name is None:
            con = dbu.connection()
        else:
            con = dbu.connection(database_name)
        res, status = DBUtils.update_table(con, table_name, update_column, update_value, column, value)
        return jsonify({'res': res}), status
    except Exception as e:
        print(f"{e}, a error in /api/project/update")
        return jsonify({'res': 'Exception, defeat'}), 200
    finally:
        if con:
            DBUtils.close_connection(con)
