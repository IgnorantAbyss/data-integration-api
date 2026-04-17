import datetime

from app.result.result import ValidateResult

def input_validate(length:list, option:list, input_string, allow_noinput=False):
    n = len(input_string)
    if not allow_noinput and n < 1:
        print('尚未輸入')
        return ValidateResult.error_result(
            code='N001',
            error_type='No input',
            message='No input'
        )
    # 輸入長度驗證(長度指定、非允許noinput)
    if length:
        # 非允許noinput 且長度不在範圍
        if not allow_noinput:
            if n not in length:
                print('長度錯誤')
                return ValidateResult.error_result(
                    code='L001',
                    error_type='Length Error',
                    message = 'Input Length Error',
                    )
        # 允許noinput 且有輸入長度
        else:
            if n and n not in length:
                print('長度錯誤')
                return ValidateResult.error_result(
                    code='L001',
                    error_type='Length Error',
                    message = 'Input Length Error',
                    )
    # 選項驗證
    if option:
        if input_string not in option:
            print('選項錯誤')
            return ValidateResult.error_result(
            code='O001',
            error_type='Option Error',
            message = 'Input not in options',
            )
        
    return ValidateResult.success_result(
        value=input_string,
        message='input_validate success'
        )

def date_validate(input_string):
    n = len(input_string)
    if n == 6:
        original_year = int(input_string[:2])
        year = original_year + 1911
    elif n == 7:
        original_year = int(input_string[:3])
        year = original_year + 1911
    else:
        original_year = int(input_string[:4])
        year = original_year
    month = int(input_string[-4:-2])
    day = int(input_string[-2:])

    roc = str(year-1911)+''.join(['0'+str(i) if i<10 else str(i) for i in [month,day]])
    common = str(year)+''.join(['0'+str(i) if i<10 else str(i) for i in [month,day]])
    try:
        datetime.date(year,month,day)
    except ValueError:
        print('日期錯誤')
        return ValidateResult.error_result(
            code='D001',
            error_type='Date Error', 
            message='Date Error')

    return ValidateResult.success_result(value=str(original_year)+''.join(['0'+str(i) if i<10 else str(i) for i in [month,day]]),
                                         message='Valid Date',
                                         data={'ROC':roc,'common':common}
                                         )
# {'Status':'OK','Value':''.join(['0'+str(i) if i<10 else str(i) for i in [original_year,month,day]])}


if __name__ =='__main__':

    year = 64
    original_year = year #- 1911
    month = 4
    day = 1
    d = ''.join(['0'+str(i) if i<10 else str(i) for i in [original_year,month,day]])
    print(d)
    # datetime.date(year,month,day)
    r = date_validate(d)
    print(r)
        
        