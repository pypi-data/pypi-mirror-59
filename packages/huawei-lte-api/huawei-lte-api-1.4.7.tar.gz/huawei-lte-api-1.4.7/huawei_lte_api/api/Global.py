
from huawei_lte_api.ApiGroup import ApiGroup


class Global(ApiGroup):
    def module_switch(self) ->dict:
        return self._connection.get('global/module-switch')
