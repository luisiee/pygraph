class _Error:
    def __init__(self, msg):
        self._msg = msg
    
    def __str__(self):
        return self._msg


class OptionsError(_Error):
    def __init__(
        self, 
        cls: str, 
        arg: str, 
        options: set | dict = None, 
        add_msg: str = ''
    ):
        msg = f'Tried to set {cls} `{arg}`, but `{arg}` is an invalid option. '
        if options is not None:
            msg = (
                msg 
                + f' `{arg}` must take one of the following values: {options} '
            )
        
        super().__init__(msg + add_msg)


class IndexError(_Error):
    def __init__(
        self, 
        cls: str, 
        arg: str, 
        idx: str = 'name', 
        action: str = None,
        overwrite: bool = False,
        add_msg: str = ''
    ):
        if action is None:
            action = f'add `{arg}` to {cls}'

        msg = f'Tried to {action}, but `{idx}` '
        if overwrite:
            msg = (
                msg
                + 'is already displayed or taken. '
                + f'If you wish to overwrite the current `{arg}`, set '
                + '`overwrite` to True. '
            )
        else:
            msg = msg + 'wasn\'t found. ' 

        super().__init__(msg + add_msg)