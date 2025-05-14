class result():
    def __init__(self,
                 state: bool,
                 *args: any,
                 **kwargs: any):
        self.state: bool = state
        self.args: tuple = args
        self.kwargs: dict = kwargs

    def __bool__(self):
        return self.state
    
    def __getitem__(self, Index):
        return self.args[Index]

    def __call__(self, Key):
        return self.kwargs[Key]

    def __repr__(self):
        if all((self.args, self.kwargs)) or not any((self.args, self.kwargs)):
            return str(self.args)+str(self.kwargs)
        elif self.args:
            return str(self.args)
        else:
            return str(self.kwargs)
