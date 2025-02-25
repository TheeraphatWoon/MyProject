from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, ImageMessage, TextSendMessage, ImageSendMessage
from linebot.exceptions import InvalidSignatureError
import pymysql
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random
from ultralytics import YOLO
import io

app = Flask(__name__)

# ข้อมูล LINE Messaging API
LINE_CHANNEL_ACCESS_TOKEN = '7S6uRt1efIK0AUIui+qa9vt2bWnz86gnDcPNjABtR3P5uByKuYJJDHeOgFAAZzsG+EtJBX40Pwy0Jcy8WNEVdBURddWDACSMpOyYMH2LPaNcHjYq1Izo21Zc4ueGnJTavVa4QQg+7P3l/jQgGXSyZAdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '8e9f905d13850039ec87d27e65f77740'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# โหลดโมเดล
model = YOLO(r"C:\Users\theer\projectrue\Finalproject\runs\detect\train3true\weights\best.pt")

# ฟังก์ชันสำหรับวาดกรอบและข้อความ
def draw_boxes(image, results):
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", size=20)
    except:
        font = ImageFont.load_default()

    for box in results.boxes:
        bbox = box.xyxy[0].tolist()  # พิกัดกรอบ
        conf = box.conf[0].item() * 100  # ความมั่นใจ
        cls = int(box.cls[0].item())  # หมายเลขคลาส
        disease_name = results.names[cls]  # ชื่อโรค

        # วาดกรอบและข้อความ
        draw.rectangle(bbox, outline="red", width=3)
        draw.text((bbox[0], bbox[1] - 20), f"{disease_name} {conf:.2f}%", fill="red", font=font)
    
    return image

# ฟังก์ชันดึงข้อมูลโรคจาก MySQL
def get_disease_info(disease_name):
    disease_mapping = {
        'Algal Leaf Spot': 'โรคใบจุดสาหร่าย',
        'Leaf Blight': 'โรคใบไหม้',
        'Leaf Spot': 'โรคใบจุด',
        'No Disease': 'ใบสมบูรณ์',
        'โรคใบจุดสาหร่าย': 'โรคใบจุดสาหร่าย',
        'โรคใบไหม้': 'โรคใบไหม้',
        'โรคใบจุด': 'โรคใบจุด',
        'ใบสมบูรณ์': 'ใบสมบูรณ์'
    }

    # ถ้ามีชื่อโรคที่พิมพ์มาอยู่ใน mapping จะใช้ชื่อโรคนั้นเลย
    db_disease_name = disease_mapping.get(disease_name, None)

    if db_disease_name is None:
        return None  # ถ้าไม่พบการจับคู่ชื่อโรคจะส่งค่า None กลับไป

    # เชื่อมต่อฐานข้อมูล MySQL
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='woon043697',
        database='durian_project',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM durian_disease WHERE name = %s"
            cursor.execute(sql, (db_disease_name,))  # ค้นหาชื่อโรคใน MySQL
            result = cursor.fetchone()
            return result
    finally:
        connection.close()

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    image_id = event.message.id
    message_content = line_bot_api.get_message_content(image_id)
    image = Image.open(BytesIO(message_content.content))

    # ทำนายโรคจากภาพ
    results = model.predict(image)
    image_with_boxes = draw_boxes(image.copy(), results[0])

    # บันทึกภาพในโฟลเดอร์ static
    image_with_boxes.save('static/received_image.jpg')

    # ดึงข้อมูลโรคจาก MySQL
    cls = int(results[0].boxes[0].cls[0].item())
    disease_name = results[0].names[cls]
    disease_info = get_disease_info(disease_name)

    if disease_info:
        reply_text = (
            f"ชื่อโรค: {disease_info['name']}\n\n"
            f"สาเหตุ: {disease_info['cause']}\n\n"
            f"อาการ: {disease_info['symptoms']}\n\n"
            f"การรักษา: {disease_info['treatment']}\n\n"
            f"ข้อมูลเพิ่มเติม: {disease_info['additional_info']}"
        )
    else:
        reply_text = "ไม่พบข้อมูลโรคนี้ในระบบ"

    line_bot_api.reply_message(
        event.reply_token,
        [TextSendMessage(text=reply_text),
         ImageSendMessage(
             original_content_url="  https://c7b2-2001-fb1-189-fb2a-993d-3154-2f6d-988e.ngrok-free.app/static/received_image.jpg",
             preview_image_url="  https://c7b2-2001-fb1-189-fb2a-993d-3154-2f6d-988e.ngrok-free.app/static/received_image.jpg"
         )]
    )

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.strip()  # ข้อความที่ผู้ใช้ส่งมา

    # ถ้าผู้ใช้พิมพ์ "คำแนะนำเพิ่มเติม" ให้ Python ไม่ตอบอะไรเลย
    if user_message == "คำแนะนำเพิ่มเติม":
        return  # ไม่ให้ตอบกลับอะไรเลย เพราะตั้งค่าใน LINE Dev แล้ว

    # ตรวจสอบว่าผู้ใช้พิมพ์ว่า "สอบถามโรคใบทุเรียนจาก AI"
    if user_message == "สอบถามโรคใบทุเรียนจาก AI":
        reply = "คุณสามารถส่งรูปใบทุเรียนที่เป็นโรคมาให้เราได้เลยครับ 😃"
    else:
        disease_info = get_disease_info(user_message)  # ค้นหาข้อมูลโรคใน MySQL

        if disease_info:
            reply = (
                f"ชื่อโรค: {disease_info['name']}\n\n"
                f"สาเหตุ: {disease_info['cause']}\n\n"
                f"อาการ: {disease_info['symptoms']}\n\n"
                f"การรักษา: {disease_info['treatment']}\n\n"
                f"ข้อมูลเพิ่มเติม: {disease_info['additional_info']}"
            )
        else:
            reply = "ขออภัย ไม่พบข้อมูลโรคนี้ในระบบ กรุณาลองใหม่อีกครั้ง"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
