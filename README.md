# Mastodon/Fediverse Post Analyzer

A Python CLI tool that analyzes Mastodon and other Fediverse posts for potential scams, phishing attempts, and fraudulent content using AI analysis via OpenRouter.

## Features

- 🔍 **Post Extraction**: Automatically extracts content from Mastodon/Fediverse URLs
- 🤖 **AI Analysis**: Uses OpenRouter API with various AI models to analyze content
- 🚨 **Scam Detection**: Identifies common scam patterns, phishing attempts, and fraud indicators
- 📊 **Detailed Reports**: Provides confidence scores, explanations, and recommendations
- 🎯 **Multiple Formats**: Supports both human-readable and JSON output
- 🌐 **Multi-Instance**: Works with any Mastodon instance and Fediverse platform

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your OpenRouter API key:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenRouter API key
   ```

## Usage

### Basic Usage

```bash
python mastodon_analyzer.py "https://mastodon.social/@user/123456789"
```

### With Options

```bash
# Use a specific AI model
python mastodon_analyzer.py "https://example.social/@user/123" --model "anthropic/claude-3-sonnet"

# JSON output for programmatic use
python mastodon_analyzer.py "https://example.social/@user/123" --output json

# Verbose mode for debugging
python mastodon_analyzer.py "https://example.social/@user/123" --verbose

# Use API key from command line
python mastodon_analyzer.py "https://example.social/@user/123" --api-key "your-key-here"
```

## Configuration

### Environment Variables

- `OPENROUTER_API_KEY`: Your OpenRouter API key (required)

### Available AI Models

The tool supports various AI models via OpenRouter:
- `anthropic/claude-3-haiku` (default, fast and cost-effective)
- `anthropic/claude-3-sonnet` (more thorough analysis)
- `openai/gpt-4` (OpenAI's GPT-4)
- `openai/gpt-3.5-turbo` (faster, less expensive)

## Output Formats

### Text Output (Default)
Human-readable format with:
- Post information (URL, instance, author)
- Content preview
- Analysis status with visual indicators
- Confidence score and category
- Detailed explanation
- Red flags detected
- Recommendations

### JSON Output
Structured data format including:
```json
{
  "url": "post_url",
  "post_data": {
    "content": "extracted_content",
    "author": "author_name",
    "instance": "instance_domain"
  },
  "analysis": {
    "is_suspicious": false,
    "confidence": 85,
    "category": "legitimate",
    "explanation": "detailed_analysis",
    "red_flags": [],
    "recommendations": "advice_for_users"
  }
}
```

## Detection Capabilities

The tool analyzes posts for various scam and phishing indicators:

### Scam Patterns
- Urgency tactics ("act now", "limited time")
- Too-good-to-be-true offers
- Cryptocurrency schemes
- Fake investment opportunities
- Impersonation attempts

### Phishing Indicators
- Requests for personal information
- Suspicious links
- Fake login prompts
- Account verification scams

### Content Analysis
- Grammar and spelling issues
- Emotional manipulation
- Social engineering tactics
- Fake giveaways or contests

## Examples

### Analyzing a Suspicious Post
```bash
$ python mastodon_analyzer.py "https://mastodon.social/@suspicious/123456"

============================================================
MASTODON POST ANALYSIS RESULTS
============================================================

Post URL: https://mastodon.social/@suspicious/123456
Instance: mastodon.social
Author: suspicious_user

Content:
----------------------------------------
🚨 URGENT! Your account will be suspended in 24 hours! 
Click here to verify: bit.ly/verify-now
Send us your password to confirm identity!
----------------------------------------

🚨 Status: SUSPICIOUS
Category: PHISHING
Confidence: 95%

Analysis:
This post exhibits multiple red flags typical of phishing attempts...

🚩 Red Flags Detected:
  • Urgency tactics to pressure immediate action
  • Requests for password/credentials
  • Suspicious shortened URL
  • Impersonation of official account actions

💡 Recommendations:
Do not click any links or provide personal information. Report this post to instance moderators.
```

## Getting an OpenRouter API Key

1. Visit [OpenRouter](https://openrouter.ai/)
2. Sign up for an account
3. Navigate to the API Keys section
4. Generate a new API key
5. Add it to your `.env` file or use the `--api-key` option

## Supported Platforms

This tool works with:
- Mastodon instances
- Pleroma instances
- Misskey instances
- Other ActivityPub-compatible platforms

## Error Handling

The tool gracefully handles:
- Invalid URLs
- Network timeouts
- API rate limits
- Parsing errors
- Missing content

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the tool.

## License

This project is open source. Please use responsibly and in accordance with the terms of service of the platforms you're analyzing.