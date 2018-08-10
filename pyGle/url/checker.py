#
#                py-google-search  Copyright (C) 2018  Javinator9889                
#   This program comes with ABSOLUTELY NO WARRANTY; for details add the "-h" option.
#           This is free software, and you are welcome to redistribute it
#                 under certain conditions; type "-L" for details.
#
from pyGle.errors import InvalidTimeException


def check_time_limit(input_value: str):
    # type: () -> bool

    if len(input_value) >= 2:
        if input_value[0] == 'm':
            try:
                duration = int(input_value[1:])
                if duration <= 0:
                    __throw_invalid_time_exception(input_value)
            except ValueError:
                __throw_invalid_time_exception(input_value)
        else:
            __throw_invalid_time_exception(input_value)
    elif len(input_value) == 0:
        __throw_invalid_time_exception(input_value)
    else:
        if any(time in input_value for time in ['d', 'w', 'm', 'y']):
            return True
        else:
            __throw_invalid_time_exception(input_value)


def __throw_invalid_time_exception(input_value: str):
    raise InvalidTimeException("Unexpected value: waiting for: \n\t- d\n\t- w\n\t- m\n\t- y\n\t- m[NUMBER],\n got:"
                               " " + input_value)
