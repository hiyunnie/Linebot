from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy
from flask import request, abort, render_template
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, PostbackEvent, TextSendMessage, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn
from urllib.parse import parse_qsl
import datetime
import time


line_bot_api = LineBotApi('/fytLeSdoje4jJ68QE6UitD0NWa1hl8E1kz+my2NWdWfZuLVs1L4xqhEAYt/I4l4nXgkprjYe3QxgEljRqbnl4K/P4duxVAyvnhiv+Eh0q1mM4vyL/bNr5UZnj0+eL8FXVhdyBf5HwQFPLoP5OQYlAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6d032577439fb7b5515aaac93d30ff5b')

# 定義 PostgreSQL 連線字串
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:asd860108@127.0.0.1:5432/Admin_data2'
db = SQLAlchemy(app)



# 重置資料庫
@app.route('/createdb')
def createdb():
    sql = """
    DROP TABLE IF EXISTS userlist, booking;

    CREATE TABLE userlist (
    id serial NOT NULL,
    uid character varying(50) NOT NULL,
    LINEname character varying(20) NOT NULL,
    PRIMARY KEY (id));
    
    
    CREATE TABLE gogg (
    id serial NOT NULL,
    bid character varying(50) NOT NULL,
    LINEname character varying(20) NOT NULL,
    location character varying(20) NOT NULL,
    information character varying(20) NOT NULL,
    PRIMARY KEY (id));


    CREATE TABLE booking (
    id serial NOT NULL,
    bid character varying(50) NOT NULL,
    LINEname character varying(50) NOT NULL,
    foodamount1 character varying(20) NOT NULL,
    foodamount2 character varying(20) NOT NULL,
    foodamount3 character varying(20) NOT NULL,
    foodamount4 character varying(20) NOT NULL,
    foodamount5 character varying(20) NOT NULL,
    stuff1 character varying(20) NOT NULL,
    stuff2 character varying(20) NOT NULL,
    stuff30 character varying(20) NOT NULL,
    stuff31 character varying(20) NOT NULL,
    stuff32 character varying(20) NOT NULL,
    stuff33 character varying(20) NOT NULL,
    stuff34 character varying(20) NOT NULL,
    stuff4 character varying(20) NOT NULL,
    datein character varying(20) NOT NULL,
    date character varying(20) NOT NULL,
    PRIMARY KEY (id))
    """
    db.engine.execute(sql)    
    return "資料表建立成功！"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# # 定義 LIFF ID
liffid = '1656983179-Epj1Y7dB'
# #LIFF靜態頁面
@app.route('/index')
def index():
 	return render_template('Form3.html', liffid = liffid)

    
# # 定義 LIFF ID
liffid2 = '1656983179-9m8JoEvY'
# #LIFF靜態頁面
@app.route('/indexx')
def indexx():
 	return render_template('registeform.html', liffid = liffid2)
 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    line_name = profile.display_name
    
    # sql_cmd = "select * from userlist where uid='" + user_id + "'"
    # query_data = db.engine.execute(sql_cmd)
   
    # if len(list(query_data)) == 0:
    #       sql_cmd = "insert into userlist (uid,LINEname) values('" + user_id + "','" + line_name + "');"
    #       db.engine.execute(sql_cmd)
          
    mtext = event.message.text
    if mtext == '我要下單':
        sendBooking(event, user_id,line_name)
        
    elif mtext == '訂單查詢':
        sendCancel(event, user_id)
    elif mtext == '營業資訊':
        sendCarousel(event)
    elif mtext[:3] == '###' and len(mtext) > 3:  #處理LIFF傳回的FORM資料
        manageForm(event, mtext, user_id,line_name)
    elif mtext[:3] == '@@@' and len(mtext) > 0:  #處理LIFF傳回的FORM資料
        RegisterForm(event, mtext, user_id,line_name)
    elif mtext == '@reset':
        createdb()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='reset！'))
    elif mtext == '@error':
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='你已放棄取消訂單！'))



@handler.add(PostbackEvent)  #PostbackTemplateAction觸發此事件
def handle_postback(event):
    backdata = dict(parse_qsl(event.postback.data))  #取得Postback資料
    if backdata.get('action') == 'yes':
        sendYes(event, event.source.user_id)
    elif backdata.get('action') == 'no':
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='你已放棄取消訂單！'))
    elif backdata.get('action') == 'orderagain':
        sendagain(event)
    elif backdata.get('action') == 'noorder':
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='期待您下次預訂！'))
    elif backdata.get('action') == 'phone':
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='0922658688'))
    elif backdata.get('action') == 'register':
        registry(event, event.source.user_id)
    elif backdata.get('action') == 'opentime':
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='24H'))

