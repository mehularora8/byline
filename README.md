# Executive Summary Agent

An AI-powered executive summary generator that uses Exa search API and OpenAI GPT-4 to create personalized reports based on user interests.

## Features

- **Intelligent Search**: Uses Exa API for web search with date filtering
- **AI-Powered Summaries**: OpenAI GPT-4 generates executive summaries
- **Email Delivery**: Automatically sends reports via email using yagmail
- **Comprehensive Logging**: Detailed logging to both file and console
- **User Interest Tracking**: Personalized reports based on user interests

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# API Keys
EXA_API_KEY=your-exa-api-key-here
OPENAI_API_KEY=your-openai-api-key-here

# Email Configuration (Gmail recommended)
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password-here
```

### 3. Gmail App Password Setup

For Gmail, you need to use an App Password:

1. Enable 2-factor authentication on your Google account
2. Go to Google Account settings > Security > App passwords
3. Generate a new app password for "Mail"
4. Use this app password in your `.env` file

### 4. Update User Email

In `exec.py`, update the user email address:

```python
user = User(
    email="your-actual-email@example.com",  # Replace with actual email
    user_interests=user_interest
)
```

## Usage

Run the script:

```bash
python exec.py
```

The script will:
1. Generate an executive summary based on user interests
2. Print the summary to console
3. Send the summary via email
4. Log all activities to `executive_summary.log`

## Logging

All activities are logged to:
- Console output
- `executive_summary.log` file

Logs include:
- API calls and responses
- Email sending status
- Error handling
- Performance metrics

## Classes

- **UserInterest**: Stores user topics, keywords, and preferred domains
- **User**: Contains user email and interests
- **ExaSearch**: Handles Exa API integration with date filtering
- **ExecutiveSummaryAgent**: AI agent using OpenAI function calling
- **EmailService**: Handles email delivery via yagmail 