from pydantic import BaseModel

class ContactUpdateItem(BaseModel):
    name: str
    phone: str
    address: str
    # 添加更多的联系人属性