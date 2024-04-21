import UserInfo

class User:

    def __init__(self, login : str, id : int, conf_flag : bool, password : str) -> None:
        self.__login = login
        self.__id = id
        self.__user_info = UserInfo.UserInfo("", "", "", "")
        self.__conf_flag = conf_flag
        self.__password = password

    def AddUser_info(self, user_info : UserInfo.UserInfo) -> None:
        self.__user_info = user_info

    def GetLogin(self) -> str:
        return self.__login

    def GetId(self) -> int:
        return self.__id

    def GetConf_flag(self) -> bool:
        return self.__conf_flag

    def GetPassword(self) -> str:
        return self.__password

    def GetUser_info(self) -> UserInfo.UserInfo:
        return self.__user_info
