#
#                py-google-search  Copyright (C) 2018  Javinator9889                
#   This program comes with ABSOLUTELY NO WARRANTY; for details add the "-h" option.
#           This is free software, and you are welcome to redistribute it
#                 under certain conditions; type "-L" for details.
#


class InvalidTimeException(RuntimeError):
    def __init__(self, message: str = None):
        self.__message = message
        super().__init__(message)


class InvalidCombinationException(RuntimeError):
    def __init__(self, message: str = None):
        self.__message = message
        super().__init__(message)


class NullQueryError(RuntimeError):
    def __init__(self, message: str = None):
        self.__message = message
        super().__init__(message)


class GoogleOverloadedException(RuntimeError):
    def __init__(self, message: str = None):
        self.__message = message
        super().__init__(message)
