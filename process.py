import pandas as pd


def read_in_csv(csv: str):
    #print(pd.__version__)
    df = pd.read_csv(csv)
    #print(df)
    #print(type(df))
    return df

def is_Frame(data):
    return isinstance(data, pd.DataFrame)

def reverse_for_loop(frames):
    if not is_Frame(frames):
            print("Invalid frame")
            return "Invalid frame"

    for i in range(len(frames)-1, -1, -1):
         print(frames.iloc[i])
         
        
def clean_data(df):
    if not is_Frame(df):
        print("❌ Invalid frame")
        return "Invalid frame"
    
    print("🧼 Cleaning data...")

    df.dropna(how='all', inplace=True)

    #Remove white space and make titles normal

    if 'age' in df.columns:
        df['age'] = pd.to_numeric(df['age'], errors='coerce')  # invalid strings -> NaN
        df['age'] = df['age'].fillna(0).astype(int)
        df['age'] = df['age'].where((df['age'] >= 1) & (df['age'] <= 120), 0)


    #df.dropna(subset=['name', 'city', 'age'], inplace=True
    if 'name' in df.columns:
        df['name'] = df['name'].astype(str).str.strip().str.title()

    if 'city' in df.columns:
        df['city'] = df['city'].astype(str).str.strip().str.title()

    df.drop_duplicates(inplace=True)

    print("✅ Cleaned", len(df), "rows")
    print(df)
    return df.to_dict(orient="records")

def read_in_json(json):
    return pd.DataFrame(pd.read_json(json))
     
#reverse_for_loop(read_in_csv())
#reverse_for_loop(read_in_json("uploads/sample.json"))
#clean_data(read_in_csv("uploads/sample.csv"))




