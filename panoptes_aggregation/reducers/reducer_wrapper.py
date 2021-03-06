from functools import wraps
from .process_kwargs import process_kwargs


def reducer_wrapper(process_data=None, defaults_process=None, defaults_data=None):
    def decorator(func):
        @wraps(func)
        def wrapper(argument, **kwargs):
            kwargs_process = {}
            kwargs_data = {}
            #: check if argument is a flask request
            if hasattr(argument, 'get_json'):
                kwargs = argument.args
                data_in = [d['data'] for d in argument.get_json()]
            else:
                data_in = argument
            if defaults_process is not None:
                kwargs_process = process_kwargs(kwargs, defaults_process)
            if defaults_data is not None:
                kwargs_data = process_kwargs(kwargs, defaults_data)
            if process_data is not None:
                data = process_data(data_in, **kwargs_process)
            else:
                data = data_in
            return func(data, **kwargs_data)
        #: keep the orignal function around for testing
        #: and access by other reducers
        wrapper._original = func
        return wrapper
    return decorator