def registry(event, user_id):  
    try:
        # sql_cmd = "select * from booking where bid='" + user_id + "'"
        # query_data = db.engine.execute(sql_cmd)
            
        message = TemplateSendMessage(
            alt_text = "新戶登錄",
            template = ButtonsTemplate(
                thumbnail_image_url='https://cdn.bella.tw/indeximage/c8A0POweZXXjZ9qndIODJnqtBIFFAnB11TcdPlOR.jpeg',
                title='新戶登錄',
                text='新用戶您好！請您在第一次下單前，先點擊下方註冊鈕進行註冊。',
                actions=[
                    URITemplateAction(label='新戶登錄', uri='https://liff.line.me/' + liffid2)  #開啟LIFF讓使用者輸入訂房資料
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)

    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def sendagain(event):  
    try:    
        message = TemplateSendMessage(
            alt_text = "食材下單",
            template = ButtonsTemplate(
                thumbnail_image_url='https://cdn.bella.tw/indeximage/c8A0POweZXXjZ9qndIODJnqtBIFFAnB11TcdPlOR.jpeg',
                title='食材下單',
                text='點擊下單即可開始預訂。',
                actions=[
                    URITemplateAction(label='食材下單', uri='https://liff.line.me/' + liffid)  #開啟LIFF讓使用者輸入訂房資料
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def sendBooking(event, user_id,line_name):  
    try:
        sql_cmd = "select * from gogg where bid='" + user_id + "'"
        query_data = db.engine.execute(sql_cmd)
        
        if len(list(query_data)) != 0:        
            message = TemplateSendMessage(
                alt_text = "食材下單",
                template = ButtonsTemplate(
                    thumbnail_image_url='https://cdn.bella.tw/indeximage/c8A0POweZXXjZ9qndIODJnqtBIFFAnB11TcdPlOR.jpeg',
                    title='食材下單',
                    text='點擊下單即可開始預訂。',
                    actions=[
                        URITemplateAction(label='食材下單', uri='https://liff.line.me/' + liffid)  #開啟LIFF讓使用者輸入訂房資料
                    ]
                )
            )
        else:  #已有訂房記錄
            message = TextSendMessage(
                text = '請先進去新戶註冊!'
            )
            
            # message = TemplateSendMessage(  #顯示確認視窗
            #     alt_text='提醒您',
            #     template=ConfirmTemplate(
            #         text='您已有訂單在處理中。確定要下單嗎？',
            #         actions=[
            #             PostbackTemplateAction(  #按鈕選項
            #                 label='是',
            #                 data='action=orderagain'
            #             ),
            #             PostbackTemplateAction(
            #                 label='否',
            #                 data='action=noorder'
            #            )
            #         ]
            #     )
            # )
        line_bot_api.reply_message(event.reply_token,message)

    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def manageForm(event, mtext, user_id,line_name):  #處理LIFF傳回的FORM資料
    try:
        flist = mtext[3:].split('/')  #去除前三個「#」字元再分解字串
        #roomtype = flist[0]  #取得輸入資料
        today = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        amount1 = flist[0]
        amount2 = flist[1]
        amount3 = flist[2]
        amount4 = flist[3]
        amount5 = flist[4]   
        amount11= flist[5]
        amount12= flist[6]
        amount130= flist[7]
        amount131= flist[8]
        amount132= flist[9]
        amount133= flist[10]
        amount134= flist[11]
        amount14= flist[12]
        in_date = flist[13]
        
        #out_date = flist[3]
        sql_cmd = "insert into booking (bid,LINEname, foodamount1,foodamount2,foodamount3,foodamount4,foodamount5, stuff1 ,stuff2 ,stuff30 ,stuff31,stuff32,stuff33,stuff34 ,stuff4 ,datein,date) values('" + user_id + "','" + line_name + "', '" + amount1 + "', '" + amount2 + "', '" + amount3 + "', '" + amount4 + "',  '" + amount5 + "','" + amount11 + "','" + amount12 + "','" + amount130 + "','" + amount131 + "','" + amount132 + "','" + amount133 + "','" + amount134 + "','" + amount14 + "','" + in_date + "','" + today + "');"
        db.engine.execute(sql_cmd)
        
        text1 = "您的訂單已預訂成功！\n"
        text1 += "您在"+today+"訂購：\n"
        if amount1!= '0':
            text1 += "\n臭豆腐數量：" + amount1
        if amount2!= '0':    
            text1 += "\n冬粉數量：" + amount2
        if amount3!= '0':
            text1 += "\n泡菜數量：" + amount3
        if amount4!= '0':
            text1 += "\n豆皮數量：" + amount4
        if amount5!= '0':
            text1 += "\n酸白菜數量：" + amount5 
        if amount11!= '0':
            text1 += "\n酒精膏數量：" + amount11             
        if amount12!= '0':
            text1 += "\n面紙數量：" + amount12               
        if amount130!= '0':
            text1 += "\n1000cc湯杯數量：" + amount130
        if amount131!= '0':
            text1 += "\n1000cc湯杯蓋數量：" + amount131
        if amount132!= '0':
            text1 += "\n260cc湯杯蓋數量：" + amount132
        if amount133!= '0':
            text1 += "\n260cc湯杯蓋數量：" + amount133
        if amount134!= '0':
            text1 += "\n850cc湯杯蓋數量：" + amount134
        if amount14!= '0':
            text1 += "\n手提袋數量：" + amount14                  
        text1 += "\n\n運送日期：" + in_date
        
        message = TextSendMessage(  #顯示訂房資料
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def RegisterForm(event, mtext, user_id,line_name):  #處理LIFF傳回的FORM資料
    try:
        flist = mtext[3:].split('/')  #去除前三個「#」字元再分解字串

        LOCA = flist[0]
        INFO = flist[1]
        
        text1 = "您的註冊已完成！\n"
        text1 += "\n店家所在地區：" + LOCA
        text1 += "\n店家資訊：" + INFO

        sql_cmd = "insert into gogg (bid,LINEname,location,information) values('" + user_id + "','" + line_name + "','" + LOCA + "','" + INFO + "');"
        db.engine.execute(sql_cmd)

        
        message = TextSendMessage(  #顯示訂房資料
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

# def sendYes(event):
#     try:       
#         message = TemplateSendMessage(
#             alt_text = "食材下單",
#             template = ButtonsTemplate(
#                 thumbnail_image_url='https://cdn.bella.tw/indeximage/c8A0POweZXXjZ9qndIODJnqtBIFFAnB11TcdPlOR.jpeg',
#                 title='食材下單',
#                 text='點擊下單即可開始預訂。',
#                 actions=[
#                     URITemplateAction(label='食材下單', uri='https://liff.line.me/' + liffid)  #開啟LIFF讓使用者輸入訂房資料
#                 ]
#             )
#         )
#         line_bot_api.reply_message(event.reply_token, message)
#     except:
#         line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
        
def sendCarousel(event):  #轉盤樣板
    try:
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://imageproxy.icook.network/resize?background=255%2C255%2C255&height=675&nocrop=false&stripmeta=true&type=auto&url=http%3A%2F%2Ftokyo-kitchen.icook.tw.s3.amazonaws.com%2Fuploads%2Frecipe%2Fcover%2F338148%2Ff4fef7b0ed0fa0d3.jpg&width=1200',
                        title='最新商品',
                        text='近期新推出的訂單內容！',
                        actions=[
                            MessageTemplateAction(
                                label='商品資訊',
                                text='賣飲料'
                            ),
                            URITemplateAction(
                                label='相關網頁',
                                uri='http://www.ntu.edu.tw'
                            ),
                            PostbackTemplateAction(
                                label='回傳訊息',
                                data='action=sell&item=飲料'
                            ),
                        ]
                    ),
                    CarouselColumn(

                        thumbnail_image_url='https://cc.tvbs.com.tw/img/program/upload/2018/10/30/20181030170631-3f05f3b7.jpg',
                        title='公司聯絡方式',
                        text='若有需要專人服務請撥打電話',
                        actions=[
                            PostbackTemplateAction(
                                label='客服電話',
                                data='action=phone'
                            ),
                            PostbackTemplateAction(
                                label='新戶註冊',
                                data='action=register'
                            ),
                            PostbackTemplateAction(
                                label='營業時間',
                                data='action=opentime'
                            ),
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendCancel(event, user_id):  #取消訂房
    try:
        
        # sql_cmd = "select * from gogg where bid='" + user_id + "'"
        # data = db.engine.execute(sql_cmd)
        # if len(list(data)) == 0:
        #     message = TextSendMessage(
        #         text = '請先進去新戶註冊!'
        #     )
            
        # else:
            sql_cmd = "select * from booking where bid='" + user_id + "'"
            query_data = db.engine.execute(sql_cmd)
            bookingdata = list(query_data)
            numberorder = len(bookingdata)
            assstr = str(numberorder)
            assint = int(numberorder)
            
            if len(bookingdata) > 0:
                #text1 = "您的訂單資料如下：\n"
                time = bookingdata[assint-1][17]
                text1 = "您目前有" + assstr + "筆訂單正在處理，以下顯示最新的訂單\n\n"
    
                
                
                #idnum = bookingdata[assint-1][0]
                food1 = bookingdata[assint-1][3]
                food2 = bookingdata[assint-1][4]
                food3 = bookingdata[assint-1][5]
                food4 = bookingdata[assint-1][6]
                food5 = bookingdata[assint-1][7]
                stuff1 = bookingdata[assint-1][8]
                stuff2 = bookingdata[assint-1][9]
                stuff30 = bookingdata[assint-1][10]
                stuff31 = bookingdata[assint-1][11]
                stuff32 = bookingdata[assint-1][12]
                stuff33 = bookingdata[assint-1][13]
                stuff34 = bookingdata[assint-1][14]
                stuff4 = bookingdata[assint-1][15]
                delivery_date = bookingdata[assint-1][16]
                
                text1 += "您於"+time+"訂購 :"
                #text1 +="\n訂購日期：" + time
                if food1 != '0':
                    text1 += "\n臭豆腐：" + food1
                if food2 != '0':
                    text1 += "\n冬粉：" + food2
                if food3 != '0':
                    text1 += "\n泡菜：" + food3
                if food4 != '0':
                    text1 += "\n豆皮：" + food4
                if food5 != '0':
                    text1 += "\n酸白菜：" + food5
                if stuff1 != '0':
                    text1 += "\n酒精膏：" + stuff1
                if stuff2 != '0':
                    text1 += "\n面紙：" + stuff2
                if stuff30 != '0':
                    text1 += "\n1000cc湯杯：" + stuff30
                if stuff31 != '0':
                    text1 += "\n1000cc湯杯蓋：" + stuff31
                if stuff32 != '0':
                    text1 += "\n260cc湯杯：" + stuff32
                if stuff33 != '0':
                    text1 += "\n260cc湯杯蓋：" + stuff33
                if stuff34 != '0':
                    text1 += "\n850cc湯杯：" + stuff34
                if stuff4 != '0':
                    text1 += "\n手提袋：" + stuff4
                    
                text1 += "\n運送日期：" + delivery_date
                
                message = [
                    TextSendMessage(  #顯示訂房資料
                        text = text1
                    ),
                    TemplateSendMessage(  #顯示確認視窗
                        alt_text='取消訂單確認',
                        template=ConfirmTemplate(
                            text='你確定要取消這筆訂單嗎？',
                            actions=[
                                PostbackTemplateAction(  #按鈕選項
                                    label='是',
                                    data='action=yes'
                                ),
                                PostbackTemplateAction(
                                    label='否',
                                    data='action=no'
                               )
                            ]
                        )
                    )
                ]
            else:  #沒有訂房記錄
                message = TextSendMessage(
                    text = '您目前沒有訂單記錄！'
                )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def sendYes(event, user_id):  #處理取消訂房
    try:
        sql_cmd = "select * from booking where bid='" + user_id + "'"
        query_data = db.engine.execute(sql_cmd)
        bookingdata = list(query_data)
        numberorder = len(bookingdata)
        assint = int(numberorder)
            
        idnum = bookingdata[assint-1][0]
        idnum = str(idnum)
        sql_cmd = "delete from booking where id='" + idnum + "'"
        db.engine.execute(sql_cmd)
        
        sql_cmd = "select * from booking where bid='" + user_id + "'"
        query_data = db.engine.execute(sql_cmd)
        bookingdata = list(query_data)
        numberorder = len(bookingdata)
        assstr = str(numberorder)
        assint = int(numberorder)
        
        text1 = "您的這筆訂單已成功刪除。"
        if assint != 0:
            text1 += "\n還有"+assstr+"筆訂單在處理中。"
        elif assint == 0:
            text1 += "\n您目前已無訂單，若有需要請重新下訂。"
        message = TextSendMessage(
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

if __name__ == '__main__':
    app.run()
