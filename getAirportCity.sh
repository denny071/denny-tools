#!/bin/bash
# 通过三字码获得城市名称
# 配置信息
HOST_NAME='120.92.116.180'
DB_PORT='3306'
DB_NAME='analysis_new'
USER_NAME='root'
PASSWD='qwe123ASD'

# 输出文件位置
JSON_FILE='./city.json'

# 处理不可识别的城市名称
dealCityName(){
     CITY=${CITY/藏族自治州/}
     CITY=${CITY/北京大兴/北京}
     CITY=${CITY/襄樊/襄阳}
     CITY=${CITY/昌都邦达/八宿}
     CITY=${CITY/海拉尔/呼伦贝尔}
     echo $CITY
}

# 查询数据库
MYSQL_CONNECT="mysql -h${HOST_NAME} -P${DB_PORT} -u${USER_NAME} -p${PASSWD} ${DB_NAME}";
SQL_QUERY="select airport,sanzima from airport"
DATA_FORMAT="tr -d '\t'"

CITY_DATA=`${MYSQL_CONNECT} -e "${SQL_QUERY}" | ${DATA_FORMAT}`
INDEX=1
# 拼接JSON
OUTPUT='{"state":0,"message":"ok","data":{'
for DATA in ${CITY_DATA}
do 
    if [ $DATA != "airportsanzima" ]; then
        SANZIMA=${DATA##*)}
        CITY=${DATA%%(*}
        CITY=`dealCityName ${CITY}`
        echo "（${INDEX}）${SANZIMA}所在城市【${CITY}】"
        INDEX=`expr $INDEX + 1`;
        # JSON像
        CITY_WEATHER="\"${SANZIMA}\":\"${CITY}\""
        # 拼接JSON
        OUTPUT="${OUTPUT}${CITY_WEATHER},"
    fi
done

OUTPUT="${OUTPUT%,*} }}"
# 输出数据到指定文件
echo $OUTPUT > ${JSON_FILE}