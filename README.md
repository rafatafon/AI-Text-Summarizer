# AI-Powered Text Summarizer

![Text Summarizer Banner](https://img.shields.io/badge/AI-Text%20Summarizer-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-brightgreen)
![Flask](https://img.shields.io/badge/Flask-2.3.3-lightgrey)
![Transformers](https://img.shields.io/badge/Transformers-4.35.0-orange)

A web-based application that uses AI to generate concise summaries of long texts. The application supports both extractive (key sentences) and abstractive (AI-generated) summarization methods.

## 🌟 Features

- **Dual Summarization Methods**:
  - **Extractive**: Identifies and extracts key sentences from the original text
  - **Abstractive**: Generates a new, concise summary using AI language models
  
- **User-Friendly Interface**:
  - Clean, responsive design
  - Text input area and file upload option
  - Customizable summarization parameters
  - Input values preserved after generating summaries
  
- **Summary Statistics**:
  - Word count comparison
  - Reduction percentage
  - Method used
  
- **Convenient Actions**:
  - Copy summary to clipboard
  - Download summary as text file
  
- **API Support**:
  - RESTful API endpoint for integration with other applications
  - JSON request/response format

## 🛠️ Technology Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python, Flask
- **AI Models**:
  - Hugging Face Transformers (BART for abstractive summarization)
  - NLTK (for extractive summarization)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ai-text-summarizer.git
   cd ai-text-summarizer
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the application**:
   Open your web browser and navigate to `http://127.0.0.1:5000`

## 🔌 API Usage

### Endpoint: `/api/summarize`

**Request Format**:
```json
{
  "text": "Your long text to summarize goes here...",
  "method": "abstractive",  // or "extractive"
  "max_length": 150,        // for abstractive summarization
  "min_length": 50,         // for abstractive summarization
  "ratio": 0.3              // for extractive summarization
}
```

**Response Format**:
```json
{
  "summary": "The generated summary text...",
  "original_length": 500,
  "summary_length": 150,
  "reduction_percentage": 70.0
}
```

## 📂 Project Structure

```
text-summarizer/
│── app.py                # Flask application with route handlers
│── models/
│   └── summarizer.py     # Summarization models implementation
│── static/
│   ├── style.css         # CSS styles for the interface
│   └── main.js           # JavaScript for UI interactions and validation
│── templates/
│   └── index.html        # HTML template with form elements
│── requirements.txt      # Project dependencies
└── README.md            # Project documentation
```

## 🧠 How It Works

### User Input Persistence
The application preserves user input values (text, parameters) after generating a summary, which:
1. Improves user experience by eliminating the need to re-enter values for subsequent summaries
2. Maintains context between summarization attempts
3. Allows for easy parameter adjustments when fine-tuning the summary output

### Extractive Summarization
The extractive summarization method works by:
1. Tokenizing the text into sentences
2. Removing stopwords
3. Calculating word frequencies
4. Scoring sentences based on the frequency of their words
5. Selecting the top-scoring sentences to form the summary

### Abstractive Summarization
The abstractive summarization method uses the BART model from Facebook AI, which:
1. Processes the input text through an encoder-decoder architecture
2. Generates a new summary that captures the essence of the original text
3. Can produce summaries that include phrases not present in the original text

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Hugging Face Transformers](https://huggingface.co/transformers/) for the pre-trained models
- [NLTK](https://www.nltk.org/) for natural language processing tools
- [Flask](https://flask.palletsprojects.com/) for the web framework
