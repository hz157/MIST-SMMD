# 未知-命名实体识别_迁移学习 unknown-NER_transfer learning
> 该分支，搜集了Github上已公开的命名实体识别公开数据集 用于基础模型训练用于迁移学习

## ArcGIS Pro 3.0训练实体识别模型所需的数据说明
经过反复测试，标签的起始位置使用计算机计数，结束位置需在基础上＋1
``` JSON
{"id": 1, "text": "今天是除夕夜。", "labels": [[0,2,"TIME"], [3,6,"TIME"]]}
```

### 代码内的JSON格式注释说明
``` python
    """
    Converts training data from JSON format to spacy offsets.

    =====================   ===========================================
    **Parameter**            **Description**
    ---------------------   -------------------------------------------
    text_key                Optional:str='text. Json key under which text is available
    ---------------------   -------------------------------------------
    offset_key              Optional:str='labels. Json key under which offsets are available
    =====================   ===========================================
    json-schema:
    ----------
    {"id": 1, "text": "EU rejects ...", "labels": [[0,2,"ORG"], [11,17, "MISC"], [34,41,"ORG"]]}
    {"id": 2, "text": "Peter Blackburn", "labels": [[0, 15, "PERSON"]]}
    {"id": 3, "text": "President Obama", "labels": [[10, 15, "PERSON"]]}
    ----------
    returns: A list that can be consumed by ner_databunch.
    """
```

### 未经过确切验证的问题
ArcGIS所导入的训练数据的label似乎只能识别全为大写的标签，如果出现小写，可能会导致报错（参数不足等报错）

## 所使用的Github公开数据集
- ChineseNER
- MSRA
- renmin
- WeiboNER
- Chinese Literature Text
- cluener
- Time_NLP
- Chinese NER Using Lattice LSTM
<br>
排名不分前后,可能有部分数据并未使用到。

