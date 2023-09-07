from datetime import datetime

from config import config
from data.csv import read_csv, write_csv
from data.excel import read_excel, write_excel
from data.ner import sentence_split, spacy_label_mark, create_write_data


def read_weibo(path, fileType):
    """
        微博数据集的读取
    Args:
        path: 文件路径
        fileType: 文件类型

    Returns:数据列表list

    """
    if fileType.lower() == "excel":
        dataSetData = read_excel(path)
    elif fileType.lower() == "csv":
        dataSetData = read_csv(path, 'ansi')
    else:
        print("请输入正确的类型，仅支持csv与excel文件格式！")
    result = []
    for item in dataSetData:
        result.append({'create_at': str(item[1]), 'text': str(item[2]), 'region': str(item[4])})  # 构造list
    return result


if __name__ == '__main__':
    star_time = datetime.now()
    current = 0
    # fields = ['text', 'sentence', 'create_at', 'ner_time', 'ner_gpe', 'ner_fac', 'stand_time', 'stand_time_status',
    #           'stand_loc', 'stand_loc_status', 'lng-bd09', 'lat-bd09', 'lng-wgs84', 'lat-wgs84', 'street_id']  # 列名
    fields = ['text', 'sentence', 'create_at', 'ner_time', 'ner_gpe', 'ner_fac', 'stand_time', 'stand_time_status',
              'stand_loc', 'stand_loc_status', 'loc_bd09', 'loc_wgs84', 'street_id']  # 列名
    write_csv(config.SAVE_PATH, fields)  # 写标签列   验证csv可能会导致mid错乱，弃用csv
    # write_excel(config.SAVE_PATH, fields)   # 写标签列
    data = read_weibo(config.ORIGINAL_PATH, fileType="excel")  # 读取数据库导出的EXCEL数据
    for i in data:  # 遍历数据
        t1 = datetime.now()  # 开始时间
        i['sentence'] = sentence_split(i['text'], cri='coarse')  # 文本分句
        spacy_data = spacy_label_mark(i['sentence'])
        current = current + 1
        write_data = create_write_data(i, spacy_data)
        t2 = datetime.now()  # 结束时间
        print(f'当前执行: {current} / 总数据: {len(data)} 单条耗时: {str(t2 - t1)}')  # 状态显示
        if not write_data:
            continue
        if write_data != 'No nerTIME':
            # write_excel(config.SAVE_PATH, write_data, fields)  # 追加Excel数据
            write_csv(config.SAVE_PATH, write_data)  # 追加CSV数据     验证csv可能会导致mid错乱，弃用csv
        if current > 1000:
            break
    end_time = datetime.now()
    sum_time = end_time - star_time
    print('总处理时间耗时:%s,共%i条微博,平均每条耗时:%s' % (sum_time, current, sum_time / current))
