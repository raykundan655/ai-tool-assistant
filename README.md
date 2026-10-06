# Agentic AI Chatbot with Tools

An AI chatbot built using **LangGraph**, **LangChain**, **Google Gemini API**, and **Streamlit**.

## Features
- **Tool Integration**:
  - Weather retrieval using WeatherAPI (`getweather`)
  - Calculator for math operations (`calculator`)
  - Web search via DuckDuckGo (`DuckDuckGoSearchRun`)
- **State & Memory Management**:
  - SQLite checkpointer for thread persistence (`SqliteSaver`)
- **Interactive UI**:
  - Streamlit sidebar for managing multi-thread conversations.

## Setup & Installation

1. **Clone the Repository**:
   ```bash
   git clone <YOUR_REPOSITORY_URL>
   cd AgenticAi
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_google_gemini_api_key
   WEATHER_API_KEY=your_weather_api_key
   ```

5. **Run the Application**:
   ```bash
   streamlit run tool_frontend.py
   ```
