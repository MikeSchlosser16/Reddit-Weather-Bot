import pymysql
import time

def insert(com_id):
    client = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="", db="WeatherDB")
    try:
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        cursor = client.cursor()
        cursor.execute("INSERT into responses (comment_id, date_responded) values(%s,%s)",(com_id,now))
        client.commit()
    except Exception as e:
        print (e)
        client.rollback()
    finally:
        client.close()

def displayAll():
    client = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="", db="WeatherDB")
    try:
        cursor = client.cursor()
        query = "SELECT id, comment_id, date_responded FROM responses"
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            id = row[0]
            commentID = row[1]
            dateResponded = row[2]
            print ("ID: {}, Comment ID: {} Date: {}".format(id, commentID, dateResponded))
        cursor.execute(query)
    finally:
        client.close()
def verifyCommentID(commentID):
    client = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="", db="WeatherDB")
    try:
        cursor = client.cursor()
        query = "SELECT * FROM responses WHERE comment_id = \"{}\"".format(commentID)
        cursor.execute(query)
        if(cursor.rowcount == 0):
            print("Have not commented")
            return True;
        else:
            print("Previously commented")
            return False;
    except Exception as e:
        print(e)
        client.rollback()
    finally:
        client.close()
