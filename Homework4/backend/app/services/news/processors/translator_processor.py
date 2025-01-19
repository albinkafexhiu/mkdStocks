from typing import Dict, Any
from transformers import MarianMTModel, MarianTokenizer
from .base_processor import NewsProcessor

class TranslatorProcessor(NewsProcessor):
    def __init__(self):
        super().__init__()
        self.model_name = "Helsinki-NLP/opus-mt-mk-en"
        self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
        self.model = MarianMTModel.from_pretrained(self.model_name)

    def translate_text(self, text: str, max_length: int = 512) -> str:
        words = text.split()
        chunks = []
        current_chunk = []

        for word in words:
            if len(' '.join(current_chunk + [word])) <= max_length:
                current_chunk.append(word)
            else:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        translated_chunks = []
        for chunk in chunks:
            encoded = self.tokenizer(chunk, return_tensors="pt", padding=True)
            translated = self.model.generate(**encoded)
            decoded = self.tokenizer.decode(translated[0], skip_special_tokens=True)
            translated_chunks.append(decoded)

        return ' '.join(translated_chunks)

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        for company, articles in data.items():
            for article in articles:
                article['title'] = {
                    'original': article['title'],
                    'translated': self.translate_text(article['title'])
                }
                article['content'] = {
                    'original': article['content'],
                    'translated': self.translate_text(article['content'])
                }
        return self.process_next(data)