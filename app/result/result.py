import dataclasses

@dataclasses.dataclass
class ValidateResult:
    status: str = ""
    code: str = ""
    value: str = ""
    error_type: str = ""
    message: str = ""
    data : dict = dataclasses.field(default_factory=dict)


    def to_JSON(self):
        return dataclasses.asdict(self)
    
    @staticmethod
    def success_result(value="", message="", data={}):
        return ValidateResult(
            status = 'SUCCESS',
            code = '0000',
            value = value,
            error_type = '',
            message = message,
            data = data
        ).to_JSON()
    
    @staticmethod
    def error_result(code, error_type, message=''):
        return ValidateResult(
            status = 'ERROR',
            code = code,
            value = '',
            error_type = error_type,
            message = message
        ).to_JSON()
    
    
@dataclasses.dataclass
class DB_result:
    status: str
    message: str = ''
    detail: str = ''
    data: dict = dataclasses.field(default_factory=dict)

    def to_JSON(self):
        return dataclasses.asdict(self)
    
    @staticmethod
    def DB_error(message, detail, data):
        return DB_result(
            status = 'ERROR',
            message = message,
            detail = detail,
            data = data
        ).to_JSON()
    
    @staticmethod
    def DB_success(message, data):
        return DB_result(
            status = 'SUCCESS',
            message = message,
            data = data
        ).to_JSON()
        

if __name__ == '__main__':
    a = ValidateResult()
    print(a.success_result(value='123',message='test').to_JSON())
    print(a.error_result(code='testerror',error_type='length error',message='test').to_JSON())