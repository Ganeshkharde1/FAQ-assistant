# Intelligent FAQ Assistant

## Objective
This project is a Flask-based Intelligent FAQ Assistant that leverages Large Language Models (LLMs) and GenAI to dynamically respond to user queries based on a structured knowledge base. The assistant provides accurate answers, allows knowledge base updates, and logs interactions for future analysis.

## Features
- **Knowledge Base Integration**: Pre-load structured or unstructured knowledge (JSON, TXT, Markdown) and allow periodic updates.
- **Dynamic Query Handling**: Uses Google Gemini for intelligent responses based on user queries.
- **Flask Web Application**:
  - Simple web interface for query input and response display.
- **Admin Features**:
  - Allows knowledge base updates.
  - View interaction logs via API.
- **Interaction Logging**: Logs all queries and responses into Firebase for future analysis.
- **Fallback Mechanism**: Provides a fallback response when an answer is unavailable or suggests related topics.

## Tools & Technologies Used
- **LLM**: Google Gemini
- **Server Framework**: Flask
- **Database**: Firebase (for logging user interactions)
- **Text Processing**: `TfidfVectorizer` (for knowledge base search)

## How to Run the Project Locally
### Prerequisites
- Python3 installed
- Firebase credentials configured
- API key for Google Gemini

### Steps to Set Up and Run
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Ganeshkharde1/FAQ-assistant.git
   cd intelligent-faq-assistant
   ```


2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Firebase credentials**:
   - Download Firebase service account JSON file.
   - Place it in the project directory and configure the path in the Flask app.

4. **Update the Gemini API key**:
   ```bash
   # Set your Gemini API key
    genai.configure(api_key="Paste API Key")
   ```

5. **Update the Firebase Database API KEY**:
   ```bash
   firebase_admin.initialize_app(cred, {
    'databaseURL': "# Replace with your database URL"  
    })
   ```
   

6. **Run the Flask server**:
   ```bash
   python main.py
   ```

7. **Access the application**:
   - Open `http://127.0.0.1:5000/` in a browser.

## API Endpoints
- `POST /ask` - Accepts user queries and returns responses.
- `POST /update_knowledge` - Allows updating the knowledge base.
- `GET /logs` - Retrieves user interaction logs.


## License
This project is open-source and available under the MIT License.

---
Feel free to contribute or report issues!
