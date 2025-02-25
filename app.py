from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextMessage, MessageEvent, TextSendMessage
import pymysql

app = Flask(__name__)

# ข้อมูล LINE Messaging API
LINE_CHANNEL_ACCESS_TOKEN = '7S6uRt1efIK0AUIui+qa9vt2bWnz86gnDcPNjABtR3P5uByKuYJJDHeOgFAAZzsG+EtJBX40Pwy0Jcy8WNEVdBURddWDACSMpOyYMH2LPaNcHjYq1Izo21Zc4ueGnJTavVa4QQg+7P3l/jQgGXSyZAdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '8e9f905d13850039ec87d27e65f77740'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# เชื่อมต่อกับ MySQL
def query_disease_info(disease_name):
    connection = pymysql.connect(
        host='localhost',
        user='root',  # ใช้ username ของ MySQL
        password='woon043697',  # ใส่รหัสผ่านของ MySQL
        database='durian_project',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM durian_disease WHERE name = %s"
            cursor.execute(sql, (disease_name,))
            result = cursor.fetchone()
            return result
    finally:
        connection.close()

@app.route("/callback", methods=['POST'])
def callback():
    print("Received request from LINE Platform")
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid Signature")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.strip()  # ข้อความที่ผู้ใช้ส่งมา
    disease_info = query_disease_info(user_message)  # ค้นหาใน MySQL

    if disease_info:
        reply = (
            f"ชื่อโรค: {disease_info['name']}\n"
            f"สาเหตุ: {disease_info['cause']}\n"
            f"อาการ: {disease_info['symptoms']}\n"
            f"การรักษา: {disease_info['treatment']}\n"
            f"ข้อมูลเพิ่มเติม: {disease_info['additional_info']}"
        )
    else:
        reply = "ไม่พบข้อมูลของโรคนี้ในระบบ"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)

