from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import StreamCallback
import json
import datetime
from datetime import datetime
from json import JSONEncoder

# Essa classe herda a classe StreamCallback, do apache/nifi.

# Função para converter o código armazenado no sistema para
# um ENUM correspondente.



def format_timestamp(data, time="0000"):
    
    if not (time == "" or time == None or time == "null" or time == "None"):
        h = int(time[0:2])
        m = int(time[2:])
    else:
        h = '00'
        m = '00'
    # data = data + datetime.timedelta(hours=hours, minutes=minutes)
    return '{0} {1}:{2}:00'.format(data, str(h).zfill(2), str(m).zfill(2))




def format_date(date):
    date = str(date)
    if date == "" or date == None or date == "null" or date == "None":
        return None
    
    d = date[0:2]
    m = date[2:4]
    y = date[4:]
    
    return '{0}-{1}-{2}'.format(y, m, d)


def format_enum(opcoes, cod):
    if cod == "":
        return 'IGNORADO'
    try:
        opcao = opcoes[int(cod)]
    except Exception:
        try: 
            opcao = opcoes[cod]
        except Exception:
            opcao = cod
            
    return opcao

def format_linha(linha): 
    if linha:
        return linha.replace('*', '')
    return None

class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


class PyStreamCallback(StreamCallback):
    def __init__(self):
        pass

    def process(self, inputStream, outputStream):
        # Opções para os enums
        fonte_opcoes = { '1':'ComiteDeMorteMaternaOuInfantil' , '2':'VisitaDomiciliar' , '3':'Prontuario' , '4':'RelacionadoComOutrosBancosDeDados' , '5':'SVO' , '6':'IML' , '7':'OutraFonte' , '8':'MultiplasFontes' , '9':'Ignorado' }
        
        opcoes_parto = {1: 'ANTES',
                2: 'DURANTE',
                3: 'DEPOIS',
                9: 'IGNORADO'}
        nivel_inv_opcoes = {'E': 'ESTADUAL','R': 'REGIONAL', 'M': 'MUNICIPAL'}
        tipo_resgate_opcoes = {1: 'NAO_ACRESCENTOU', 2: 'SIM_NOVAS_INFORMACOES', 3: 'SIM_CORRECAO_CAUSAS'}
        # O conteúdo do arquivo (FlowFile) é lido do inputStream e
        # decodificado em utf-8.
        text = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
        # O conteúdo textual é decodificado como json, por meio do
        # pacote json do python.
        jc = json.JSONDecoder().decode(text)
        # Um objeto metadados é inicializado, e nele serão inseridas apenas
        # as propriedades necessárias.
        
        
        data = {}
                
        data['idObito'] = jc['CONTADOR']
        data['isObitoFetal'] = (jc['TIPOBITO'] == 1)
        data['houveAlteracaoCausa'] = (jc['ALTCAUSA'] == 1)
        data['dataHora'] = format_timestamp(
                    jc['DTOBITO'], jc['HORAOBITO'])
        data['diagonosticoLinhaA'] = format_linha(jc['LINHAA'])
        data['diagonosticoLinhaB'] = format_linha(jc['LINHAB'])
        data['diagonosticoLinhaC'] = format_linha(jc['LINHAC'])
        data['diagonosticoLinhaD'] = format_linha(jc['LINHAD'])
        data['diagonosticoLinhaII'] =format_linha( jc['LINHAII'])
        data['causaBasica'] = jc['CAUSABAS']
        data['cids'] = jc['ATESTADO'].replace('/', ', ')
        data['obitoEmRelacaoAoParto'] = format_enum(
                    opcoes_parto, jc['OBITOPARTO'])
        data['crmAtestante'] = jc['ATESTANTE']
        
        # Formatando as datas: 
        
        # O conteúdo é serializado para JSON.
        content = json.dumps(data, cls=DateTimeEncoder)

        # E por fim, o conteúdo é escrito novamente no arquivo,
        # fazendo a sobrescrita.
        outputStream.write(bytearray(content.encode('utf-8')))


flowFile = session.get()
if (flowFile != None):
    # Se houver flowFile, faz a escrita nela, utilizando a classe criada
    # anteriormente como CallBack dessa função.
    flowFile = session.write(flowFile, PyStreamCallback())

# O arquivo é transferido para a próxima etapa, com o status de sucesso.
session.transfer(flowFile, REL_SUCCESS)
