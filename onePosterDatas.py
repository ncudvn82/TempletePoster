import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import json

def main(no, path):
    # 读取原始 JSON 文件
    with open('content_all.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        print(data[no]["_subtable_1003253"].values())

    for load_dict in data[no]["_subtable_1003253"].values():
        documentNo = load_dict['編號']
        f = open(f'./{path}/documents/txt/{documentNo}.txt', 'w', encoding="utf-8")
        f.write(load_dict['編號'] + '\n')
        f.write(load_dict['日期'] + '\n')
        f.write(load_dict['標題'] + '\n')
        f.write(load_dict['作者'] + '\n')
        f = open(f'./{path}/documents/txt/{documentNo}.md', 'w', encoding="utf-8")
        f.write(load_dict['內容'])

    def get_filename(path):
        return path.split('@')[-1] if '@' in path else path

    # 创建新的 JSON 结构
    print(data[no])
    new_data = {
        "siteTitle": data[no]["主題"],
        "navigation": [
            {"label": "Introduction", "link": "#intro"},
            {"label": "Speakers", "link": "#speakers"},
            {"label": "Agenda", "link": "#agenda"},
            {"label": "Documents", "link": "#documents"},
            {"label": "FAQ", "link": "#faq"},
            {"label": "Register", "link": "#register"}
        ],
        "languages": [
            {"label": "English", "code": "en", "active": True},
            {"label": "中文", "code": "zh", "active": False}
        ],
        "hero": {
            "title": data[no]["主題"],
            "date": data[no]["活動時間"].split()[0],  # 只取日期部分
            "ctaButton": {"text": "Register Now", "link": "#register"},
            "backgroundImage": f"./images/{get_filename(data[no]['image'])}"
        },
        "introduction": {
            "title": data[no]["Introduction Title"],
            "content": data[no]["Introduction"],
            "image": f"./images/intro-image.jpg"
        },
        "speakers": {
            "title": "Speakers",
            "list": [
                {
                    "name": speaker["講者"],
                    "photo": f"./images/{get_filename(speaker['Image'])}",
                    "title": speaker["title"],
                    "description": speaker["introduction"]
                } for speaker in data[no]["_subtable_1003256"].values()
            ]
        },
        "agenda": {
            "title": "Agenda",
            "image": f"./images/{get_filename(data[no]['Agenda'])}"
        },
        "documents": {
            "title": "Documents",
            "items": [
            ]
        },
        "faq": {
            "title": "FAQ",
            "items": [
                {
                    "question": faq["FAQ"],
                    "answer": faq["Answer"]
                } for faq in data[no]["_subtable_1003254"].values()
            ]
        },
        "registration": {
            "title": "Registration",
            "options": [
                {"link": site["報名網址"],
                 "image": f"./images/{get_filename(site['Image'])}"
                 } for site in data[no]["_subtable_1003255"].values()
            ],
            "eventDate": data[no]["活動時間"]
        },
        "footer": {
            "organizer": {"title": "Organizer", "image": f"./images/{get_filename(data[no]['Organizor'])}"},
            "coOrganizer": {"title": "Co-organizer", "image": f"./images/{get_filename(data[no]['Co-organizor'])}"},
            "sponsor": {"title": "Sponsor", "image": f"./images/{get_filename(data[no]['Sponsor'])}"},
            "contact": {
                "title": "Contact Us",
                "phone": "+886-2-27322701",
                "address": "3F.-2, No. 56, Lane 258, Ruiguang Rd, Neihu District, Taipei City"
            }
        }
    }

    # 保存新的 JSON 文件
    with open(f'./{path}/content.json', 'w', encoding='utf-8') as file:
        json.dump(new_data, file, ensure_ascii=False, indent=4)


main("0", "Avater Medicine 2023")

