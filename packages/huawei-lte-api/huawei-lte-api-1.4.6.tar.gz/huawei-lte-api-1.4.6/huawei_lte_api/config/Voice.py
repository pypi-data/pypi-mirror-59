
from huawei_lte_api.ApiGroup import ApiGroup


class Voice(ApiGroup):
    def config(self):
        return self._connection.get('voice/config.xml', prefix='config')
