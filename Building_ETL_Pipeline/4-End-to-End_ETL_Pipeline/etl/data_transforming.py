import pandas as pd


def transform_data(df: object) -> object:
  # 1. Drop duplicate rows
  df = df.drop_duplicates()

  # 2. Fill numeric columns with their mean (prevents TypeError on text columns)
  numeric_cols = df.select_dtypes(include="number").columns
  if not numeric_cols.empty:
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

  # 3. Fill remaining missing values column-by-column with their mode
  for col in df.columns:
    if df[col].isnull().any():
      mode_val = df[col].mode()
      if not mode_val.empty:
        df[col] = df[col].fillna(mode_val.iloc[0])

  # 4. Safely convert CRASH_DATE to datetime
  if "CRASH_DATE" in df.columns:
    try:
      df["CRASH_DATE"] = pd.to_datetime(
          df["CRASH_DATE"], format="%m/%d/%Y", errors="coerce"
      )
    except Exception:
      pass

  # 5. Safely convert POSTED_SPEED_LIMIT to integer
  if "POSTED_SPEED_LIMIT" in df.columns:
    try:
      df["POSTED_SPEED_LIMIT"] = df["POSTED_SPEED_LIMIT"].astype("int32")
    except Exception:
      pass

  return df