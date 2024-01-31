import json
import csv

# 读取并解析文件
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield json.loads(line)

# 主函数
def main():
    file_path = 'google100.txt'  # 输入文件的路径
    output_file = 'patents_dates.csv'  # 输出CSV文件的路径

    # 定义CSV文件的列
    headers = ['publication_number', 'filing_date', 'publication_date', 'grant_date', 'priority_date']

    # 读取并处理文件
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

        for patent in read_file(file_path):
            row = {
                'publication_number': patent.get('publication_number', ''),
                'filing_date': patent.get('filing_date', ''),
                'publication_date': patent.get('publication_date', ''),
                'grant_date': patent.get('grant_date', ''),
                'priority_date': patent.get('priority_date', '')
            }
            writer.writerow(row)

    print(f"数据已写入 {output_file}")

if __name__ == '__main__':
    main()
