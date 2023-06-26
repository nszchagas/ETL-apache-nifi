from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import StreamCallback
import json

# Define a subclass of StreamCallback for use in session.write()
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
    except Exception as e:
        opcao = cod
    return opcao


class PyStreamCallback(StreamCallback):
    def __init__(self):
        pass

    def process(self, inputStream, outputStream):
        text = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
        
        jc = json.JSONDecoder().decode(text)
        
        
        etnia = {
            '1': 'BRANCA',
            '2': 'PRETA',
            '3': 'AMARELA',
            '4': 'PARDA',
            '5': 'INDIGENA'
        }
        
        estciv = {
            '1': 'SOLTEIRO', 
            '2': 'CASADO',
            '3': 'VIUVO',
            '4': 'SEPARADO',
            '5': 'UNIAO_CONSENSUAL',
            '9': 'IGNORADO'            
        }
        
        escolaridade = {
            '1':'NENHUMA',
            '2':'DE_1_A_3_ANOS',
            '3':'DE_4_A_7_ANOS',
            '4':'DE_8_A_11_ANOS',
            '5':'12_ANOS_E_MAIS',
            '9':'IGNORADO'
        }
        
        dados = {}
        date_keys = ['DTOBITO', 'DTNASC', 'DTATESTADO', 'DTINVESTIG', 'DTCADASTRO',
             'DTRECEBIM', 'DTRECORIGA', 'DTCADINV', 'DTCONINV', 'DTCADINF', 'DTCONCASO', ]

        for dk in date_keys:
            jc[dk] = format_date(jc[dk])

        dados['idObito'] = jc['CONTADOR']
        dados['naturalidade'] = jc['NATURAL']
        dados['codMunResidencia'] = jc['CODMUNRES']
        dados['codMunNaturalidade'] = jc['CODMUNNATU']
        dados['dtNascimento'] = jc['DTNASC']
        dados['dtFalecimento'] = jc['DTATESTADO']
        dados['sexo'] = jc['SEXO']
        dados['etnia'] = format_enum(etnia, jc['RACACOR'])
        dados['estadoCivil'] = format_enum(estciv, jc['ESTCIV'])
        dados['escolaridade'] = format_enum(escolaridade, jc['ESC'])
        dados['codOcupacao'] = jc['OCUP']
        dados['qtdFilhosVivos'] = jc['QTDFILVIVO']
        dados['qtdFilhosMortos'] = jc['QTDFILMORT']
        dados['tipoGravidez'] = jc['GRAVIDEZ']
        dados['semanasGestacao'] = jc['SEMAGESTAC']
        dados['tipoParto'] = jc['PARTO']
        dados['pesoEmGramas'] = jc['PESO']
        dados['numeroLote'] = jc['NUMEROLOTE']
        
        
        content = json.dumps(dados)
        outputStream.write(bytearray(content.encode('utf-8')))


# end class
flowFile = session.get()
if (flowFile != None):
    flowFile = session.write(flowFile, PyStreamCallback())

session.transfer(flowFile, REL_SUCCESS)
