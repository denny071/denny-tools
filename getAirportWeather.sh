#!/bin/bash
# 通过城市名称获得天气
# 配置信息
HOST_NAME='120.92.116.180'
DB_PORT='3306'
DB_NAME='analysis_new'
USER_NAME='root'
PASSWD='qwe123ASD'
WEATHER_API_URL='http://wthrcdn.etouch.cn/weather_mini'
WEATHER_WANGYI_API_URL='http://weather.mail.163.com/weather/xhr/weather/info.do'
# 输出文件位置
JSON_FILE='./weather.json'
# 是否请求API数据 0：不请求 1：请求
IS_RQUEST_API=1
# 是否获取海外数据 0：不获取 1：获取
IS_OVERSEAS=0
# 处理不可识别的城市名称
dealCityName(){
     CITY=${CITY/藏族自治州/}
     CITY=${CITY/北京大兴/北京}
     CITY=${CITY/襄樊/襄阳}
     CITY=${CITY/昌都邦达/八宿}
     CITY=${CITY/海拉尔/呼伦贝尔}
     echo $CITY
}
# 处理不可识别的城市名称
dealWeatherName(){

     WEATHER=${WEATHER/多云/阴}
     WEATHER=${WEATHER/雾/阴}
     WEATHER=${WEATHER/霾/阴}
     WEATHER=${WEATHER/浓雾/阴}
     WEATHER=${WEATHER/沙尘暴/阴}
     WEATHER=${WEATHER/浮尘/阴}
     WEATHER=${WEATHER/扬沙/阴}
     WEATHER=${WEATHER/强沙尘暴/阴}

     WEATHER=${WEATHER/阵雨/雨}
     WEATHER=${WEATHER/小雨/雨}
     WEATHER=${WEATHER/中雨/雨}
     WEATHER=${WEATHER/大雨/雨}
     WEATHER=${WEATHER/暴雨/雨}
     WEATHER=${WEATHER/雨夹雪/雨}
     WEATHER=${WEATHER/雷阵雨/雨}
     WEATHER=${WEATHER/冰雹/雨}
     WEATHER=${WEATHER/雷阵雨伴有冰雹/雨}
     WEATHER=${WEATHER/大暴雨/雨}
     WEATHER=${WEATHER/特大暴雨/雨}
     WEATHER=${WEATHER/冻雨/雨}
     WEATHER=${WEATHER/小到中雨/雨}
     WEATHER=${WEATHER/中到大雨/雨}
     WEATHER=${WEATHER/大到暴雨/雨}
     WEATHER=${WEATHER/暴雨到大暴雨/雨}
     WEATHER=${WEATHER/大暴雨到特大暴雨/雨}

     WEATHER=${WEATHER/阵雪/雪}
     WEATHER=${WEATHER/小雪/雪}
     WEATHER=${WEATHER/中雪/雪}
     WEATHER=${WEATHER/大雪/雪}
     WEATHER=${WEATHER/暴雪/雪}
     WEATHER=${WEATHER/小到中雪/雪}
     WEATHER=${WEATHER/中到大雪/雪}
     WEATHER=${WEATHER/大到暴雪/雪}
 
     echo $WEATHER
}

