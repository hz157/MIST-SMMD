import json

""" 配置文件 """
# json文件位置
Jsonfile = './test.json'
Textfile = './data.json'

def writeText(data: dict):
    Note = open(Textfile, 'a', encoding = "utf-8")
    Note.write(f'{data} \n') #\n 换行符

def readJsonFile():
    with open(Jsonfile, 'r', encoding="utf-8") as f:
        # 全部读取
        # json_data = json.loads(f)
        # 逐行读取
        count = 1
        for line in f.readlines():
            json_data = json.loads(line)
            data = """{"text": "{}"}"""
            analysis = convert(count, json_data)
            count = count + 1
            writeText(analysis)

def convert(id: int, json_data: dict=None):
    data_dicr = {'id': id}
    tagList = []
    # 为返回字典赋值Text
    data_dicr['text'] = json_data['text']
    # 拆分原有labels
    labels = json_data['labels']
    # 遍历字典Key
    for i in labels:
        # 遍历二级字典Key
        for j in labels[i]:
            # label数据
            labelList = []
            # 分割二级字典数据
            number = 0
            for position in str(labels[i][j]).replace('[','').replace(']','').split(','):
                if number == 1:
                    number = 0
                    labelList.append(int(position) + 1)
                else:
                    number = number + 1
                    # print(int(position))
                    labelList.append(int(position))
            # 添加label Title
            labelList.append(i)
            # 添加到总目录
            tagList.append(labelList)
    # 为返回字典labels赋值
    data_dicr['labels'] = tagList
    data_dicr['Comments'] = []
    print(data_dicr)
    # 返回数据
    return data_dicr

if __name__ == '__main__': 
    # print(convert({"text": "玉米的成交量也并不太理想。记者接触的多家企业负责人均表示并未参与拍卖。", "labels": {"position": {"记者": [[13, 14]], "负责人": [[22, 24]]}}}))
    readJsonFile()


