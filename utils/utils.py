import time
import pymysql
import json
import decimal
import string

from jieba.analyse import extract_tags

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)


def get_time():
    time_str = time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format("年", "月", "日")  # 因为直接写不支持直接识别中文，才用format写


# return: 连接，游标
def get_conn():
    # 创建连接
    conn = pymysql.connect(host="192.168.8.130",
                           user="root",
                           password="root",
                           db="cov",
                           charset="utf8")
    # 创建游标
    cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
    return conn, cursor


def close_conn(conn, cursor):
    cursor.close()
    conn.close()


def query(sql, *args):
    """
    封装通用查询
    :param sql:
    :param args:
    :return: 返回查询到的结果，((),(),)的形式
    """
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res


def get_c1_data():
    """
    :return: 返回大屏div id=c1 的数据
    """
    # 因为会更新多次数据，取时间戳最新的那组数据
    sql = "select sum(confirm)," \
          "(select suspect from history order by ds desc limit 1)," \
          "sum(heal)," \
          "sum(dead), " \
          "(select importedCase from history order by ds desc limit 1)" \
          "from details " \
          "where update_time=(select update_time from details order by update_time desc limit 1) "
    res = query(sql)

    data = res[0]
    print(type(data))
    print(data[0])
    json_list = []
    dic = {"confirm": data[0], "suspect": data[1], "heal": data[2], "dead": data[3], "importedCase": data[4]}
    json_list.append(dic)
    json_str = json.dumps(json_list, cls=DecimalEncoder)
    print(type(json_str))
    return json_str


# 返回各省数据
def get_c2_data():
    # 因为会更新多次数据，取时间戳最新的那组数据
    sql = "select province,sum(confirm) from details " \
          "where update_time=(select update_time from details " \
          "order by update_time desc limit 1) " \
          "group by province"
    res = query(sql)

    con = []
    for tup in res:
        con.append({"name": tup[0], "value": tup[1]})

    print(con)

    return res


def get_r1_data():
    sql = "select ds, confirm, suspect, heal, dead from history;"

    res = query(sql)

    return res


def get_r2_data():
    sql = "select ds, confirm_add, suspect_add from history;"

    res = query(sql)

    # 传回值均为数组
    day, confirm_add, suspect_add = [], [], []
    # 不要前七条数据
    for a, b, c in res[7:]:
        day.append(a.strftime('%m-%d'))
        confirm_add.append(b)
        suspect_add.append(c)

    dic = {
        "day": day,
        "confirm_add": confirm_add,
        "suspect_add": suspect_add,
    }
    print(dic)

    return res

def get_l1_data():
    sql = "select content from hotsearch order by id desc limit 20"

    res = query(sql)

    d = []

    for i in res:
        # 移除热搜数字
        k = i[0].rstrip(string.digits)
        # 获取热搜数组
        v = i[0][len(k):]
        # 使用jieba提取关键字
        ks = extract_tags(k)

        for j in ks:
            if not j.isdigit():
                d.append({"name": j, "value": v})

    dic = {"kws": d}

    return dic

    return res



def get_l2_data():
    sql = "select city, confirm from" \
          "(select city, confirm from details " \
          "where update_time=(select update_time from details order by update_time desc limit 1) " \
          "and province not in ('湖北', '北京', '上海', '天津', '重庆')" \
          "union all " \
          "select province as city, sum(confirm) as confirm from details " \
          "where update_time=(select update_time from details order by update_time desc limit 1) " \
          "and province in ('北京', '上海', '天津', '重庆') group by province) as a " \
          "order by confirm desc limit 5"

    res = query(sql)

    city, confirm = [], []
    for a, b in res:
        city.append(a)
        confirm.append(b)

    dic = {
        "city": city,
        "confirm": confirm
    }

    print (dic)
    return res


if __name__ == "__main__":
    print(get_l1_data())
    print("--------------------------------------------")
