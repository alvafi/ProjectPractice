class UserInfo:

    def __init__(self, name : str, surname : str, patronymic : str, email: str) -> None:
        self.__name = name
        self.__surname = surname
        self.__patronymic = patronymic
        self.__email = email

    def GetName(self) -> str:
        return self.__name

    def GetSurname(self) -> str:
        return self.__surname

    def Getpatronymic(self) -> str:
        return self.__patronymic

    def GetEmail(self) -> str:
        return self.__email