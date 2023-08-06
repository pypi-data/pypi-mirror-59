china_district [![latest_version]][pypi_version] [![License]][license_url] [![python_version]][python_version]
========




china_district是根据关键词获取行政区域信息的python库。

是对高德地图开放平台的行政区域查询接口进行了封装。



安装
------------

    pip install china-district

依赖库
---------

`requests=2.22.0`

## 基础使用示例

基础使用，默认使用作者自己的高德地图开发者key，每天上限调用30万次。超过这个限制将无法使用。


    >>> In [1]: from china_district import District
    # 初始化District,默认只返回下一级行政区，不返回行政区边界坐标点
    >>> In [2]: d=District()
    
    >>> In [3]: d.get("武侯区")
    {'status': '1',
     'info': 'OK',
     'infocode': '10000',
     'count': '1',
     'suggestion': {'keywords': [], 'cities': []},
     'districts': [{'citycode': '028',
       'adcode': '510107',
       'name': '武侯区',
       'center': '104.05167,30.630862',
       'level': 'district',
       'districts': [{'citycode': '028',
         'adcode': '510107',
         'name': '金花桥街道',
         'center': '103.973,30.6029',
         'level': 'street',
         'districts': []},
    ……}
    # 将当前搜索结果(json对象)写入到当前目录，默认文件名"搜索关键词.json"
    >>> d.to_json("武侯区")
    	写入本地完成...
​    
高级使用示例
------------------

``` d.get("武侯区")
>>> In [1]: from china_district import District
# 初始化District,key为高德地图开发者key,subdistrict设置显示下级行政区级数，extensions设置行政区信息中是否返回行政区边界坐标点，”base"不返回，“all"返回

>>> In [5]:d = District(key="182ad5d7061ed1e421091c22089c3677",subdistrict=3,extensions="all")

Out[6]: 
{'status': '1',
 'info': 'OK',
 'infocode': '10000',
 'count': '1',
 'suggestion': {'keywords': [], 'cities': []},
 'districts': [{'citycode': '028',
   'adcode': '510107',
   'name': '武侯区',
   'polyline': '103.949841,30.658586;103.949928,30.658864;103.950137,30.659044;103.950415,30.659121;103.950667,30.6591;103.952425,30.658587;103.952869,30.658525;103.95333,30.658589;103.953
687,30.658726;103.953966,30.658948;103.954261,30.659335;103.954984,30.660906;103.955149,30.661113;103.955472,30.661348;103.95575,30.661423;103.956107,30.661436;103.957439,30.661364;103.957……```}

```

## 请求参数说明



| 参数名      | 含义             | 规则说明                                                     | 是否必须 | 缺省值 |
| :---------- | :--------------- | :----------------------------------------------------------- | :------- | :----- |
| key         | 请求服务权限标识 | 用户在高德地图官网[申请Web服务API类型KEY](https://lbs.amap.com/dev/) | 可选     | 无     |
| keywords    | 查询关键字       | 规则：只支持单个关键词语搜索关键词支持：行政区名称、citycode、adcode例如，在subdistrict=2，搜索省份（例如山东），能够显示市（例如济南），区（例如历下区）adcode信息可参考[城市编码表](https://lbs.amap.com/api/webservice/download)获取 | 可选     | 无     |
| subdistrict | 子级行政区       | 规则：设置显示下级行政区级数（行政区级别包括：国家、省/直辖市、市、区/县、乡镇/街道多级数据）可选值：0、1、2、3等数字，并以此类推0：不返回下级行政区；1：返回下一级行政区；2：返回下两级行政区；3：返回下三级行政区； 需要在此特殊说明，目前部分城市和省直辖县因为没有区县的概念，故在市级下方直接显示街道。例如：广东-东莞、海南-文昌市 | 可选     | 1      |
| extensions  | 返回结果控制     | 此项控制行政区信息中返回行政区边界坐标点； 可选值：base、all;base:不返回行政区边界坐标点；all:只返回当前查询district的边界值，不返回子节点的边界值；目前**不能**返回乡镇/街道级别的边界值 | 可选     | base   |


## 了解更多

高德地图行政区域查询接口：https://lbs.amap.com/api/webservice/guide/api/district

License
-------
Licensed under the MIT License.


[License]:         https://img.shields.io/github/license/xugongli/china-district.svg
[license_url]:     https://github.com/xugongli/china-district/blob/master/LICENSE
[latest_version]:            https://img.shields.io/pypi/v/china_district.svg
[pypi_version]: https://pypi.org/project/china-district/
[python_version]: https://img.shields.io/pypi/pyversions/china_district.svg
