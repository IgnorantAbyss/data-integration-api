from pydantic import BaseModel


# 定義 API 預期收到的 JSON 結構
class input_request(BaseModel):
    length: list
    option: list = []
    allow_noinput: bool = False
    input_string: str


class ID_request(BaseModel):
    id_digits: str


class date_request(BaseModel):
    input_date: str


class user_data_insert(BaseModel):
    call_id : str
    id : str = ''
    acc : str = ''
    pwd_verified : bool = False


class user_data_select(BaseModel):
    call_id : str