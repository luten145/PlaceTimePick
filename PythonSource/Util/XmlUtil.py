def getDataList(data, s, e):
    if s in data:
        tmp = data.split(s)
        data = []
        for i in range(0, len(tmp)):
            if e in tmp[i]:
                data.append(tmp[i][:tmp[i].find(e)])
    else:
        data = []
    return data


def getDataItem(data, s, e):
    if s in data:
        data = data[data.find(s) + len(s):]
        if e in data: data = data[:data.find(e)]
    return data