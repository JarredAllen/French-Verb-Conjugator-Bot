def group_iterable(num, iterable):
    location = 0
    out = ''
    for i in iterable:
        out += i
        location += 1
        if location == num:
            yield out
            location = 0
            out = ''
