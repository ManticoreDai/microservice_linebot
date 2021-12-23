from __future__ import unicode_literals
import os
from flask import Flask, request, abort  # , session
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import configparser

import random
import json

import json_process
import re
import pandas as pd


app = Flask(__name__)
#app.config['SECRET_KEY'] = '123456'

# LINE 聊天機器人的基本資料
try:
    # set in Heroku
    line_access_token = os.environ['line_access_token']
    line_secret = os.environ['line_secret']
except:
    print('read config.ini')
    config = configparser.ConfigParser()
    config.read('config.ini')
    line_access_token = config.get('line-bot', 'line_access_token')
    line_secret = config.get('line-bot', 'line_secret')


line_bot_api = LineBotApi(line_access_token)
handler = WebhookHandler(line_secret)


movies_df = pd.read_excel('./movies_info.xlsx')


@app.route("/", methods=['GET'])
def index():
    return "Good!"

# print(movies_df)
# 接收 LINE 的資訊


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        print(body, signature)
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'

# #此段可藉由user回覆LineBot後，便可取得user_id，有user_id，就能主動推撥(Push)訊息給user(尚未成熟)
# def get_id(event):
#     user_id = event.source.user_id
#     print("user_id =", user_id)

#     try:
#         line_bot_api.push_message(user_id, TextSendMessage(text="請輸入1~20的數字，查詢電影排行榜"))
#     except Exception as e:
#         print(e)


@handler.add(MessageEvent, message=TextMessage)
def movies(event):
    value_rank = re.compile(r'^排行榜 *(2[0]|1[0-9]|[1-9])$')
    result_rank = value_rank.match(event.message.text)
    if result_rank:
        id = eval(event.message.text[3:])
        movies_dict = get_movie(movies_df, rank=id)
        json_process.rank(movies_dict, id)
        FlexMessage = json.load(open('rank.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(
            'Movie Introduction', FlexMessage))

    #value_theater = re.compile(r'^排行榜 *(2[0]|1[0-9]|[1-9])$')
    if event.message.text == "電影院屏東":

        FlexMessage = json.load(
            open('theater_Pingtung.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(
            event.reply_token, FlexSendMessage('Theater Location', FlexMessage))

    elif event.message.text == "電影院高雄":
        FlexMessage = json.load(
            open('theater_Kaohsiung.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(
            event.reply_token, FlexSendMessage('Theater Location', FlexMessage))


@handler.add(PostbackEvent)
def handle_postback(event):
    data = json.loads(event.postback.data)
    id = int(data['rank'])
    action = data['action']
    print(data)

    if id > len(movies_df):
        id = len(movies_df)
    # poster(movies_df['劇照'][id])
    # TemplateMessage = json.load(open('poster.json','r',encoding='utf-8'))
    image_url = eval(movies_df['劇照'][id-1])[0]
    print("在這裡:"+image_url)

    if len(eval(movies_df['劇照'][id-1])) != 0:
        columns = [ImageCarouselColumn(
            image_url=eval(movies_df['劇照'][id-1])[i],
            action=MessageTemplateAction(
                label=movies_df['片名'][id-1],
                text="劇照"
            )
        ) for i in range(5)]
        carousel_template = ImageCarouselTemplate(columns=columns)

    line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
        alt_text="電影劇照", template=carousel_template))  # TemplateSendMessage('profile',TemplateMessage)


def get_movie(df, rank=1, col=None):
    if rank > len(df):
        rank = len(df)
    print(f'rank = {rank}, len(df) = {len(df)}')
    if col == None:
        res = {}
        res = df.iloc[rank-1].to_dict()
        return res
    if col in ("本周排名", "片名", "評分", "連結", '電影海報', "上映日期", "片長", "發行公司", "導演", "劇情介紹"):
        res = str(df.iloc[rank-1][col])
        return res
    else:
        print("無此資訊")


# line_bot_api.push_message("Ub7385e82f5a34b097e8a12ec38601723", TextSendMessage(text="請輸入1~20的數字，查詢電影排行榜"))

id = 1
movies_dict = get_movie(movies_df, rank=id)
json_process.rank(movies_dict, id)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
