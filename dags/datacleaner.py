import pandas as pd
import re

def data_cleaner():
    input_path = "/store_files/raw_store_transactions.csv"
    output_path = "/store_files/clean_store_transactions.csv"

    df = pd.read_csv(input_path)

    # Remove anything other than whitespace and word character 
    # Strip both dead ends  

    def clean_store_location(st_loc):
        return re.sub(r"[^\w\s]", "", str(st_loc)).strip()

    # Stop and return pd_id value when anything other than number arises(Formatting IDs)
    def clean_product_id(pd_id):
        matches = re.findall(r"\d+", str(pd_id))
        return matches[0] if matches else pd_id

    # Remove dolar symbol 
    def remove_dollar(amount):
        return float(str(amount).replace("$", ""))

    df["STORE_LOCATION"] = df["STORE_LOCATION"].map(clean_store_location)
    df["PRODUCT_ID"] = df["PRODUCT_ID"].map(clean_product_id)

    for col in ["MRP", "CP", "DISCOUNT", "SP"]:
        df[col] = df[col].map(remove_dollar)

    df.to_csv(output_path, index=False)
