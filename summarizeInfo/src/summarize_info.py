from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from utils import clean_text, read_text_from_file, fetch_article_text, preprocess_text_for_abstractive_summarization, read_pdf 
import redis
import validators

class SummarizeInfo:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('sshleifer/distilbart-cnn-12-6')
        self.model = AutoModelForSeq2SeqLM.from_pretrained('sshleifer/distilbart-cnn-12-6')

        self.redis_instance = redis.Redis(
            host='127.0.0.1',
            port=6379,
            decode_responses=True
        )

    def summarize_article(self, article):
        is_url = validators.url(article)
        if is_url:
            text, cleaned_text = fetch_article_text(url=article)
        else:
            cleaned_text = read_text_from_file(article)
            cleaned_text = clean_text(cleaned_text)
        inputs = self.tokenizer(cleaned_text, max_length=1024, return_tensors="pt")
        # inputs = self.tokenizer(article, max_length=1024, return_tensors="pt")
        summary_ids = self.model.generate(inputs["input_ids"], num_beams=2, min_length=0, max_length=20)
        return self.tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    
summary = SummarizeInfo()
article = "PG&E stated it scheduled the blackouts in response to forecasts for high winds amid dry conditions. The aim is to reduce the risk of wildfires. Nearly 800 thousand customers were scheduled to be affected by the shutoffs which were expected to last through at least midday tomorrow."
print(summary.summarize_article(article))