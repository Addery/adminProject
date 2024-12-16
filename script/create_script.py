"""
@Author: zhang_zhiyi
@Date: 2024/8/19_11:26
@FileName:create_script.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 创建windows定时任务
"""
import subprocess


def create_daily_task(task_name, script_path):
    command = [
        'schtasks', '/create',
        '/tn', task_name,  # Task name
        # '/tr', f'python {script_path}',  # Task to run py file
        '/tr', f'{script_path}',  # Task to run exe file
        '/sc', 'daily',  # Schedule type
        '/st', '10:00',  # Start time (24-hour format)
        '/f'  # Force overwrite if task already exists
    ]

    # Execute the command
    subprocess.run(command, check=True)


# Example usage
create_daily_task('TunnelProject', r'E:\07-code\remote_study\tunnelProject\outer\script\history_script.exe')
