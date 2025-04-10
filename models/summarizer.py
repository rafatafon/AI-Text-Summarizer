"""
AI Text Summarizer Models
This module contains the implementation of both extractive and abstractive summarization techniques.
"""

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from transformers import pipeline
import torch

# Download necessary NLTK data
try:
    nltk.data.find("tokenizers/punkt")
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("punkt")
    nltk.download("stopwords")


class TextSummarizer:
    def __init__(self):
        """Initialize the summarizer with both extractive and abstractive capabilities."""
        # Check if CUDA is available
        self.device = 0 if torch.cuda.is_available() else -1

        # Initialize abstractive summarizer
        try:
            self.abstractive_summarizer = pipeline(
                "summarization", model="facebook/bart-large-cnn", device=self.device
            )
        except Exception as e:
            print(f"Error loading abstractive model: {e}")
            self.abstractive_summarizer = None

    def extractive_summarize(self, text, ratio=0.3):
        """
        Generate an extractive summary by selecting the most important sentences.

        Args:
            text (str): The input text to summarize
            ratio (float): The proportion of sentences to include in the summary (0.0-1.0)

        Returns:
            str: The extractive summary
        """
        if not text or len(text.strip()) == 0:
            return "No text provided for summarization."

        # Tokenize the text into sentences and words
        sentences = sent_tokenize(text)
        words = word_tokenize(text.lower())

        # Remove stopwords
        stop_words = set(stopwords.words("english"))
        filtered_words = [
            word for word in words if word.isalnum() and word not in stop_words
        ]

        # Calculate word frequencies
        word_frequencies = FreqDist(filtered_words)

        # Calculate sentence scores based on word frequencies
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            for word in word_tokenize(sentence.lower()):
                if word in word_frequencies:
                    if i not in sentence_scores:
                        sentence_scores[i] = 0
                    sentence_scores[i] += word_frequencies[word]

        # Normalize sentence scores by sentence length
        for i in sentence_scores:
            sentence_scores[i] = sentence_scores[i] / len(word_tokenize(sentences[i]))

        # Select top sentences
        num_sentences = max(1, int(len(sentences) * ratio))
        top_sentences = sorted(
            sentence_scores.items(), key=lambda x: x[1], reverse=True
        )[:num_sentences]
        top_sentences = sorted(
            top_sentences, key=lambda x: x[0]
        )  # Sort by original position

        # Combine selected sentences
        summary = " ".join([sentences[i] for i, _ in top_sentences])

        return summary

    def abstractive_summarize(self, text, max_length=150, min_length=50):
        """
        Generate an abstractive summary using a pre-trained transformer model.

        Args:
            text (str): The input text to summarize
            max_length (int): Maximum length of the summary
            min_length (int): Minimum length of the summary

        Returns:
            str: The abstractive summary
        """
        if not text or len(text.strip()) == 0:
            return "No text provided for summarization."

        if self.abstractive_summarizer is None:
            return "Abstractive summarization model is not available."

        try:
            # Truncate input if it's too long (BART has a limit of 1024 tokens)
            max_input_length = 1024
            words = text.split()
            if len(words) > max_input_length:
                text = " ".join(words[:max_input_length])

            # Generate summary
            summary = self.abstractive_summarizer(
                text, max_length=max_length, min_length=min_length, do_sample=False
            )

            return summary[0]["summary_text"]
        except Exception as e:
            return f"Error generating abstractive summary: {str(e)}"

    def summarize(self, text, method="abstractive", **kwargs):
        """
        Summarize text using the specified method.

        Args:
            text (str): The input text to summarize
            method (str): The summarization method ('extractive' or 'abstractive')
            **kwargs: Additional arguments for the specific summarization method

        Returns:
            str: The generated summary
        """
        if method.lower() == "extractive":
            ratio = kwargs.get("ratio", 0.3)
            return self.extractive_summarize(text, ratio)
        else:  # default to abstractive
            max_length = kwargs.get("max_length", 150)
            min_length = kwargs.get("min_length", 50)
            return self.abstractive_summarize(text, max_length, min_length)
