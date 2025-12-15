from PythonProject5.src.enums_item.const_url import ConstURL

class ItemsURLs:
    @staticmethod
    def base_url():
        return ConstURL.BASE_URL.value

    @classmethod
    def auth_endpoint(cls):
        return ConstURL.LOGIN_URL.value

    @classmethod
    def items_endpoint(cls):
        return ConstURL.ITEMS_URL.value

    @classmethod
    def items_endpoint_id(cls, id_item):
        return cls.items_endpoint()+ str(id_item)
