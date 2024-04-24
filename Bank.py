import Kit

class Bank:
    def __init__(self, bank_id : int, name : str) -> None:
        self.__bank_id = bank_id
        self.__name = name
        self.__kits = []

    def GetId(self) -> int:
        return self.__bank_id

    def GetName(self):
        return self.__name
    
    def GetKits(self):
        return self.__kits
    
    def AddKit(self, kit : Kit):
        self.__kits.append(kit)

    def SetName(self, new_bank_name : str) -> None:
        self.__name = new_bank_name

    def DeleteKit(self, kit : Kit) -> None:
        self.__kits.remove(kit)


    