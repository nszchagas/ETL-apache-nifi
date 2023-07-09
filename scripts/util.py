def format_enum(opcoes, cod):
    if cod == "" or cod == "null" or cod == None:
        return None
    try:
        opcao = opcoes[int(cod)]
    except Exception:
        try:
            opcao = opcoes[cod]
        except Exception:
            opcao = cod

    return opcao


def format_date(date):
    date = str(date)
    if date == "" or date == None or date == "null" or date == "None":
        return None

    d = int(date[0:2])
    m = int(date[2:4])
    y = int(date[4:])
    data = datetime(y, m, d)

    return data.strftime("%Y-%m-%d %H:%M:%S.000")
