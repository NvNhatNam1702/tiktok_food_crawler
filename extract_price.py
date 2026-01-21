from operator import index
import os
import re
import pandas as pd

def normalize_the_price(value, unit) :
    value  = value.replace(" ", "")
    if "," in value and "." not in value:
        value.replace(",", ".")
    try: 
        number = float(value)
    except ValueError:
        return None
    if unit in ["cành","k","ngàn","nghìn","đ","vnd"]:
        number *= 1000.0

    return int(number)

def extract_price_text(input_dir, output_csv):
    # NOTE : regular expression
    price_pattern = re.compile(
        r"(\d{1,3}(?:[.,]\d{3})*|\d+)\s*(cành|k|ngàn|nghìn|đ|vnd)?", re.IGNORECASE
    )
    all_prices = []
    len_data = len(os.listdir(input_dir))
    if len_data == 0:
        print(f"no data in {input_dir}")
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_dir, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().lower()
            except Exception as e:
                print(f"there an erorr in reading txt : {e}")
                continue
        price = price_pattern.findall(content)
        #output : value + unit (e.g: 12k or 12 ngàn)
        for value, unit in price:
            price = normalize_the_price(value, unit)
            all_prices.append({"filename": filename, "value": f"{value} {unit}", "normalize_value" : price})

    if all_prices:
        df = pd.DataFrame(all_prices)
        df.to_csv(output_csv, index = False)
        print(f"success!!")
    else:
        print(f"no data")


extract_price_text("cleaned_text", "price.csv")
