from transformers import pipeline

# model being used is lxyuan/distilbert-base-multilingual-cased-sentiments-student

LOCAL_MODEL_PATH = "app/ai/fine_tuned_sentiment"

sentimentPipeline = pipeline(
    task="text-classification", model=LOCAL_MODEL_PATH, tokenizer=LOCAL_MODEL_PATH
)


def analyzeSentiment(text: str) -> dict:

    output = sentimentPipeline(text)[0]

    return {"label": output["label"], "confidence": round((output["score"] * 100), 2)}


if __name__ == "__main__":

    testInputs = [
        "I keep getting a 500 Internal Server Error every time I click billing.",
        "The application UI is standard, nothing special.",
        "Wow, the loading speed is incredibly fast! Love it.",
    ]

    for input in testInputs:
        pred = analyzeSentiment(input)[0]
        print(f"text: {input}")
        print(f"Label: {pred['label'].upper()} Confidence: {pred['confidence']}%")
        print("-" * 50)
