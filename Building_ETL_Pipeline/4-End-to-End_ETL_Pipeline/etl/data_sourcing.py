import pandas as pd



def extract_data(file_path: str) -> object:

    try:
        df = pd.read_csv(file_path)
        print("Data loaded successfully in DataFrame")
    except FileNotFoundError as e:
        print(f"File Not Found : {e}")
    except Exception as e:
        print(f"error : {e}")


    return df