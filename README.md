# Agent Zero: MCP Email Assistant

This project demonstrates a **Model Context Protocol (MCP)** integration using a Python-based email server and a Gradio web interface. The agent can intelligently read your Gmail inbox and compose/send emails based on natural language instructions.



## 🛠 Prerequisites

- **Conda** (Miniconda or Anaconda)
- **Gmail Account** with:
  - 2-Step Verification enabled.
  - An **App Password** generated.
  - IMAP enabled in Gmail Settings.

## 🚀 Getting Started

### 1. Environment Setup
Create and activate the specialized Conda environment:

```bash
conda env create -f environment.yml
conda activate mcp-email
```

### 2. Configuration (`.env`)
Create a `.env` file in the root directory:

```text
GOOGLE_API_KEY=your_gemini_api_key
SENDER_EMAIL=your_gmail@gmail.com
EMAIL_APP_PASSWORD=your_16_character_app_password
```

### 3. Run the Application
Start the Gradio interface:

```bash
python agent_zero.py
```

## 🤖 Example Prompts to Try

- **Direct Action**: "Email xxx@gmail.com and tell them the MCP tutorial is complete."
- **Read & Analyze**: "Check my last 3 emails and tell me if any of them are security alerts."
- **Multi-Step**: "Reverse the word 'Strawberry', then email the result to xxx@gmail.com with the subject 'Reversed Word'."
- **Summarization**: "Who sent my last 5 emails and what were they about?"



## ⚠️ Troubleshooting

- **Authentication Error**: Ensure your App Password has no spaces and IMAP is ON in Gmail.
- **Connection Refused**: Ensure `email_tools_server.py` is in the same folder as `agent_zero.py`.
- **Logic Errors**: If the agent can't reverse a word, ensure you added the `reverse_string` tool to the server file.