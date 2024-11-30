import os
import json


class AutoCibusUser:
    def __init__(self, cibus_email, cibus_password=None, wolt_wtoken=None, wolt_wrtoken=None):
        self.cibus_email = cibus_email  # lowercase all email

        # TODO: CHANGE FETCHING OF CREDS TO BE IN RUNTIME
        self.__cibus_password = cibus_password
        self.__wolt_wtoken = wolt_wtoken
        self.__wolt_wrtoken = wolt_wrtoken

    def toDICT(self):
        return {
            "cibus_email": self.cibus_email,
            "cibus_password": self.__cibus_password,
            "wolt_wtoken": self.__wolt_wtoken,
            "wolt_wrtoken": self.__wolt_wrtoken
        }

