class DualCaseSet():
    def __init__(self, items: list[str] | tuple[str]):
        self.__items: set[str] = set(items)
        self.__itemsUpper: dict[str] = {}

        for item in items: self.__itemsUpper[item.upper()] = item

    def __iter__(self):
        return iter(self.__items)

    @property
    def Methods(self):
        return self.__items

    @property
    def MethodsUpper(self):
        return set(self.__itemsUpper.keys())
    
    def isIn(self,
             item: str,
             CaseSensitive: bool = True) -> str | None:
        """Check whether the string is in the collection, Case Sensitive by Default.

        Args:
            item (str): _description_
            CaseSensitive (bool, optional): _Case Sensitive Or Not._ Defaults to True.

        Returns:
            bool: Inside -> True | NotInside -> False
        """
        match CaseSensitive:
            case True:
                if item in self.__items: return item
                else: return None
            case False:
                if item.upper() in self.__itemsUpper: return self.__itemsUpper[item.upper()]
                else: return None