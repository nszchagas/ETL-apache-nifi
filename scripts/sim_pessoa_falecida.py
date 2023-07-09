from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import StreamCallback
import json


# Função para converter o código armazenado no sistema para
# um ENUM correspondente.


def format_enum(opcoes, cod):
    if cod == "" or cod == "null" or cod == None:
        return 'IGNORADO'
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


def format_escolaridade(dados):
    escolaridade = 'IGNORADO'

    # A escolaridade pode estar em um dos três campos: ESC, ESC2010 e ESCFALAGR1.
    esc = {1: 'NENHUMA', 2: 'FUND_I_INC', 3: 'FUND_II_INC',
           4: 'MEDIO_INC', 5: 'MEDIO_COMP', 9: 'IGNORADO'}
    esc2010 = {0: 'NENHUMA', 1: 'FUND_I_COMP', 2: 'FUND_II_COMP',
               3: 'MEDIO_COMP', 4: 'SUPERIOR_INC', 5: 'SUPERIOR_COMP', 9: 'IGNORADO'}
    escfalagr1 = {0: 'NENHUMA', 1: 'FUND_I_INC', 2: 'FUND_I_COMP', 3: 'FUND_II_INC', 4: 'FUND_II_COMP', 5: 'MEDIO_INC',
                  6: 'MEDIO_COMP', 7: 'SUPERIOR_INC', 8: 'SUPERIOR_COMP', 9: 'IGNORADO', 10: 'IGNORADO', 11: 'IGNORADO', 12: 'IGNORADO'}
    if dados['ESC']:
        return format_enum(esc, dados['ESC'])
    if dados['ESC2010']:
        return format_enum(esc2010, dados['ESC2010'])
    if dados['ESCFALAGR1']:
        return format_enum(escfalagr1, dados['ESCFALAGR1'])

    return escolaridade


class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


class PyStreamCallback(StreamCallback):
    def __init__(self):
        pass

    def process(self, inputStream, outputStream):
        text = IOUtils.toString(inputStream, StandardCharsets.UTF_8)

        jc = json.JSONDecoder().decode(text)

        d = {}
        date_keys = ['DTNASC', 'DTATESTADO']

        for dk in date_keys:
            jc[dk] = format_date(jc[dk])

            # ENUMS
        sexo = {'M': 'M', 'F': 'F', 'I': 'IGNORADO'}

        etnia = {1: 'BRANCA', 2: 'PRETA',
                 3: 'AMARELA', 4: 'PARDA', 5: 'INDIGENA'}

        estado_civil = {1: 'SOLTEIRO', 2: 'CASADO', 3: 'VIUVO',
                        4: 'SEPARADO', 5: 'UNIAO_CONSENSUAL', 9: 'IGNORADO'}

        d['idObito'] = jc['contador']
        d['naturalidade'] = jc['NATURAL']
        d['codMunResidencia'] = jc['CODMUNRES']
        d['codMunNaturalidade'] = jc['CODMUNNATU']
        d['dtNascimento'] = jc['DTNASC']
        d['dtFalecimento'] = jc['DTATESTADO']
        d['sexo'] = jc['SEXO']
        d['etnia'] = format_enum(etnia, jc['RACACOR'])
        d['estadoCivil'] = format_enum(estciv, jc['ESTCIV'])
        d['escolaridade'] = format_escolaridade(jc)

        content = json.dumps(d)
        outputStream.write(bytearray(content.encode('utf-8')))


# end class
flowFile = session.get()
if (flowFile != None):
    flowFile = session.write(flowFile, PyStreamCallback())

session.transfer(flowFile, REL_SUCCESS)