dealCityCode(){
    case $SEARCH_CITY in
        "北京") echo "101010100";;
        "朝阳") echo "101010300";;
        "上海") echo "101020100";;
        "天津") echo "101030100";;
        "重庆") echo "101040100";;
        "万州") echo "101041300";;
        "哈尔滨") echo "101050101";;
        "齐齐哈尔") echo "101050201";;
        "牡丹江") echo "101050301";;
        "佳木斯") echo "101050401";;
        "黑河") echo "101050601";;
        "漠河") echo "101050703";;
        "伊春") echo "101050801";;
        "大庆") echo "101050901";;
        "鸡西") echo "101051101";;
        "长春") echo "101060101";;
        "吉林") echo "101060201";;
        "延吉") echo "101060301";;
        "通化") echo "101060501";;
        "沈阳") echo "101070101";;
        "大连") echo "101070201";;
        "鞍山") echo "101070301";;
        "丹东") echo "101070601";;
        "锦州") echo "101070701";;
        "呼和浩特") echo "101080101";;
        "包头") echo "101080201";;
        "通辽") echo "101080501";;
        "赤峰") echo "101080601";;
        "鄂尔多斯") echo "101080701";;
        "锡林浩特") echo "101080901";;
        "二连浩特") echo "101080903";;
        "满洲里") echo "101081010";;
        "乌兰浩特") echo "101081101";;
        "石家庄") echo "101090101";;
        "唐山") echo "101090501";;
        "秦皇岛") echo "101091101";;
        "太原") echo "101100101";;
        "大同") echo "101100201";;
        "长治") echo "101100501";;
        "运城") echo "101100801";;
        "西安") echo "101110101";;
        "榆林") echo "101110401";;
        "安康") echo "101110701";;
        "汉中") echo "101110801";;
        "济南") echo "101120101";;
        "青岛") echo "101120201";;
        "烟台") echo "101120501";;
        "潍坊") echo "101120601";;
        "济宁") echo "101120701";;
        "临沂") echo "101120901";;
        "威海") echo "101121301";;
        "乌鲁木齐") echo "101130101";;
        "克拉玛依") echo "101130201";;
        "库尔勒") echo "101130601";;
        "且末") echo "101130605";;
        "阿克苏") echo "101130801";;
        "库车") echo "101130807";;
        "喀什") echo "101130901";;
        "伊宁") echo "101131001";;
        "塔城") echo "101131101";;
        "哈密") echo "101131201";;
        "和田") echo "101131301";;
        "阿勒泰") echo "101131401";;
        "富蕴") echo "101131408";;
        "博乐") echo "101131601";;
        "拉萨") echo "101140101";;
        "林芝") echo "101140401";;
        "八宿") echo "101140508";;
        "西宁") echo "101150101";;
        "玉树") echo "101150601";;
        "格尔木") echo "101150901";;
        "兰州") echo "101160101";;
        "庆阳") echo "101160401";;
        "酒泉") echo "101160801";;
        "敦煌") echo "101160808";;
        "天水") echo "101160901";;
        "嘉峪关") echo "101161401";;
        "银川") echo "101170101";;
        "固原") echo "101170401";;
        "中卫") echo "101170501";;
        "郑州") echo "101180101";;
        "南阳") echo "101180701";;
        "洛阳") echo "101180901";;
        "南京") echo "101190101";;
        "无锡") echo "101190201";;
        "苏州") echo "101190401";;
        "南通") echo "101190501";;
        "扬州") echo "101190601";;
        "盐城") echo "101190701";;
        "徐州") echo "101190801";;
        "淮安") echo "101190901";;
        "连云港") echo "101191001";;
        "常州") echo "101191101";;
        "武汉") echo "101200101";;
        "襄阳") echo "101200201";;
        "宜昌") echo "101200901";;
        "恩施") echo "101201001";;
        "沙市") echo "101201406";;
        "杭州") echo "101210101";;
        "宁波") echo "101210401";;
        "台州") echo "101210601";;
        "温州") echo "101210701";;
        "义乌") echo "101210904";;
        "衢州") echo "101211001";;
        "舟山") echo "101211101";;
        "合肥") echo "101220101";;
        "蚌埠") echo "101220201";;
        "安庆") echo "101220601";;
        "阜阳") echo "101220801";;
        "黄山") echo "101221001";;
        "福州") echo "101230101";;
        "厦门") echo "101230201";;
        "泉州") echo "101230501";;
        "连城") echo "101230703";;
        "武夷山") echo "101230905";;
        "南昌") echo "101240101";;
        "九江") echo "101240201";;
        "赣州") echo "101240701";;
        "景德镇") echo "101240801";;
        "长沙") echo "101250101";;
        "衡阳") echo "101250401";;
        "常德") echo "101250601";;
        "张家界") echo "101251101";;
        "怀化") echo "101251201";;
        "永州") echo "101251401";;
        "贵阳") echo "101260101";;
        "遵义") echo "101260201";;
        "安顺") echo "101260301";;
        "荔波") echo "101260412";;
        "黎平") echo "101260513";;
        "铜仁") echo "101260601";;
        "兴义") echo "101260901";;
        "成都") echo "101270101";;
        "绵阳") echo "101270401";;
        "南充") echo "101270501";;
        "达州") echo "101270601";;
        "泸州") echo "101271001";;
        "宜宾") echo "101271101";;
        "西昌") echo "101271610";;
        "九寨沟") echo "101271906";;
        "广汉") echo "101272003";;
        "广元") echo "101272101";;
        "广州") echo "101280101";;
        "梅州") echo "101280401";;
        "汕头") echo "101280501";;
        "深圳") echo "101280601";;
        "珠海") echo "101280701";;
        "佛山") echo "101280800";;
        "湛江") echo "101281001";;
        "昆明") echo "101290101";;
        "大理") echo "101290201";;
        "保山") echo "101290501";;
        "腾冲") echo "101290506";;
        "昭通") echo "101291001";;
        "临沧") echo "101291101";;
        "丽江") echo "101291401";;
        "德宏") echo "101291501";;
        "景洪") echo "101291601";;
        "南宁") echo "101300101";;
        "柳州") echo "101300301";;
        "桂林") echo "101300501";;
        "梧州") echo "101300601";;
        "百色") echo "101301001";;
        "北海") echo "101301301";;
        "海口") echo "101310101";;
        "三亚") echo "101310201";;
        "台北") echo "101340101";;
        "高雄") echo "101340201";;
        "嘉义") echo "101340202";;
        "台南") echo "101340203";;
        "台东") echo "101340204";;
        "台中") echo "101340401";;
        "花莲") echo "101340405";;
    esac
}


