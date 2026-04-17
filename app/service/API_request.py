import requests
from datetime import datetime, date

from app.config import config
from app.result.result import ValidateResult

# 讀取設定
setting = config.Settings()
url = setting.Txnip

def get_working_day():
    today = datetime.now().year

    payload = {
        "TXN": {
                "TXNID": "fbivr\\EB852770",
                "SUB_FUNC_COD": "03",
                "INIT_NO": today
            }
    }

    try:
        response = requests.post(
                url,
                json=payload,
                timeout=5
            )

        response.raise_for_status()

        result = response.json()
        print(result)

        flag = result['TxBody']['BUS_DATE_FLG']

    except requests.exceptions.Timeout as e:
        # 如果超過 timeout 秒數還沒回應，就會進來這裡
        print("錯誤：請求逾時，對方主機可能太慢或無回應")
        print(e)
        return ValidateResult.error_result(code='T001',
                                           error_type='Time out',
                                           message='請求逾時')

    except requests.exceptions.HTTPError as e:
        # 如果 HTTP 狀態碼不是成功，例如 404 / 500
        print("HTTP 錯誤：", e)
        print("伺服器回應內容：", response.text)
        return ValidateResult.error_result(code='F001',
                                           error_type='bad request',
                                           message=e)

    except ValueError:
        # 如果 response.json() 解析失敗，代表回傳內容不是合法 JSON
        print("錯誤：伺服器回應不是合法 JSON")
        print("實際回應內容：", response.text)
        return ValidateResult.error_result(code='J001',
                                           error_type='JSON error',
                                           message=e)

    except Exception as e:
        # 其他未預期錯誤
        print("其他錯誤：", e)
        return ValidateResult.error_result(code='U001',
                                           error_type='unexpect error',
                                           message=e)


    day_of_year = int(date.today().strftime('%j'))
    print('今日為本年度第',day_of_year,'天')
    
    f = flag[day_of_year]
    m = '營業日' if f == ' ' else '非營業日'
    print('註記為',m)
    
    return ValidateResult.success_result(value=f,
                                         message=m
                                         )