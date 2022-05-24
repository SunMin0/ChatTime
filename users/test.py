# # STEP 1
# import pymysql
#
# con = pymysql.connect(host='localhost', user='root', password='qwer1234',
#                        db='ChatTime', charset='utf8') # 한글처리 (charset = 'utf8')
# cur = con.cursor()
# sql = "SELECT * FROM chattime.users_customuser where login_method='C';"
# cur.execute(sql)
# rows = cur.fetchall()
# login_method = rows[0][12]
# if login_method == "C" :