import shutil
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
from os import listdir
import json

from gitProcess import auto_git_process
import getRagicData
import gitMake
import fileInit
import checkTxt
import datetime
import onePosterDatas
import onePosterImage


def project_exists_locally(project_name, base_path):
    project_path = os.path.join(base_path, project_name)
    return os.path.exists(project_path)


def main():
    # get ragic
    n = getRagicData.main()
    files = listdir(".")
    folders = [item for item in files if os.path.isdir(os.path.join(".", item))]
    with open('content_all.json', 'r', encoding='utf-8') as file:
        datas = json.load(file)

    for i in range(n):
        dataTitle = datas[f"{i}"]["主題"]
        # 新海報長新網站(init)
        if not project_exists_locally(dataTitle, "."):
            dataTemplete = datas[f"{i}"]["templete"]
            gitMake.main(dataTitle)
            fileInit.main(f"./{dataTitle}", dataTemplete)

        # get
        # 生content.json .txt .md
        onePosterDatas.main(f"{i}", dataTitle)

        # add ./images
        onePosterImage.main(f"{i}", dataTitle)

        # checktxt...
        checkTxt.main(dataTitle)
        # add .
        # push
        now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))
        repo_path = f"./{dataTitle}"
        commit_message = f"Article Updated {now.strftime('%Y/%m/%d %H:%M:%S')}"

        success = auto_git_process(repo_path, commit_message)
        if success:
            print("Git process completed successfully")
        else:
            print("Git process failed or no changes to commit")



main()

