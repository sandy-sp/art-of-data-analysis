import pandas as pd
import io

def export_dataframe_as_excel(df: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

def export_dataframe_as_csv(df: pd.DataFrame) -> str:
    return df.to_csv(index=False)

def export_dataframe_as_html(df: pd.DataFrame) -> str:
    return df.to_html(index=False)
