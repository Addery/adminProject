"""
@Author: zhang_zhiyi
@Date: 2024/11/22_16:12
@FileName:space_calculation.py
@LastEditors: zhang_zhiyi
@version: 1.0
@lastEditTime: 
@Description: 净空计算
"""
import open3d.visualization

from utils.calculation import calculation
from spaceCalculation.divide import divide
from utils.dfutils import df2pcd
from utils.preprocess import filter_distance
from utils.sampling import upsample_by_mesh
from utils.segment import pcd2df
from utils.show import read_csv


def run(data, save_path, size=5):
    try:
        res = {}
        # 数据预处理
        data = filter_distance(data, 50)
        s, v, mesh = calculation(data, show=False)
        upsampled_pcd = upsample_by_mesh(mesh)
        df = pcd2df(upsampled_pcd)
        seg_data = divide(df, size)
        region_dict = {}
        if seg_data:
            s, v = 0, 0
            for i, segment in enumerate(seg_data):
                i_s, i_v, _ = calculation(segment, show=False)
                s += i_s
                v += i_v

                # 将 dataframe转化为前端需要的格式
                segment.loc[:, 'Reflectivity'] = 102
                segment_list = []
                for row in segment.itertuples(index=False):
                    segment_list.extend([row.X, row.Y, row.Z, row.Reflectivity])
                segment_dict = {'surface_area': i_s, 'volume': i_v, 'points': segment_list}
                region_dict[i] = segment_dict
                # 将数据写入服务器本地
                with open(f'{save_path}/{i}.txt', 'w', encoding='utf-8') as f:
                    f.write(str(segment_dict))
                # print(f"第{i+1}段表面积: {i_s}, 体积: {i_v}")
            # print(f"segments calculation: 表面积: {s}, 体积: {v}")
            res['intact_surface_area'] = s
            res['intact_volume'] = v
            res['region'] = region_dict
        return res
    except Exception as e:
        print(f"Error during calculation: {e}")
        return None


if __name__ == '__main__':
    path = r'E:\07-code\tunnelProject\adminProject\test\data\1731656822.6120367_0.csv'
    data = read_csv(path)
    # pcd = df2pcd(data)
    # open3d.visualization.draw_geometries([pcd])
    print(run(data))
