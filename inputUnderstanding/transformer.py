from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import redis

class Transformer:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("cartesinus/bert-base-uncased-amazon-massive-intent")
        self.model = AutoModelForSequenceClassification.from_pretrained("cartesinus/bert-base-uncased-amazon-massive-intent")
        r = redis.Redis(
            host='127.0.0.1',
            port=6379,
            decode_responses=True
        )
        listener = r.pubsub()
        listener.subscribe('voice-input')
        for message in listener.listen():
            self.determine_intent(str(message))

    def determine_intent(self, input_text):
        inputs = self.tokenizer(input_text, return_tensors="pt")
        with torch.no_grad():
            logits = self.model(**inputs).logits
        
        predicted_class_id = logits.argmax().item()
        predicted_intent = self.model.config.id2label[predicted_class_id]
        # return predicted_intent
        print(predicted_intent)


transformer = Transformer()
