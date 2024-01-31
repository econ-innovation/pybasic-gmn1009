import pandas as pd
import requests

# 高德地图API的基础URL
AMAP_URL = "https://restapi.amap.com/v3/place/text"

# 高德地图API密钥
AMAP_KEY = "45aff143c80be095aa0b05b0bb7b606a"

# 从Excel文件中读取大学名单
def read_university_list(file_path):
    df = pd.read_excel(file_path)
    return df['大学名称'].tolist()

# 使用高德API获取地理位置信息
def get_location_details(university, key):
    params = {
        "key": key,
        "keywords": university,
        "types": "高等院校",
        "city": "全国",
        "children": 1,
        "offset": 1,
        "page": 1,
        "extensions": "all"
    }
    response = requests.get(AMAP_URL, params=params)
    if response.status_code == 200:
        results = response.json()["pois"]
        if results:
            location_info = results[0]
            province = location_info['pname']
            city = location_info['cityname']
            district = location_info['adname']
            street = location_info['address']
            location = location_info['location']
            longitude, latitude = location.split(',')
            return province, city, district, street, longitude, latitude
        else:
            return ["未找到"] * 6
    else:
        return ["请求错误"] * 6

# 主程序
def main():
    # Excel文件路径
    file_path = '985.xlsx'

    # 读取大学名单
    universities = read_university_list(file_path)

    # 创建DataFrame
    cols = ['University', 'Province', 'City', 'District', 'Street', 'Longitude', 'Latitude']
    result_df = pd.DataFrame(columns=cols)

    # 获取每所大学的地理位置信息
    for university in universities:
        province, city, district, street, longitude, latitude = get_location_details(university, AMAP_KEY)
        result_df = result_df.append({
            'University': university,
            'Province': province,
            'City': city,
            'District': district,
            'Street': street,
            'Longitude': longitude,
            'Latitude': latitude
        }, ignore_index=True)

    # 将结果保存回Excel
    result_df.to_excel('university_locations.xlsx', index=False)

    print("处理完成，结果已保存到 university_locations.xlsx")

if __name__ == "__main__":
    main()
