class result():
    def __init__(self,
                 state: bool,
                 *args: any,
                 **kwargs: any):
        self.state: bool = state
        self.args: list = list(args)
        self.kwargs: dict = kwargs

    def __bool__(self):
        return self.state
    
    def __getitem__(self, Index: int | str):
        """_Used to obtain the contents of arrays and dictionaries._

        Args:
            Index (int | str): _description_

        Returns:
            _type_: _description_
        """
        if isinstance(Index, int): return self.args[Index]
        if isinstance(Index, str): return self.kwargs[Index]

    def __repr__(self):
        if all((self.args, self.kwargs)) or not any((self.args, self.kwargs)):
            return str(self.args)+str(self.kwargs)
        elif self.args:
            return str(self.args)
        else:
            return str(self.kwargs)

    def append(self, Element: any):
        """_Append Element To result.args._

        Args:
            Element (any): _Any Type._
        """
        self.args.append(Element)

    def update(self, KnV: dict):
            self.kwargs.update(**KnV)
