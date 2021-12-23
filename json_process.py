# https://blog.csdn.net/hjxu2016/article/details/79109407
# https://codertw.com/%E7%A8%8B%E5%BC%8F%E8%AA%9E%E8%A8%80/356901/

import json


def rank(data_dict, index):
    test = './rank.json'
    # 劇情介紹不能超過300字
    if len(data_dict['劇情介紹']) > 299:
        data_dict['劇情介紹'] = data_dict['劇情介紹'][0:295] + "..."

    data_dict = {
        'rank': index,
    }

    temp_dict = {}  # template_dict
    temp_dict["type"] = "bubble"
    temp_dict["hero"] = {
        "type": "image",
        "url": data_dict['電影海報'],
        "size": "full",
        "aspectRatio": "3.95:5.6"}

    message_content = [
        {
            "type": "text",
            "text": data_dict['片名'],
            "size": "lg",
            "weight": "bold"
        },
        {
            "type": "text",
            "text": "上映日期：" + data_dict['上映日期']
        },
        {
            "type": "text",
            "text": "片　　長：" + data_dict['片長']
        },
        {
            "type": "text",
            "text": "發行公司：" + data_dict['發行公司']
        },
        {
            "type": "text",
            "text": "導　　演：" + data_dict['導演']
        },
        {
            "type": "button",
            "action": {
                "type": "message",
                "label": "劇情介紹",
                "text": data_dict['劇情介紹']  # 不能大於300
            },
            "color": "#FF6B6E",
            "style": "primary",
            "margin": "lg"
        },
        {
            "type": "button",
            "action": {
                "type": "uri",
                "label": "更多資訊",
                "uri": data_dict['連結']
            },
            "color": "#A17DF5",
            "style": "primary",
            "margin": "lg"
        }
    ]

    if len(eval(data_dict['劇照'])) != 0:
        data_dict['action'] = '劇照'
        message_content.append(
            {
                "type": "button",
                "action": {
                    "type": "postback",
                    "label": "劇照",
                    "data": json.dumps(data_dict)
                    # "uri": data_dict['連結']
                },
                "color": "#66CDAA",
                "style": "primary",
                "margin": "lg"
            }
        )

    data_dict['action'] = '訂票'
    message_content.append(
        {
            "type": "button",
            "action": {
                "type": "postback",
                "label": "訂票",
                "data": json.dumps(data_dict)
            },
            "color": "#5c8dff",
            "style": "primary",
            "margin": "lg"
        }
    )

    temp_dict["body"] = {
        "type": "box",
        "layout": "vertical",
        "contents": message_content
    }

    with open(test, 'w', encoding='utf-8') as f:
        json.dump(temp_dict, f, ensure_ascii=False, indent=4)
