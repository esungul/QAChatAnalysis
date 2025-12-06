# QA Analysis Tool

World-class web-based tool for analyzing customer service calls/chats using OpenAI LLM. Prioritizes accuracy for single/multiple transactions.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Set OPENAI_API_KEY in environment (e.g., .env or Colab secrets).
3. Run: `streamlit run app.py`

## Features
- Strict scoring for first response and verification.
- Dashboard with metrics, charts, expanders.
- Modular for easy extension (e.g., batch analysis).

## Extending
- For voice: Add audio transcription in utils/.
- For multi-transaction: Update app.py to loop over inputs.



/Users/esungul/Documents/Projects/WindstreamQA/qa_analysis_tool
esungul@Sunnys-MacBook-Air qa_analysis_tool % streamlit run app.py

