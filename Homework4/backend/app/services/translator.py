from transformers import MarianMTModel, MarianTokenizer
from typing import List

class Translator:
    def __init__(self):
        self.model_name = "Helsinki-NLP/opus-mt-mk-en"
        self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
        self.model = MarianMTModel.from_pretrained(self.model_name)

    def translate_text(self, text: str, max_length: int = 512) -> str:
        # Split long text into chunks to handle model limitations
        def chunk_text(text: str) -> List[str]:
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
            
            return chunks

        chunks = chunk_text(text)
        translated_chunks = []

        for chunk in chunks:
            encoded = self.tokenizer(chunk, return_tensors="pt", padding=True)
            translated = self.model.generate(**encoded)
            decoded = self.tokenizer.decode(translated[0], skip_special_tokens=True)
            translated_chunks.append(decoded)

        return ' '.join(translated_chunks)