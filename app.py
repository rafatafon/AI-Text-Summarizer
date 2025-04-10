from flask import Flask, render_template, request, jsonify
from models.summarizer import TextSummarizer

app = Flask(__name__)
summarizer = TextSummarizer()


@app.route("/")
def index():
    """Render the main page of the application."""
    return render_template("index.html")


@app.route("/summarize", methods=["POST"])
def summarize_text():
    """
    Handle text summarization requests from the web interface.
    Returns the summarized text to be displayed on the web page.
    """
    if request.method == "POST":
        # Get form data
        text = request.form.get("text", "")
        method = request.form.get("method", "abstractive")

        # Handle file upload if present
        if "file" in request.files:
            file = request.files["file"]
            if file.filename != "":
                try:
                    text = file.read().decode("utf-8")
                except Exception as e:
                    return render_template(
                        "index.html", error=f"Error reading file: {str(e)}"
                    )

        if not text:
            return render_template(
                "index.html", error="No text provided for summarization."
            )

        # Get additional parameters based on the method
        if method == "extractive":
            ratio = float(request.form.get("ratio", 0.3))
            summary = summarizer.summarize(text, method="extractive", ratio=ratio)
        else:  # abstractive
            max_length = int(request.form.get("max_length", 150))
            min_length = int(request.form.get("min_length", 50))
            summary = summarizer.summarize(
                text, method="abstractive", max_length=max_length, min_length=min_length
            )

        # Calculate statistics
        original_length = len(text.split())
        summary_length = len(summary.split())
        reduction = (
            round((1 - summary_length / original_length) * 100, 1)
            if original_length > 0
            else 0
        )

        # Preserve all user input values
        input_values = {
            "original_text": text,
            "summary": summary,
            "method": method,
            "original_length": original_length,
            "summary_length": summary_length,
            "reduction": reduction,
        }

        # Add method-specific parameters
        if method == "extractive":
            input_values["ratio"] = ratio
        else:  # abstractive
            input_values["max_length"] = max_length
            input_values["min_length"] = min_length

        return render_template("index.html", **input_values)


@app.route("/api/summarize", methods=["POST"])
def api_summarize():
    """
    API endpoint for text summarization.
    Accepts JSON input and returns JSON output.
    """
    try:
        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({"error": "No text provided for summarization"}), 400

        text = data.get("text", "")
        method = data.get("method", "abstractive")

        if method == "extractive":
            ratio = float(data.get("ratio", 0.3))
            summary = summarizer.summarize(text, method="extractive", ratio=ratio)
        else:  # abstractive
            max_length = int(data.get("max_length", 150))
            min_length = int(data.get("min_length", 50))
            summary = summarizer.summarize(
                text, method="abstractive", max_length=max_length, min_length=min_length
            )

        # Calculate statistics
        original_length = len(text.split())
        summary_length = len(summary.split())
        reduction = (
            round((1 - summary_length / original_length) * 100, 1)
            if original_length > 0
            else 0
        )

        return jsonify(
            {
                "summary": summary,
                "original_length": original_length,
                "summary_length": summary_length,
                "reduction_percentage": reduction,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Use debug=True for local development only
    app.run(debug=True)
