# main.py
import os
import json
import pandas as pd
from datetime import date, datetime
from dotenv import load_dotenv
from sqlalchemy import text

from db import engine_risco
from AzureBlobConnect import AzureBlobConnect
from sql import SQL_RESGATES

# ========= calendário bizdays / ANBIMA =========
def load_anbima_calendar():
    from bizdays import Calendar
    try:
        return Calendar.load("ANBIMA")
    except Exception as e:
        raise RuntimeError(
            "Não foi possível carregar o calendário 'ANBIMA' no bizdays. "
            "Certifique-se de que ele está registrado no seu ambiente."
        ) from e

def bizday_offset(cal, d: date, n: int) -> date:
    return cal.offset(d, n)

# ========= utils =========
def executar_query_com_data(data_ref: date, sql: str) -> pd.DataFrame:
    query = sql.replace("{{data_ref}}", str(data_ref))
    with engine_risco.connect() as conn:
        return pd.read_sql_query(text(query), con=conn)

def stringify_datetimes(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].astype(str)
        else:
            sample = df[col].head(50)
            if sample.apply(lambda x: isinstance(x, (datetime, date))).any():
                df[col] = df[col].astype(str)
    return df

def save_arquivo(blob_name: str, content_bytes: bytes, container_name: str = "rawdata") -> None:
    connect_str = os.getenv("AUGME_WASB_CONNECTION_STRING")
    wasb_client = AzureBlobConnect.connect(connection_string=connect_str, container_name=container_name)
    wasb_client.save_blob(blob_name=blob_name, content=content_bytes)

# ========= main =========
if __name__ == "__main__":
    load_dotenv()
    cal = load_anbima_calendar()

    # Usa DATA_REF do ambiente ou D-1 como padrão
    env_data = os.getenv("DATA_REF")
    if env_data:
        data_base = date.fromisoformat(env_data)
    else:
        data_base = bizday_offset(cal, date.today(), -2)

    # ------- Resgates -------
    df_resgates = executar_query_com_data(data_base, SQL_RESGATES)
    df_resgates["data_ref"] = str(data_base)
    df_resgates = stringify_datetimes(df_resgates)

    # Salva JSON no Blob
    json_resgates = json.dumps(df_resgates.to_dict(orient="records"), ensure_ascii=False, indent=2)
    base_path_resgates = "risco/resgates_proj"
    fname_resgates = f"resgates_{data_base}.json"
    blob_path_resgates = f"{base_path_resgates}/{fname_resgates}"
    save_arquivo(blob_path_resgates, json_resgates.encode("utf-8"))

    resumo = {
        "resgates": {
            "blob_path": blob_path_resgates,
            "total_rows": int(df_resgates.shape[0])
        }
    }
    print(json.dumps(resumo, separators=(",", ":")))
