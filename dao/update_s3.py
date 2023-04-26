import boto3
import botocore
import pandas as pd
import logging

from .config import AWSENV

logging.basicConfig(level=logging.INFO)

def download():
    
    logging.info("Lendo o Bucket no S3 e gerando o Cnab")
    
    # Ler o arquivo CSV e armazenar os dados em um dataframe do pandas
    df = pd.read_csv("data/data_cnab.csv")

    #Variaveis de acessos AWS
    Bucket = f'{AWSENV}-msc-cnab-files'
    File_name = df["name"][0]
    print(File_name)

 # Criação de uma conexão com o S3
    #session = boto3.Session(Bucket)
    session = boto3.Session(profile_name=f'msc-{AWSENV}')
    s3 = session.resource('s3')

    # Download do arquivo cnab com tratamento de exceção para erro
    try:
        s3.Bucket(Bucket).download_file(File_name, 'template/arq_cnab.csv')
        print("Arquivo baixado com sucesso!")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("O arquivo não existe.")
        else:
            raise
        
if __name__ == "__main__":
     download()
        