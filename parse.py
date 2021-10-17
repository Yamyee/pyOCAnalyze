import os


def filterContent(content, l, r):
    if (l not in content) or (r not in content):
        return content
    arr = content.split(l)
    if len(arr) > 1:
        c = arr[1]
        arr = c.split(r)
        if len(arr) > 1:
            c = arr[0]
        return c.strip(" ")
    else:
        return content


def filterArr(content, l, r, sep):
    s = filterContent(content, l, r)
    res = []
    if sep in s:
        for c in s.split(sep):
            res.append(c.strip(" "))
    else:
        res.append(s)
    return res