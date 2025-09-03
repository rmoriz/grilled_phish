# Mastodon/Fediverse Post Analyzer

A Python CLI tool that analyzes Mastodon and other Fediverse posts for potential scams, phishing attempts, and fraudulent content using AI analysis via OpenRouter.

## Features

- 🔍 **Post Extraction**: Automatically extracts content from Mastodon/Fediverse URLs
- 📝 **Direct Text Analysis**: Analyze any text content without needing a URL
- 📥 **Stdin Support**: Read content from pipes, files, or clipboard for batch processing
- 🤖 **AI Analysis**: Uses OpenRouter API with free AI model to analyze content
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
   # Edit .env and add your OpenRouter API key and optionally set your preferred model
   ```

## Usage

### URL Analysis
Analyze posts directly from Mastodon/Fediverse URLs:

```bash
python mastodon_analyzer.py "https://mastodon.social/@user/123456789"
```

### Text Analysis
Analyze any text content without needing a URL - perfect for content from other platforms, messages, emails, or suspicious text you encounter:

```bash
python mastodon_analyzer.py "🚨 URGENT! Your account will be suspended! Click here: bit.ly/verify" --text
```

### Stdin Input
Read content from stdin for pipeline processing or file analysis:

```bash
# From a file
cat suspicious_message.txt | python mastodon_analyzer.py --stdin

# From clipboard (macOS)
pbpaste | python mastodon_analyzer.py --stdin --json

# From echo
echo "Click here to claim your prize!" | python mastodon_analyzer.py --stdin
```

### Basic Usage

```bash
# Analyze a post by URL
python mastodon_analyzer.py "https://mastodon.social/@user/123456789"

# Analyze text content directly
python mastodon_analyzer.py "🚨 URGENT! Click here to verify your account!" --text
```

### With Options

```bash
# Use a specific AI model
python mastodon_analyzer.py "https://example.social/@user/123" --model "anthropic/claude-3-sonnet"

# JSON output for programmatic use
python mastodon_analyzer.py "https://example.social/@user/123" --output json

# Simple JSON output (verdict, percentage, reason only)
python mastodon_analyzer.py "https://example.social/@user/123" --json

# Analyze text directly with JSON output
python mastodon_analyzer.py "Check out this amazing crypto opportunity!" --text --json

# Verbose mode for debugging
python mastodon_analyzer.py "https://example.social/@user/123" --verbose

# Use API key from command line
python mastodon_analyzer.py "https://example.social/@user/123" --api-key "your-key-here"

# Set model via environment variable
export OPENROUTER_MODEL="anthropic/claude-3-sonnet"
python mastodon_analyzer.py "https://example.social/@user/123"

# Analyze suspicious text content
python mastodon_analyzer.py "URGENT! Send me your password to verify account!" --text --verbose

# Read from stdin
echo "Free Bitcoin! Click now!" | python mastodon_analyzer.py --stdin --json
```

## Configuration

### Environment Variables

- `OPENROUTER_API_KEY`: Your OpenRouter API key (required)
- `OPENROUTER_MODEL`: AI model to use for analysis (optional, default: `openai/gpt-oss-20b:free`)

### Available AI Models

The tool uses the free OpenRouter model:
- `openai/gpt-oss-20b:free` ✅ **(default, free to use)**

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

### Simple JSON Output (--json)
Minimal JSON format for quick integration:
```json
{
  "verdict": "legitimate",
  "percentage": 85,
  "reason": "Post appears to be normal social media content with no suspicious indicators"
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