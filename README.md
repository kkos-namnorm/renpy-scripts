# renpy-scripts
ya_translate.py - a script for automatic text translation for your Ren'Py game using Yandex Cloud Transle.
More info about Yandex Translate - https://cloud.yandex.ru/services/translate

# Prerequisites
1. Generate all the translations for your game - https://www.renpy.org/doc/html/translation.html
2. If needed, update default interface translations
3. Sign up or in https://cloud.yandex.com/, using Yandex ID (https://yandex.ru/id/about) or SSO
4. Create folder in Yandex Cloud and get folder-id https://cloud.yandex.ru/docs/resource-manager/operations/folder/get-id
5. Get OauthToken https://cloud.yandex.ru/docs/iam/operations/iam-token/create
6. Put some money on your billing account - https://cloud.yandex.ru/docs/billing/payment/

# Usage

```
$ python3 ya_translate.py -h
usage: ya_translate.py [-h] [-f FOLDER_ID] [-o OAUTHTOKEN] [-l LANGUAGECODE] [-t TRANSLATIONFOLDER]

options:
  -h, --help            show this help message and exit
  -f FOLDER_ID, --folder_id FOLDER_ID
                        Yandex Cloud folder id. Doc - https://cloud.yandex.ru/docs/resource-
                        manager/operations/folder/get-id
  -o OAUTHTOKEN, --OauthToken OAUTHTOKEN
                        OauthToken, needed for IAM-token. Doc - https://cloud.yandex.ru/docs/iam/operations/iam-
                        token/create
  -l LANGUAGECODE, --LanguageCode LANGUAGECODE
                        The language we need to translate into. Must be one of ISO 639-1. Doc -
                        https://cloud.yandex.ru/docs/translate/operations/list
  -t TRANSLATIONFOLDER, --translationFolder TRANSLATIONFOLDER
                        Translation folder of your Ren'Py game. Should end on /. For example /mnt/d/degraman/game/tl/
```

example
```
$ python3 ya_translate.py -f b1111111111111111111 -o y1111 -l en -t /mnt/d/degraman/game/tl/
```

# Pricing
Yandex Translate is not free, but pretty cheap. As of Feb'23 1M symbols cost ~$4, proof - https://cloud.yandex.com/services/translate?state=563a00739c4e#calculator