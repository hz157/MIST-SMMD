from datetime import datetime

import spacy

from config import config
from data.csv import read_csv, write_csv
from data.ner import sentence_split, spacy_label_mark, create_write_csv_data


def read_weibo_csv(path):
    """
        CSV数据集的读取
    Args:
        path: csv文件路径

    Returns:数据列表list

    """
    data = read_csv(path, 'ansi')
    result = []
    for item in data:
        result.append({'create_at': str(item[1]), 'text': str(item[2]), 'region': str(item[3])})  # 构造list
    return result


if __name__ == '__main__':
    current = 1
    write_csv(config.SAVE_CSV_PATH,
              ['text', 'sentence', 'create_at', 'ner_time', 'ner_gpe', 'ner_fac', 'stand_time', 'stand_time_status',
               'stand_loc', 'stand_loc_status', 'lng-bd09', 'lat-bd09', 'lng-wgs84', 'lat-wgs84', 'street_id'])  # 写标签列
    data = read_weibo_csv(config.ORIGINAL_CSV_PATH) # 读取原生CSV数据
    for i in data:  # 遍历数据
        i['sentence'] = sentence_split(i['text'], cri='coarse')  # 文本分句
        i['sentence'] = sentence_split(i['text'], cri='coarse')  # 文本分句
        t1 = datetime.now()
        spacy_data = spacy_label_mark(i['sentence'])
        t2 = datetime.now()
        t = t2 - t1
        print(f'当前执行: {current} / 总数据: {len(data)} 单条耗时: {str(t)}')  # 状态显示
        current = current + 1
        csv_data = create_write_csv_data(i, spacy_data)
        if not csv_data:
            continue
        if csv_data != 'No nerTIME':
            write_csv(config.SAVE_CSV_PATH, csv_data)  # 追加CSV数据

