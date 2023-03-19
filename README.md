# 数据清洗获取最终训练数据
First Version Author: [Uyoin](#)<br>
Finally Version Author: [hz157](https://github.com/hz157)

## 提示
- **spacy语言包需手动安装**
```shell
    python -m spacy download zh_core_web_trf
```
- Spacy使用GPU调用请取消 ner.py中的该行注释
```python
# spacy.require_gpu()   # 使用GPU请取消该行注释
```

### 配置文件
可变更配置均在config/config.py文件中，修改config/config.py内的参数即可

### API

#### 百度Baidu
> 使用百度地图开放平台，使用前请先成为百度地图开放平台开发者申请个人Access Key（AK）
#### 腾讯Tencent
> 使用腾讯位置服务
