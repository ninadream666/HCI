# **Multi-Model Chatbot System**

This project implements a multi-model chatbot system that allows users to interact with two language models, OpenAI and DeepSeek. It leverages Gradio for the UI, and includes features such as multi-turn conversations, chat history, and model selection.

### **Features**

* Multi-Model Support: Choose between OpenAI and DeepSeek for generating responses.

* Multi-Turn Conversations: Continue conversations from previous exchanges.

* Chat History: View and interact with past conversations.
* Customizable UI: Enhanced user interface with a clean, modern design.

### **Requirements**

Before running the program, make sure to install the following dependencies:

* Python 3.7 or later

* Gradio

* OpenAI API (for OpenAI model support)

* DeepSeek API (for DeepSeek model support)

You can install the required libraries with:


`pip install gradio openai requests`
`

Make sure you have the correct API keys for both OpenAI and DeepSeek in your environment or configuration file.

### **Project Structure**


- **api/**：
  - **__init__.py**：#Mark a directory as a Python package
  - **openai_api.py**：# OpenAI API call functionality
  - **deepseek_api.py**：# DeepSeek API call functionality
  
- **chat/**：

  - **__init__.py**：#Mark a directory as a Python package
  - **history_manager.py**：# History management (saving/loading conversation history)
  - **history.json**：#Record the conversation
- **app.py**：# Main Gradio application file
- **config.py**: #Store the API keys
- **README.md**： # This readme file



### **How to Run**

#### 1. Setup API Keys

Before running the application, ensure that your API keys for OpenAI and DeepSeek are properly set up:

* For OpenAI:

    Sign up at OpenAI and get your API key.

    Set the key as an environment variable:

  `export OPENAI_API_KEY="your_openai_api_key"`
* For DeepSeek:

    Obtain the API key from DeepSeek and set it similarly as an environment variable.


#### 2. Install Dependencies

Install the required Python libraries:

`pip install -r requirements.txt`

Ensure you have openai and gradio installed for API calls and interface rendering.

#### 3. Run the Application

Once everything is set up, run the app.py file:

`python app.py`

This will launch a local Gradio interface in your browser.

#### 4. Use the Chatbot

* Select a Model: Choose between "OpenAI" and "DeepSeek" in the radio button.

* Enter a Question: Type your query in the text input box and click "Send".

* Continue Conversation: If you wish to continue a previous conversation, you can click the "🔄 继续对话" button next to the relevant history to continue the conversation.

* Customization Styling: The UI is customizable by editing the custom_css string in the main.py file.

* API Integration: You can replace the existing API calls in api/openai_api.py and api/deepseek_api.py with your custom models or APIs.