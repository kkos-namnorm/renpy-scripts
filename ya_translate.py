import requests
import os
import re
import ast
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-f", "--folder_id", dest="folder_id", help="""
Yandex Cloud folder id. Doc - https://cloud.yandex.ru/docs/resource-manager/operations/folder/get-id
""")
parser.add_argument("-o", "--OauthToken", dest="OauthToken", help="""
OauthToken, needed for IAM-token. Doc - https://cloud.yandex.ru/docs/iam/operations/iam-token/create
""")
parser.add_argument("-l", "--LanguageCode", dest="LanguageCode", help="""
The language we need to translate into. Must be one of ISO 639-1. Doc - https://cloud.yandex.ru/docs/translate/operations/list
""")
parser.add_argument("-t", "--translationFolder", dest="translationFolder", help="""
Translation folder of your Ren'Py game. Should end on /. For example /mnt/d/degraman/game/tl/
""")

args = parser.parse_args()


OauthToken = "{\"yandexPassportOauthToken\":\"" + args.OauthToken + "\"}"
url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
response = requests.post(url, data=OauthToken)
IAM_TOKEN = response.json()['iamToken']

def translate(lines, file):
    texts = []
    for i in range(0, len(lines)):
        row = lines[i]
        res = row.find("    #")
        if res == -1:
            res = row.find("    old \"")
        if res == -1:
            continue
        else:
            next_line_has_translation = re.search(r"^\s+\s(\w+\s)?\"\"", lines[i+1])
            if next_line_has_translation is not None:
                res = re.search(r"^\s+(#|old)\s(\w+\s)?\"(.*)\"", row)
                texts.append(res.group(3))
    if not texts:
        return
    else:
        body = {
            "targetLanguageCode": args.LanguageCode,
            "texts": texts,
            "folderId": args.folder_id,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(IAM_TOKEN)
        }

        response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
            json = body,
            headers = headers
        )

        os.rename(file, file +"_old")

        translation_file_new = open(file, 'w')
        tr_line = 0
        response_text = ast.literal_eval(response.text)

        for i in range(0, len(lines)):
            row = lines[i]
            res = re.search(r"^\s+\s(\w+\s)?\"\"", row)
            if res is None:
                translation_file_new.write(row)
                continue
            else:
                translated_text = response_text['translations'][tr_line]['text'].replace('"','\\"')
                translation_file_new.write(res.group(0)[:-1] + translated_text + "\"\n")
                tr_line = tr_line+1
        
        translation_file_new.close()
        os.remove(file +"_old")



for subdir, dirs, files in os.walk(args.translationFolder):
    for file in files:
        if file[-4:] == 'rpym' or file[-3:] == 'rpy':
            with open(os.path.join(subdir, file)) as infile:
                lines = infile.readlines()
            infile.close()
            translate(lines, os.path.join(subdir, file))