# 简化天气编码
dealSimpleWeatherCode(){
    case $SIMPLE_WEATHER in
    "晴") echo 1;;
    "阴") echo 2;;
    "雨") echo 3;;
    "雪") echo 4;;
    esac
}

# 转换天气编码
dealWeatherCode(){
    case $WEATHER in
     "晴") echo 1;;
     "阴") echo 2;;
     "雨") echo 3;;
     "雪") echo 4;;
     "多云") echo 5;;
     "雾") echo 6;;
     "霾") echo 7;;
     "浓雾") echo 8;;
     "沙尘暴") echo 9;;
     "浮尘") echo 10;;
     "扬沙") echo 11;;
     "强沙尘暴") echo 12;;
     "阵雨") echo 13;;
     "小雨") echo 14;;
     "中雨") echo 15;;
     "大雨") echo 16;;
     "暴雨") echo 17;;
     "雨夹雪") echo 18;;
     "雷阵雨") echo 19;;
     "冰雹") echo 20;;
     "雷阵雨伴有冰雹") echo 21;;
     "大暴雨") echo 22;;
     "特大暴雨") echo 23;;
     "冻雨") echo 24;;
     "小到中雨") echo 25;;
     "中到大雨") echo 26;;
     "大到暴雨") echo 27;;
     "暴雨到大暴雨") echo 28;;
     "大暴雨到特大暴雨") echo 29;;
     "阵雪") echo 30;;
     "小雪") echo 31;;
     "中雪") echo 32;;
     "大雪") echo 33;;
     "暴雪") echo 34;;
     "小到中雪") echo 35;;
     "中到大雪") echo 36;;
     "大到暴雪") echo 37;;
    esac
}
# 获得天气数据
getWeather(){
    if (( $IS_RQUEST_API == 0 )); then
        echo "晴"
    else 
        SEARCH_CITY=`dealCityName ${CITY}`
        QUERY_URL="${WEATHER_API_URL}?city=${SEARCH_CITY}"
        WEATHER_DATA=`curl -s -H "Accept-Encoding: gzip"  ${QUERY_URL} | gunzip | more`
        if [[ $WEATHER_DATA == '{"status":1002,"desc":"invilad-citykey"}' ]]; then
             # 获得天气
            echo `getWanyYiWeather ${CITY}`
        else 
            TEMP1=${WEATHER_DATA#*'type":"'}
            TEMP2=${TEMP1#*'type":"'}
            WEATHER_NAME=${TEMP2%%'"},'*}
            echo ${WEATHER_NAME} 
        fi
       

    fi
}

# 获得天气数据
getWanyYiWeather(){
    if (( $IS_RQUEST_API == 0 )); then
        echo "晴"
    else 
        SEARCH_CITY=`dealCityName ${CITY}`
        SEARCH_CITY_CODE=`dealCityCode ${SEARCH_CITY}`
        QUERY_URL="${WEATHER_WANGYI_API_URL}?city=${SEARCH_CITY_CODE}"
        WEATHER_DATA=`curl -s   ${QUERY_URL}  | more`
        if [ $WEATHER_DATA == '{"code":"FAIL","errorCode":"CITY_NOT_EXIST"}' ]; then
            echo ""
        else 
            TEMP1=${WEATHER_DATA#*'"weatherDay"'}
            TEMP2=${TEMP1#*'"value":"'}
            WEATHER_NAME=${TEMP2%%'"},"'*}
            echo ${WEATHER_NAME} 
        fi
     
    fi
}





# 查询数据库
MYSQL_CONNECT="mysql -h${HOST_NAME} -P${DB_PORT} -u${USER_NAME} -p${PASSWD} ${DB_NAME}";
SQL_CHINA_QUERY="select airport,sanzima from airport where country_name = '中国'"
SQL_OVERSEAS_QUERY="select airport,sanzima from airport where country_name <> '中国'"
DATA_FORMAT="tr -d '\t'"
# 国内天气
CHINA_DATA=`${MYSQL_CONNECT} -e "${SQL_CHINA_QUERY}" | ${DATA_FORMAT}`
INDEX=1
# 拼接JSON
OUTPUT='{"state":0,"message":"ok","data":['
for DATA in ${CHINA_DATA}
do 
    if [ $DATA != "airportsanzima" ]; then
        SANZIMA=${DATA#*)}
    
        if [ ${SANZIMA#*)} != "" ]; then
            SANZIMA=${SANZIMA#*)}
        fi
        
        TEMP=${DATA#*(}
        AIRPORT=${TEMP%)*}
        CITY=${DATA%%(*}
        # 获得天气
        WEATHER=`getWeather ${CITY}`
 
        # 获得天气编码
        WEATHER_CODE=`dealWeatherCode ${WEATHER}`
        # 简化天气
        SIMPLE_WEATHER=`dealWeatherName ${WEATHER}`
        # 获得简化天气编码
        SIMPLE_WEATHER_CODE=`dealSimpleWeatherCode ${SIMPLE_WEATHER}`
        # 调试日志
        SEARCH_CITY=`dealCityName ${CITY}`
        # echo $SEARCH_CITY
        echo "（${INDEX}）${AIRPORT}（${SANZIMA})所在城市【${CITY}】的当天天气为【${WEATHER}(${WEATHER_CODE})】简化后【${SIMPLE_WEATHER}(${SIMPLE_WEATHER_CODE})】"
        # 序号
        INDEX=`expr $INDEX + 1`;
        # JSON像
        CITY_WEATHER="{\"${SANZIMA}\":{\"simple_weather\":\"${SIMPLE_WEATHER_CODE}\",\"weather\":\"${WEATHER_CODE}\"}}"
        # 拼接JSON
        OUTPUT="${OUTPUT}${CITY_WEATHER},"
    fi
done
# 国际天气
if (( $IS_OVERSEAS == 1 )); then
    OVERSEAS_DATA=`${MYSQL_CONNECT} -e "${SQL_OVERSEAS_QUERY}" | ${DATA_FORMAT}`
    for DATA in ${OVERSEAS_DATA}
    do 
        if [ $DATA != "airportsanzima" ]; then
            SANZIMA=${DATA#*)}
            TEMP=${DATA#*(}
            AIRPORT=${TEMP%)*}
            CITY=${DATA%%(*}
            # 获得天气
            WEATHER=""
            # 获得天气编码
            WEATHER_CODE=0
            # 简化天气
            SIMPLE_WEATHER=""
            # 获得简化天气编码
            SIMPLE_WEATHER_CODE=0
            # 调试日志
            # echo "（${INDEX}）${AIRPORT}（${SANZIMA})所在城市【${CITY}】的当天天气为【${WEATHER}(${WEATHER_CODE})】简化后【${SIMPLE_WEATHER}(${SIMPLE_WEATHER_CODE})】"
            # 序号
            INDEX=`expr $INDEX + 1`;
            # JSON像
            CITY_WEATHER="{\"${SANZIMA}\":{\"simple_weather\":\"${SIMPLE_WEATHER}\",\"weather\":\"${WEATHER_CODE}\"}}"
            # 拼接JSON
            OUTPUT="${OUTPUT}${CITY_WEATHER},"
        fi
    done
fi
OUTPUT="${OUTPUT%,*} ]}"
# 输出数据到指定文件
echo $OUTPUT > ${JSON_FILE}