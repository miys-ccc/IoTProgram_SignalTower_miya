# デコレーター

# ---- print_more --- #
def print_more(func1):
    def wrapper(*args, **kwargs):
        print("func:", func1.__name__)
        print("*args:", *args)
        print("**kwargs:", **kwargs)
        result = func1(*args, **kwargs)
        print("result:", result)
        return result
    return wrapper


def print_info(func2):
    def wrapper(*args, **kwargs):
        print("start")
        result = func2(*args, **kwargs)
        print("end")
        return result
    return wrapper


@print_info
@print_more
def add_num(a, b):
    return a + b


print("start__")

r = add_num(10, 20)
print(r)
