# scrapy-googleauth

## 安裝方法

使用 pip 安裝

    $ pip install scrapy-googleauth

或者使用 pipenv 安装

    $ pipenv install scrapy-googleauth

## 配置

1. 在 Scrapy 中的 settings.py 加入：

        GOOGLE_AUTH_SCOPES = ['YOUR_GOOGLE_ANALYTICS_SCOPE']
        GOOGLE_AUTH_CREDENTIAL_PATH = 'YOUR_GOOGLE_CREDENTIAL_CONFIG.json'

    请注意 GOOGLE_AUTH_CREDENTIAL_PATH 是 Google 的服务账号秘钥，请根据 settings.py 所在的目录设置相对路径

2. 在 Scrapy 中的 settings.py 配置中间件：

        DOWNLOADER_MIDDLEWARES = {
            'googleauth.googleauth.GoogleAuthDownloaderMiddleware': 543
        }

    或者在 Spider 的 custom_settings 中配置：

        custom_settings = {
            'DOWNLOADER_MIDDLEWARES': {
                'googleauth.googleauth.GoogleAuthDownloaderMiddleware': 543
            }
        }

3. 配置完成，可以使用 Google API 抓取数据了

## 备注

Google Report API：[https://developers.google.com/analytics/devguides/reporting/core/v3](https://developers.google.com/analytics/devguides/reporting/core/v3)