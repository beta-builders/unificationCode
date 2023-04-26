""" query database
"""

import os
import time
import pandas as pd
import psycopg2
import logging

from .config import DBNAME, DBPASS, DBUSER, DBPORT, AWSENV
from .queries import QUERY1, QUERY2, QUERY3

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('Rodando a query e gerando o arquivo csv')


def query(group_nun: int, quota_nun: int) -> None:
    """Realiza a query baseado em grupo e cota
    Args:
        GROUP (int): Grupo
        QUOTA (int): Cota
    """
    os.system(
        "nohup bash /app/dao/scripts/bastion-port-forward.sh env=prod lp=5435 >/dev/null 2>&1 &"
    )
    time.sleep(10)
    conn = psycopg2.connect(
        database=DBNAME, user=DBUSER, password=DBPASS, host="localhost", port=DBPORT
    )

    cur = conn.cursor()

    queries = [QUERY1.format(group_nun, quota_nun), QUERY2.format(group_nun, quota_nun), QUERY3.format(AWSENV, group_nun, quota_nun)]
    queries_names = ["data_api", "data_contrato", "data_cnab"]

    for index, query_str in enumerate(queries):
        cur.execute(query_str)
        rows = cur.fetchall()

        row_list = [row for row in rows]
        
        column_names = [desc[0] for desc in cur.description]

        df = pd.DataFrame(row_list, columns=column_names)
        # df.drop(["ownername"], axis=1, inplace=True)
        # df["ownername"] = df["ownername"].apply(
        #     lambda x: str(x)[:3] + "***********" + str(x)[-3:] if x == x else x
        # )

        df.to_csv(
            f"/app/data/{queries_names[index]}.csv",
            index=False,
            header=True,
        )
        df.to_csv(f"./data/{queries_names[index]}.csv", index=False, header=True)
        df.to_csv(f"./data/{queries_names[index]}.csv", index=False, header=True)

    cur.close()
    conn.close()

# if __name__ == "__main__":
#    query(460, 333)