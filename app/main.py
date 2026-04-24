from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from datetime import datetime
from sqlalchemy import select
import pyotp
import time

from app.service.Check_ID import get_ID_char
from app.module.input import input_validate, date_validate
from app.result.result import ValidateResult, DB_result
from app.service.API_request import get_working_day
from app.config.config import Settings
from app.schema.schema import input_request, ID_request, date_request, user_data_insert, user_data_select
# SQL
from app.config.database import Base, engine, SessionLocal
from app.model.ORM_model import user_data

app = FastAPI()

@app.get('/')
def read_root():
    return {"message": "API server is running"}

@app.post("/id/candidates")
# data: IdRequest
# 代表 FastAPI 會把收到的 JSON 解析成 IdRequest 物件。
def find_id_candidates(data: ID_request):
    input_string = data.id_digits
    print('收到字串:',input_string)
    valid_input = input_validate(length=[9],option=[],input_string=input_string)

    if valid_input.get('status',) == 'ERROR':
        return valid_input
    
    candidates = get_ID_char(valid_input['value'])
    if not candidates:
        return ValidateResult.error_result(
            code='ID01',
            error_type='Not valid ID',
            message='Not valid ID')

    print(candidates)
    result =  {
        "input": data.id_digits,
        "candidates": candidates,
        "count": len(candidates)
    }

    valid_input['data'] = result
    return valid_input

@app.post("/date/validate")
def check_date(data: date_request):
    input_date = data.input_date
    print('收到日期',input_date)
    valid_input = input_validate(length=[6,7,8],
                                option=[],
                                input_string=input_date,)
    if valid_input.get('status',) == 'ERROR':
        return valid_input
    
    valid_date = date_validate(valid_input['value'])
    return valid_date

@app.post("/input/validate")
def check_input(data: input_request):
    input_string = data.input_string
    length = data.length
    option = data.option
    allow_noinput = data.allow_noinput
    result = input_validate(length=length,
                            option=option,
                            input_string=input_string,
                            allow_noinput=allow_noinput)
    return result

@app.get("/apirequest/working_day")
def working_day():
    return get_working_day()

@app.get("/GC_OTP/api")
def get_OTP():
    setting = Settings()
    secret = setting.secret
    totp = pyotp.TOTP(secret, digits=6, interval=30)

    code = totp.now()
    print("目前 OTP:", code)
    
    # 目前 Unix timestamp（秒）
    current_time = int(time.time())
    remaining_seconds = totp.interval - (current_time % totp.interval)
    print('剩餘時間:',remaining_seconds)

    return {'code':code,'remaining_seconds':remaining_seconds}

