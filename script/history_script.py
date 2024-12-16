"""
@Author: zhang_zhiyi
@Date: 2024/8/16_14:20
@FileName:history_script.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 隧道项目只在本地保留三天内的历史数据和日志信息，并在每天早上10点进行检查

    假设保留三天的数据 count = 3
    以data/history为例，正常情况下只有两种情况：根目录下有一个文件夹、根目录下有两个文件夹
        config/history/ 如果该目录中只有一个文件夹，那么继续深入到下一层目录中
            config/history/2024/ 如果该目录中只有一个文件夹，那么继续深入到下一层目录中
                config/history/2024/8 如果该目录中的文件夹数量大于等于 count ，则需要修改本目录下的文件保留最新的 count 个文件夹，并删除上一层目录中的其他全部文件夹
                否则不需要修改
            config/history/2024/ 如果该目录中只有两个文件夹，那么首先深入到下一层最新的目录中
                config/history/2024/8 如果该目录中的文件夹数量大于等于 count ，则需要修改本目录下的文件保留最新的 count 个文件夹，并删除上一层目录中的其他全部文件夹
                否则记录当前目录中的文件夹数量为temp，在进入data/history/2024/中的另一个文件夹内，假设为data/history/2024/7，只保留这个目录中最新的 count - temp
                个文件夹
        config/history/ 如果该目录中有两个文件夹，直接深度到最新目录的下两层目录中
            config/history/2024/1 如果该目录中的文件夹数量大于等于 count ，则需要修改本目录下的文件保留最新的 count 个文件夹，并删除上一层目录中的其他全部文件夹
            config/history/2024/1 否则记录当前目录中的文件夹数量为temp，再进入data/history/2023/中的最新的文件夹内，假设为data/history/2023/12，只保留这个目录中最新的 count - temp
            个文件夹，其他文件夹及其上一级data/history/2023目录中除此之外的文件全部删除
"""
import os
import shutil
import sys
from pathlib import Path


def get_exe_root():
    """
    获取 .exe 脚本可执行文件所在的根目录
    """
    if getattr(sys, 'frozen', False):
        # 如果程序已经被打包为 .exe，返回 .exe 文件所在目录
        return os.path.dirname(sys.executable)
    else:
        # 如果是正常的 Python 脚本，返回脚本的所在目录
        return os.path.dirname(os.path.abspath(__file__))


def get_project_root_content(folder_name):
    """
    获取项目根目录
    :param folder_name:
    :return:
    """
    # return Path(__file__).parent.parent
    root_content = get_exe_root()
    parent_dir = os.path.abspath(os.path.join(root_content, os.pardir))
    target_dir = os.path.join(parent_dir, folder_name)
    return target_dir


def get_dir_count(directory):
    """
    获取directory路径下文件夹的数量
    :param directory:
    :return:
    """
    dirs = []
    dir_paths = []
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_dir():
                dirs.append(entry.name)
                dir_paths.append(entry.path)
    return len(dirs), dirs, dir_paths


def sorted_dirs(dirs, dirs_path):
    """
    排序
    :param dirs:
    :param dirs_path:
    :return:
    """
    try:
        int_dirs = list(map(int, dirs))
        combined = zip(int_dirs, dirs_path)
        combined_sorted = sorted(combined, key=lambda x: x[0])
        _, dirs_path_sorted = zip(*combined_sorted)
        return dirs_path_sorted
    except Exception as e:
        print(f"{str(e)}: A error in sorted_dirs")
        return None


def remove_file(dirs, paths, count, directory=None):
    """
    删除时目录中只有一个文件夹
    保留指定数量的非空文件夹
    :param directory
    :param dirs:
    :param paths:
    :param count:
    :return:
    """
    paths = sorted_dirs(dirs, paths)
    if paths is not None:
        remove_paths = paths[0: -count]
        if count == 0:
            shutil.rmtree(directory)
        for d in remove_paths:
            shutil.rmtree(d)


def remove_double_file(max_path, min_path, count, min_root_path=None):
    """
    删除时目录中有两个文件夹
    :param max_path:
    :param min_path:
    :param count:
    :param min_root_path:
    :return:
    """
    dir_count, son_dir, son_dir_paths = get_dir_count(max_path)
    # 如果数量大于 count 则需要修改max_path目录中的文件, 并删除mix_path中的所有文件
    if dir_count >= count:
        remove_file(son_dir, son_dir_paths, count)
        if min_root_path is not None:
            shutil.rmtree(min_root_path)
        else:
            shutil.rmtree(min_path)
    else:
        _, son_dir, son_dir_paths = get_dir_count(min_path)
        remove_file(son_dir, son_dir_paths, count - dir_count, min_path)


def remove_first_history(path, count):
    """
    目录第一层
    :param path:
    :param count:
    :return:
    """
    length = len(path)
    if length == 1:
        dir_count, dirs, dir_paths = get_dir_count(path[0])
        if dir_count <= count:
            return
        else:
            remove_file(dirs, dir_paths, count)
    elif length == 2:
        # 得到两个文件路径
        max_path, min_path = path[-1], path[-2]
        remove_double_file(max_path, min_path, count)
    else:
        return


def remove_second_history(dirs, dir_paths, count, depth):
    """
    目录第二层
    :param dirs:
    :param dir_paths:
    :param count:
    :param depth:
    :return:
    """
    # 正常情况下只有2个子目录
    if len(dir_paths) != 2:
        return

    # 对子目录进行排序
    dir_paths = sorted_dirs(dirs, dir_paths)
    if dir_paths is not None:
        # 得到两个文件路径
        max_path, min_path = dir_paths[-1], dir_paths[-2]
        min_root_path = None

        # 如果文件深度等于1，则需要直接在深入两层，而且最里层只有一个文件夹
        if depth == 1:
            if not os.listdir(min_path):
                shutil.rmtree(min_path)
                min_path = None
            else:
                min_root_path = min_path
                max_name, min_name = os.listdir(max_path)[0], os.listdir(min_path)[0]
                max_path, min_path = os.path.join(max_path, max_name), os.path.join(min_path, min_name)

        remove_double_file(max_path, min_path, count, min_root_path)


def history(directory, count=3, depth=0):
    """
    主程序
    :param directory:
    :param count:
    :param depth:
    :return:
    """
    depth += 1
    # 获取文件夹下文件夹的数量
    root_dir_count, dirs, dir_paths = get_dir_count(directory)

    if root_dir_count == 1:  # 如果文件夹数量为1
        if depth == 1:
            history(dir_paths[0], count, depth)
        elif depth == 2:
            remove_first_history(dir_paths, count)
    elif root_dir_count == 2:  # 如果文件夹数量为2
        remove_second_history(dirs, dir_paths, count, depth)
    else:
        return


def main():
    """
    主程序入口
    :return:
    """
    day = 3
    history_folder_name = "config/history"
    log_folder_name = "config/log"
    test_folder_name = "config/test"
    target_path = get_project_root_content(test_folder_name)
    history(target_path, day)


if __name__ == '__main__':
    main()
