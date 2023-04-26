import os
import shutil
import pdfrw
import yaml
import logging
from time import sleep

from api import (
caller_cadastro_cedentes,
caller_cadastro_coleta_hibrida,
caller_consulta_docs,
caller_consulta_props,
caller_consulta_status_coleta,
)

from dao import query_data, update_data, update_s3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(group: int, quota: int, cnab_path: str, contract_path: str): 
    """_summary_
    Args:
        _type_: _description_
    """
    
    logger.info('gerando pdf')
    
    # Remove os arquivos da pasta data
    # with os.scandir("./data") as entries:
    #     for entry in entries:
    #         if entry.is_dir() and not entry.is_symlink():
    #             shutil.rmtree(entry.path)
    #         else:
    #             os.remove(entry.path)
    
# Preenche o config.yaml
    query_data.query(460, 333)
    sleep(1)
    update_data.main(group, quota, cnab_path, contract_path)
    sleep(2)

    with open(
        "./data/config_contrato.yaml", "r", encoding="latin1"
    ) as file:
        configf_contrato = yaml.safe_load(file)

    with open("./data/config_api.yaml", "r", encoding="latin1") as file:
        configf_api = yaml.safe_load(file)

    with open("./templates/json/consultaDocsProp.json", "r", encoding="latin1") as file:
        consultaDocsProp = yaml.safe_load(file)

    with open("./templates/json/cadastroCedentes.json", "r", encoding="latin1") as file:
        cadastroCedentes = yaml.safe_load(file)

    with open(
        "./templates/json/cadastroColetaDigital.json", "r", encoding="latin1"
    ) as file:
        cadastroColetaDigital = yaml.safe_load(file)

    with open(
        "./templates/json/cadastroColetaHibrida.json", "r", encoding="latin1"
    ) as file:
        cadastroColetaHibrida = yaml.safe_load(file)

    with open(
        "./templates/json/consultaStatusColeta.json", "r", encoding="latin1"
    ) as file:
        consultaStatusColeta = yaml.safe_load(file)
    return (
        configf_contrato,
        configf_api,
        consultaDocsProp,
        cadastroCedentes,
        cadastroColetaDigital,
        cadastroColetaHibrida,
        consultaStatusColeta
    )
    
def form_filler(in_path: str, data: dict, out_path: str) -> None:
    """_summary_
    Args:
        in_path (str): _description_
        data (object): _description_
        out_path (str): _description_
    """
    logger.info('preenchendo formulário')
       
    pdf = pdfrw.PdfReader(in_path)
    for page in pdf.pages:
        annotations = page["/Annots"]
        if annotations is None:
            continue
        for annotation in annotations:
            if annotation["/Subtype"] == "/Widget":
                key = str(annotation["/T"].to_unicode())
                if key in data:
                    pdfstr = pdfrw.objects.pdfstring.PdfString.encode(data[key])
                    annotation.update(pdfrw.PdfDict(V=pdfstr, Ff=1))
                    annotation.update(pdfrw.PdfDict(Ff=1))
        pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject("true")))
        pdfrw.PdfWriter().write(out_path, pdf)
    
if __name__ == "__main__":
    BATCH_SIZE = 2
    GRUPO = 460
    COTA = 333
    GROUP = [GRUPO, GRUPO]
    QUOTA = [COTA, COTA]
    CONTRACT_PATH = [
        "./templates/pdf/filled_out_contrato_cessao_forms_api.pdf",
        "./templates/pdf/filled_out_contrato_cessao_forms_api.pdf",
    ]
    CNAB_PATH = ["./files/CNAB444.rem", "./files/CNAB444.rem"]
    query_data.query(GRUPO, COTA)
    update_data.main(GROUP[0], QUOTA[0], CNAB_PATH[0], CONTRACT_PATH[0])
   
    for index in range(BATCH_SIZE):
        (
            configf_contrato,
            configf_api,
            consultaDocsProp,
            cadastroCedentes,
            cadastroColetaDigital,
            cadastroColetaHibrida,
            consultaStatusColeta,
        ) = main(GROUP[0], QUOTA[0], CNAB_PATH[0], CONTRACT_PATH[0])
        
    form_filler(
         "templates/pdf/template_contrato_cessao_forms.pdf",
         configf_contrato["cedente"],
         "templates/pdf/filled_out_contrato_cessao_forms_contrato.pdf",
    )
    
    # # 3. Consultar os Tipos de Documentos
    #caller_consulta_docs.post(configf_api, consultaDocsProp)

    # # 4. Consultar os Propósitos de Assinatura
    # caller_consulta_props.post(configf_api, consultaDocsProp)

    # 5. Cadastro de Cedentes
    #caller_cadastro_cedentes.post(configf_api, cadastroCedentes)

    # 6. Cadastro da Coleta Digital de Recebíveis
    # caller_cadastro_coleta_hibrida.post(configf_api, cadastroColetaHibrida)
   
    # 7. Consulta o Status da Coleta
    # caller_consulta_status_coleta.post(configf_api, consultaStatusColeta)
    
    # 8. Dowload arquivo Cnab
    update_s3.download()