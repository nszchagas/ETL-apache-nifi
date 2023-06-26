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
        
        
        inv = {}
                
        inv['idObito'] = jc['CONTADOR']
        
        # Formatando as datas: 
        
        inv['dtInicio']  =   format_date(jc['DTINVESTIG'])
        inv['dtCadastro'] =  format_date(jc['DTCADINV'])
        inv['dtConclusao'] = format_date(jc['DTCONINV'])

        inv['fonteInvestigacao'] = format_enum(fonte_opcoes, jc['FONTEINV'])
        inv['nivelInvestigador'] = format_enum(nivel_inv_opcoes, jc['TPNIVELINV'])
        inv['tipoResgateInformacao'] = format_enum(tipo_resgate_opcoes, jc['TPRESGINFO'])                
        # O conteúdo é serializado para JSON.
        content = json.dumps(inv, cls=DateTimeEncoder)

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
