from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("cartesinus/bert-base-uncased-amazon-massive-intent")
model = AutoModelForSequenceClassification.from_pretrained("cartesinus/bert-base-uncased-amazon-massive-intent")

# inputs = tokenizer("Play All I want for Christmas is you", return_tensors="pt")
inputs = tokenizer("Set an alarm for 8AM", return_tensors="pt")


with torch.no_grad():
    logits = model(**inputs).logits

predicted_class_id = logits.argmax().item()
ahh = model.config.id2label[predicted_class_id]
print(ahh)
