from operator import mod
from sys import exception
from google.ai.generativelanguage_v1beta.types import content
from google.generativeai.types import GenerationConfig, content_types
from urllib3 import response
from utils.prompt import PROMPT
from utils.scheme import FoodList
import google.generativeai as genai
import os
import json
import pandas as pd
from dotenv import load_dotenv
import time

load_dotenv()
# TODO : testing a file
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


def extract_info(text):
    model = genai.GenerativeModel(model_name="gemini-2.5-flash-lite")

    prompt = f"{PROMPT}+{text}"
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json", response_schema=FoodList
            ),
        )
        print(f"{response.text}")
        # return json.loads(response.text).get("items", [])
        return json.loads(response.text)
    except Exception as e:
        print(f"error occured in processing text: {e}")
        return []


def parse_to_csv(input_dir, output_csv):
    all_data = []
    len_data = len(os.listdir(input_dir))
    if len_data == 0:
        print(f"no data in {input_dir}")
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_dir, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                print(f"there an erorr in reading txt : {e}")
                content = []
            if content:
                item = extract_info(content)
                time.sleep(5)
                all_data.append(item)
    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv(output_csv)
        print(f"success!!")
    else:
        print(f"no data")


parse_to_csv("/home/nampc/code/personal/tiktok/test_data/", "data.csv")
