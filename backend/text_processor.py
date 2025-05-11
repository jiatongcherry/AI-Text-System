import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from transformers import pipeline
from typing import List, Tuple
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

class TextProcessor:
    """Base class for text processing utilities."""
    
    def __init__(self, model_name: str = "en_core_web_sm"):
        self.nlp = spacy.load(model_name)

class KeywordExtractor(TextProcessor):
    # (Unchanged from your original code)
    def __init__(self, corpus_path: str = "data/sample_corpus.txt"):
        super().__init__()
        try:
            with open(corpus_path, "r", encoding="utf-8") as f:
                self.corpus = f.read().split("\n\n")
        except FileNotFoundError:
            self.corpus = [""]
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=100
        )

    def preprocess(self, text: str) -> List[str]:
        doc = self.nlp(text.lower())
        candidates = []
        for token in doc:
            if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop:
                candidates.append(token.lemma_)
        for chunk in doc.noun_chunks:
            if not all(w.is_stop for w in chunk):
                candidates.append(chunk.text.lower())
        return candidates

    def extract_keywords(self, text: str, top_n: int = 5) -> List[Tuple[str, float]]:
        candidates = self.preprocess(text)
        if not candidates:
            return []
        documents = [text] + self.corpus
        tfidf_matrix = self.vectorizer.fit_transform(documents)
        feature_names = self.vectorizer.get_feature_names_out()
        scores = tfidf_matrix[0].toarray()[0]
        keyword_scores = [(word, scores[i]) for i, word in enumerate(feature_names) if word in candidates]
        return sorted(keyword_scores, key=lambda x: x[1], reverse=True)[:top_n]


class TextSummarizer(TextProcessor):
    """Class for generating abstractive text summaries using a transformer model."""
    
    def __init__(self, model_name: str = "sshleifer/distilbart-cnn-6-6", cache_dir: str = "D:/HuggingFaceCache"):
        super().__init__()
        # Load the tokenizer and model with cache_dir
        tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name, cache_dir=cache_dir)
        # Initialize the pipeline with the loaded model and tokenizer
        self.summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

    def preprocess(self, text: str) -> List[spacy.tokens.Span]:
        """Split text into sentences."""
        doc = self.nlp(text)
        return list(doc.sents)

    def summarize(self, text: str, ratio: float = 0.3) -> str:
        """Generate an abstractive summary of the text."""
        if not text.strip():
            return ""

        # Estimate desired summary length
        word_count = len(text.split())
        min_length = max(10, int(word_count * ratio * 0.5))
        max_length = max(20, int(word_count * ratio * 1.5))

        try:
            # Generate summary
            summary = self.summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )[0]["summary_text"]
            return summary.strip()
        except Exception as e:
            return f"Error generating summary: {str(e)}"