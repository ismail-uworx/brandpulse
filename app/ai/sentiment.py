from transformers import pipeline, AutoTokenizer
from datasets import Dataset
import pandas as pd
import numpy as np

MODEL_NAME = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"

label2Id = {"negative": 0, "neutral": 1, "positive": 2}


def tokenize():

    df = pd.read_excel("data\BrandPulse_Sentiment_Training_Dataset.xlsx")

    df["label"] = df["label"].map(label2Id)
    dataset = Dataset.from_dict(df)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    def preprocessFunction(examples):
        return tokenizer(examples["text"], truncation=True, max_length=28)

    tokenizedDataset = dataset.map(preprocessFunction, batched=True)

    return tokenizedDataset


def fineTune():
    print("Write fine tuning logic")


pipeline = pipeline(
    task="text-classification",
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student",
    use_safetensors=True,
)

if __name__ == "__main__":

    print("running")

    testInputs = [
        "I keep getting a 500 Internal Server Error every time I click billing.",
        "The application UI is standard, nothing special.",
        "Wow, the loading speed is incredibly fast! Love it.",
    ]

    for input in testInputs:
        print(pipeline(input))

    tokenize()
