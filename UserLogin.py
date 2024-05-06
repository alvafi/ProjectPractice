from flask_login import UserMixin


class UserLogin(UserMixin):
    def fromDB(self, user_id, db):
        self.__user = db.get_user_by_id(user_id)
        return self

    def Create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user['user_id'])

    def GetFirstName(self):
        return str(self.__user['first_name'])
    
    def GetMiddleName(self):
        return str(self.__user['middle_name'])
    
    def GetLastName(self):
        return str(self.__user['last_name'])
    

    def GetLogin(self):
        return self.__user['login'] if self.__user else "Без логина"

    def GetEmail(self):
        return self.__user['email'] if self.__user else "Без email"