@app.get("/GC_OTP", response_class=HTMLResponse)
def otp_page():
    # 回傳一整份 HTML
    # - 瀏覽器打開 /GC_OTP 時，會直接看到美化後頁面
    # - 這裡把 CSS 和 JavaScript 都直接寫進去，方便你先快速測試
    return """
    <!DOCTYPE html>
    <html lang="zh-Hant">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OTP 驗證碼</title>

        <style>
            /* 
            body:
            - 整個頁面的基本樣式
            - margin: 0 讓瀏覽器預設外距消失
            - min-height: 100vh 代表最小高度等於整個視窗高度
            - display: flex 搭配置中排版
            - justify-content: center 水平置中
            - align-items: center 垂直置中
            - background 使用漸層，看起來比較像真正介面
            - font-family 設定字體
            */
            body {
                margin: 0;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                font-family: "Microsoft JhengHei", Arial, sans-serif;
            }

            /*
            .card:
            - 中間那塊資訊卡片
            - background: 白底
            - padding: 內距，讓內容不要貼邊
            - border-radius: 圓角
            - box-shadow: 陰影，讓卡片有浮起來的感覺
            - text-align: center 文字置中
            - width 設定寬度
            */
            .card {
                background: white;
                padding: 40px 50px;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
                text-align: center;
                width: 420px;
                max-width: 90%;
            }

            /*
            .title:
            - 標題文字
            - font-size 放大
            - margin-bottom 增加與下方的距離
            */
            .title {
                font-size: 32px;
                font-weight: bold;
                color: #333;
                margin-bottom: 25px;
            }

            /*
            .otp:
            - OTP 顯示區
            - 字體放大，讓使用者一眼看到
            - letter-spacing 增加每個數字的間距
            - font-weight 加粗
            - color 改成深藍，視覺上更醒目
            */
            .otp {
                font-size: 56px;
                font-weight: bold;
                letter-spacing: 8px;
                color: #1e3c72;
                margin-bottom: 20px;
            }

            /*
            .countdown:
            - 倒數文字區
            - 字體比一般文字稍大
            - color 用灰色，避免搶走 OTP 主體注意力
            */
            .countdown {
                font-size: 24px;
                color: #555;
                margin-bottom: 10px;
            }

            /*
            .hint:
            - 補充提示文字
            - 字體較小
            - 顏色更淡一點
            */
            .hint {
                font-size: 14px;
                color: #888;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <div class="title">目前 OTP 驗證碼</div>

            <!-- 
            這裡先放預設文字
            - 畫面載入後，JavaScript 會把真正的 OTP 寫進去
            -->
            <div id="otp" class="otp">------</div>

            <!-- 
            剩餘秒數顯示區
            - 例如會顯示：剩餘時間：18 秒
            -->
            <div id="countdown" class="countdown">剩餘時間：-- 秒</div>

            <div class="hint">OTP 每 30 秒自動更新一次</div>
        </div>

        <script>
            // currentRemaining:
            // - 用來記錄目前還剩幾秒
            // - 之後 setInterval 每秒會把它減 1
            let currentRemaining = 0;

            // fetchOtp:
            // - 這個函式會去呼叫後端 /GC_OTP/api
            // - 拿到最新 OTP 和剩餘秒數後，更新畫面
            async function fetchOtp() {
                try {
                    // fetch("/GC_OTP/api"):
                    // - 向後端發出 GET 請求
                    const response = await fetch("/GC_OTP/api");

                    // 將回應解析成 JSON
                    const data = await response.json();

                    // 把 OTP 填進 id="otp" 的元素中
                    document.getElementById("otp").innerText = data.code;

                    // 更新目前剩餘秒數
                    currentRemaining = data.remaining_seconds;

                    // 立刻刷新倒數文字，避免畫面延遲
                    updateCountdownText();
                } catch (error) {
                    // 若 API 呼叫失敗，就在畫面上顯示錯誤訊息
                    document.getElementById("otp").innerText = "ERROR";
                    document.getElementById("countdown").innerText = "無法取得 OTP 資料";
                    console.error("取得 OTP 失敗:", error);
                }
            }

            // updateCountdownText:
            // - 單純負責把 currentRemaining 顯示到畫面上
            function updateCountdownText() {
                document.getElementById("countdown").innerText =
                    `剩餘時間：${currentRemaining} 秒`;
            }

            // 頁面一打開時，先抓一次 OTP
            fetchOtp();

            // setInterval(..., 1000):
            // - 每 1000 毫秒（1 秒）執行一次
            // - 這樣畫面上的倒數就會每秒更新
            setInterval(() => {
                // 如果 currentRemaining 大於 1
                // - 代表 OTP 還有效
                // - 就把秒數減 1
                if (currentRemaining > 1) {
                    currentRemaining -= 1;
                    updateCountdownText();
                } else {
                    // 如果剩餘秒數已經到 1 或 0
                    // - 代表快到期或已到期
                    // - 直接重新向後端抓最新 OTP
                    fetchOtp();
                }
            }, 1000);
        </script>
    </body>
    </html>
    """


@app.post("/DB_insert")
def DB_insert(datas : user_data_insert):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    insert_row = user_data(
        call_id=datas.call_id,
        ID=datas.id,
        acc=datas.acc,
        pwd_verified=datas.pwd_verified,
        write_time=current_time)
    print(insert_row)

    with SessionLocal() as s:
        try:
            s.add(insert_row)
            s.commit()
            print('新增資料成功:',insert_row)
            return DB_result.DB_success(
                message='新增資料成功',
                data={
                    'call_id':insert_row.call_id,
                    'ID':insert_row.ID,
                    'acc':insert_row.acc,
                    'pwd_verified':insert_row.pwd_verified,
                    'write_time':insert_row.write_time
                })

        except Exception as e:
            print('新增失敗',e)
            return DB_result.DB_error(
                message='新增失敗',
                detail=e,
                data={
                      'call_id':insert_row.call_id,
                      'ID':insert_row.ID,
                      'acc':insert_row.acc,
                      'pwd_verified':insert_row.pwd_verified,
                      'write_time':insert_row.write_time
                })


@app.post("/DB_select")
def DB_select(datas: user_data_select):
    cid = datas.call_id
    with SessionLocal() as s:
        try:
            row = s.scalar(select(user_data).where(user_data.call_id==cid))
            if row is None:
                print(f"查無資料: session_id={cid}")
                return DB_result.DB_error(
                    message='查無資料',
                    detail='',
                    data={'call_id':datas.call_id}
                )

            print('查詢成功:',row)
            return DB_result.DB_success(
                message='查詢成功',
                data={
                    "call_id": row.call_id,
                    "ID": row.ID,
                    "acc": row.acc,
                    "pwd_verified": row.pwd_verified,
                    "write_time": row.write_time
                })
        
        except Exception as e:
            print(f"查詢失敗: {e}")
            return DB_result.DB_error(
                message='查詢失敗',
                detail=e,
                data={'call_id':datas.call_id}
            )
