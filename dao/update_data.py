import pandas as pd
import yaml
from datetime import date, timedelta
from num2words import num2words
import logging

logging.basicConfig(level=logging.INFO)

def main(group: int , quota: int , cnab_path: str, contract_path: str) -> None: 
    """_summary_
    Args:
        group (int): _description_
        quota (int): _description_
        cnab_path (str): _description_
        contract_path (str): _description_
                       
    Returns:
        _type_: _description_
    """

    logging.info("Lendo o arquivo csv e convertendo em yaml")
    df_data_contrato = pd.read_csv("data/data_contrato.csv")
    df_data_api = pd.read_csv("./data/data_api.csv")
    
    def parse_data(data_frame: pd.DataFrame) -> str:
        """_summary_
        Args:
            df (pd.DataFrame): _description_
        Returns:
            str: _description_
        """
        string_data = data_frame["data"][0].replace("'", '"')
        string_data = string_data.replace("False", "false")
        string_data = string_data.replace("True", "true")
        string_data = string_data.replace("None", "null")
        return string_data
    
    def fill_number_fild(value: str, field_len: int) -> str:
         """_summary_
         Args:
             value (str): _description_
             field_len (int): _description_
         Returns:
             str: _description_
         """
         if len(value) < field_len:
             value = ((field_len - len(value) ) * '0' +value )
         return  value

    def update_yaml_api(yaml_file: dict, df_data_api: pd.DataFrame) -> dict:
    
        """_summary_
        Args:
            yaml_file (dict): _description_
            data_frame (dict): _description_
        Returns:
            dict: _description_
        """
        #json_data = json.loads(parse_data(df_data))
        json_data = df_data_api
        json_data.fillna("",inplace=True)
        # f"{user_info['document'].values[0]}"
        yaml_file["cedente"]["cpf"] = fill_number_fild(str(json_data["cpf"][0]), 11)
        yaml_file["cedente"]["nome"] = str(json_data["nome"][0])
        yaml_file["cedente"]["cep"] =  fill_number_fild(str(json_data["cep"][0]), 8 )
        yaml_file["cedente"]["logradouro"] = str(json_data["logradouro"][0])
        yaml_file["cedente"]["numeroLogradouro"] = str(json_data["numero_logradouro"][0])
        yaml_file["cedente"]["complementoLogradouro"] = str(json_data["complemento_logradouro"][0])
        yaml_file["cedente"]["bairro"] = str(json_data["bairro"][0])
        yaml_file["cedente"]["cidade"] = str(json_data["cidade"][0])
        yaml_file["cedente"]["uf"] = str(json_data["uf"][0])
        yaml_file["cedente"]["telefone"] = str(json_data["telefone"][0]).replace("55", "")
        yaml_file["cedente"]["signatarios"][0]["cpf"] = fill_number_fild(str(json_data["cpf"][0]), 11)
        yaml_file["cedente"]["signatarios"][0]["nome"] = str(json_data["nome"][0])
        yaml_file["cedente"]["signatarios"][0]["email"] = str(json_data["email"][0])
        yaml_file["cedente"]["signatarios"][0]["fone"] = str(json_data["telefone"][0]).replace("55", "")
        yaml_file["cedente"]["signatarios"][0]["dataNascimento"] = f'''{json_data["data_nascimento"][0][8:10]+"/"+
                                                                                                                  json_data["data_nascimento"][0][5:7]+"/"+
                                                                                                                  json_data["data_nascimento"][0][0:4]}'''
        
        yaml_file["coleta"]["nomeColeta"] = f"Coleta G{group}C{quota}"
        yaml_file["coleta"]["dataVigencia"] = date.today().strftime('%m/%d/%Y') # Hoje
        yaml_file["coleta"]["dataLimite"] =  (date.today() + timedelta(weeks=1)).strftime('%m/%d/%Y') # Hoje + 1 semana
        yaml_file["coleta"]["cedente"]["cpf"] = fill_number_fild(str(json_data["cpf"][0]), 11)
        yaml_file["coleta"]["documentos"][0]["conteudo"] = contract_path
        yaml_file["coleta"]["arquivoCnab"]["conteudo"] = cnab_path
        return yaml_file
        
    def update_yaml_contrato(yaml_file: dict, df_data_contrato: pd.DataFrame) -> dict:
        """_summary_
        Args:
        yaml_file (dict): _description_
        data_frame (dict): _description_
        
        Returns:
            dict: _description_
        """
        preco_aquisicao = float(df_data_contrato["preco_de_aquisicao"][0].replace(",", "."))
        yaml_file["cedente"]["cpf_cedente"] = fill_number_fild(str(df_data_contrato["cpf"][0]), 11)
        yaml_file["cedente"]["nome_cedente"] = str(df_data_contrato["nome"][0])
        yaml_file["cedente"]["cep_cedente"] = fill_number_fild(str(df_data_contrato["cep"][0]), 8 )
        yaml_file["cedente"]["endereco_cedente"] = str(df_data_contrato["endereco"][0])
        yaml_file["cedente"]["comp_cedente"] = str(df_data_contrato["complemento"][0])
        yaml_file["cedente"]["bairro_cedente"] = str(df_data_contrato["barro"][0])
        yaml_file["cedente"]["cidade_cedente"] = str(df_data_contrato["cidade"][0])
        yaml_file["cedente"]["uf_cedente"] = str(df_data_contrato["uf"][0])
        yaml_file["cedente"]["telefone_cedente"] = str(df_data_contrato["telefone"][0]).replace("55", "")
        yaml_file["cedente"]["email_cedente"] = str(df_data_contrato["email"][0])
        yaml_file["cedente"]["grupo"] = str(df_data_contrato["grupo"][0])
        yaml_file["cedente"]["cota"] = str(df_data_contrato["cota"][0])
        yaml_file["cedente"]["carta_credito"] = str(df_data_contrato["carta_credito_objeto_plano_vigente"][0])
        yaml_file["cedente"]["data_aquisicao"] = str(df_data_contrato["data_da_aquisicao"][0])
        yaml_file["cedente"]["data_exclusao"] = str(df_data_contrato["data_da_exclusao"][0])
        yaml_file["cedente"]["percentual_pago"] = str(df_data_contrato["percentual_pago_pelo_cliente"][0])
        yaml_file["cedente"]["contrato_adesao"] = str(df_data_contrato["contrato_adesao"][0])
        yaml_file["cedente"]["bem_objeto"] = str(df_data_contrato["bem_objeto"][0])
        yaml_file["cedente"]["credito_atual"] = str(df_data_contrato["credito_atual"][0])
        yaml_file["cedente"]["saldo_devedor"] = str(df_data_contrato["saldo_devedor"][0])
        yaml_file["cedente"]["preco_aquisicao"] = str(df_data_contrato["preco_de_aquisicao"][0])
        yaml_file["cedente"]["preco_aquisicao_extenso"] = num2words(preco_aquisicao, lang='pt-br')
        yaml_file["cedente"]["banco"] = str(df_data_contrato["banco"][0])
        yaml_file["cedente"]["agencia"] = str(df_data_contrato["agencia"][0])
        yaml_file["cedente"]["conta_corrente"] = str(df_data_contrato["conta_corrente"][0])
        yaml_file["cedente"]["mes"] = date.today().strftime('%m')
        yaml_file["cedente"]["ano"] = date.today().strftime('%y')
        yaml_file["cedente"]["dia"] = date.today().strftime('%d')
        return yaml_file

    with open(
        "/workspaces/msc-pdf-generator/data/config_contrato.yaml", "r", encoding="utf8"
    ) as rfile:
        configf_contrato = yaml.safe_load(rfile)
        configf_contrato = update_yaml_contrato(configf_contrato, df_data_contrato)

    with open(
        "/workspaces/msc-pdf-generator/data/config_contrato.yaml", "w", encoding="utf8"
    ) as wfile:
        yaml.safe_dump(configf_contrato, wfile)
        
    with open(
        "/workspaces/msc-pdf-generator/data/config_api.yaml", "r", encoding="utf8"
    ) as rfile:
        configf_api = yaml.safe_load(rfile)
        configf_api = update_yaml_api(configf_api, df_data_api)

    with open(
        "/workspaces/msc-pdf-generator/data/config_api.yaml", "w", encoding="utf8"
    ) as wfile:
        yaml.safe_dump(configf_api, wfile)

    # for _key in json_data:
    #     print(_key, json_data[_key])

# if __name__ == "__main__":
#     main()