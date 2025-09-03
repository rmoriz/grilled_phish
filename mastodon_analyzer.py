#!/usr/bin/env python3
"""
Mastodon/Fediverse Post Analyzer CLI
Analyzes posts for potential scams and phishing attempts using OpenRouter API.
"""

import re
import sys
import json
import requests
from urllib.parse import urlparse, urljoin
from typing import Optional, Dict, Any
import click
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


class MastodonPostExtractor:
    """Extracts post content from Mastodon/Fediverse URLs."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; MastodonAnalyzer/1.0)'
        })
    
    def extract_post_data(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Extract post data from a Mastodon/Fediverse URL.
        
        Args:
            url: The URL to the post
            
        Returns:
            Dictionary containing post data or None if extraction fails
        """
        try:
            # Parse the URL to understand the structure
            parsed_url = urlparse(url)
            
            # Try to get the post via web interface first
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract post content using various selectors
            post_data = self._extract_from_html(soup, url)
            
            # If HTML extraction fails, try API approach
            if not post_data.get('content'):
                post_data = self._try_api_extraction(url, parsed_url)
            
            return post_data
            
        except Exception as e:
            click.echo(f"Error extracting post: {e}", err=True)
            return None
    
    def _extract_from_html(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Extract post data from HTML content."""
        post_data = {
            'url': url,
            'content': '',
            'author': '',
            'timestamp': '',
            'instance': urlparse(url).netloc
        }
        
        # Try different selectors for different Mastodon interfaces
        content_selectors = [
            '.status__content',
            '.detailed-status__wrapper .status__content',
            '[data-testid="status-content"]',
            '.post-content',
            '.toot-content',
            'article .content',
            '.status-content'
        ]
        
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                post_data['content'] = content_elem.get_text(strip=True)
                break
        
        # Extract author information
        author_selectors = [
            '.status__display-name strong',
            '.detailed-status__display-name strong',
            '.display-name__account',
            '.author-name',
            '.username'
        ]
        
        for selector in author_selectors:
            author_elem = soup.select_one(selector)
            if author_elem:
                post_data['author'] = author_elem.get_text(strip=True)
                break
        
        # Try to extract from meta tags as fallback
        if not post_data['content']:
            og_description = soup.find('meta', property='og:description')
            if og_description:
                post_data['content'] = og_description.get('content', '')
        
        return post_data
    
    def _try_api_extraction(self, url: str, parsed_url) -> Dict[str, Any]:
        """Try to extract post data using Mastodon API."""
        post_data = {
            'url': url,
            'content': '',
            'author': '',
            'timestamp': '',
            'instance': parsed_url.netloc
        }
        
        try:
            # Extract post ID from URL
            post_id = self._extract_post_id(url)
            if not post_id:
                return post_data
            
            # Try Mastodon API endpoint
            api_url = f"https://{parsed_url.netloc}/api/v1/statuses/{post_id}"
            response = self.session.get(api_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                post_data['content'] = BeautifulSoup(data.get('content', ''), 'html.parser').get_text(strip=True)
                post_data['author'] = data.get('account', {}).get('display_name', '')
                post_data['timestamp'] = data.get('created_at', '')
        
        except Exception:
            pass  # Fallback to HTML extraction
        
        return post_data
    
    def _extract_post_id(self, url: str) -> Optional[str]:
        """Extract post ID from various Mastodon URL formats."""
        patterns = [
            r'/statuses/(\d+)',
            r'/@[^/]+/(\d+)',
            r'/posts/(\d+)',
            r'/status/(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None


class ScamAnalyzer:
    """Analyzes posts for scam/phishing content using OpenRouter API."""
    
    def __init__(self, api_key: str, model: str = "openai/gpt-oss-20b:free"):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        self.model = model
    
    def analyze_post(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a post for scam/phishing indicators.
        
        Args:
            post_data: Dictionary containing post information
            
        Returns:
            Analysis results
        """
        content = post_data.get('content', '')
        author = post_data.get('author', '')
        instance = post_data.get('instance', '')
        
        if not content:
            return {
                'error': 'No content to analyze',
                'is_suspicious': False,
                'confidence': 0,
                'explanation': 'No content found in the post'
            }
        
        prompt = self._create_analysis_prompt(content, author, instance)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a cybersecurity expert specializing in identifying scams, phishing attempts, and fraudulent content on social media platforms."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            result = response.choices[0].message.content
            return self._parse_analysis_result(result)
            
        except Exception as e:
            return {
                'error': f'Analysis failed: {str(e)}',
                'is_suspicious': False,
                'confidence': 0,
                'explanation': 'Could not complete analysis due to API error'
            }
    
    def _create_analysis_prompt(self, content: str, author: str, instance: str) -> str:
        """Create the analysis prompt for the AI model."""
        return f"""
Analyze the following social media post for potential scam, phishing, or fraudulent content:

POST CONTENT:
{content}

AUTHOR: {author}
INSTANCE: {instance}

Please analyze this post and determine if it appears to be:
1. A scam or fraudulent scheme
2. A phishing attempt
3. Legitimate content

Consider these factors:
- Urgency tactics ("act now", "limited time")
- Requests for personal information
- Suspicious links or promises
- Too-good-to-be-true offers
- Impersonation attempts
- Grammar and spelling issues
- Cryptocurrency or investment schemes
- Fake giveaways or contests

Respond in JSON format with:
{{
    "is_suspicious": boolean,
    "confidence": number (0-100),
    "category": "scam|phishing|legitimate|unclear",
    "explanation": "detailed explanation of your analysis",
    "red_flags": ["list", "of", "specific", "concerns"],
    "recommendations": "what users should do"
}}
"""
    
    def _parse_analysis_result(self, result: str) -> Dict[str, Any]:
        """Parse the AI analysis result."""
        try:
            # Try to extract JSON from the response
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback parsing if JSON format is not followed
                return {
                    'is_suspicious': 'suspicious' in result.lower() or 'scam' in result.lower(),
                    'confidence': 50,
                    'category': 'unclear',
                    'explanation': result,
                    'red_flags': [],
                    'recommendations': 'Manual review recommended'
                }
        except json.JSONDecodeError:
            return {
                'error': 'Could not parse analysis result',
                'is_suspicious': False,
                'confidence': 0,
                'explanation': result
            }


@click.command()
@click.argument('url')
@click.option('--api-key', envvar='OPENROUTER_API_KEY', help='OpenRouter API key')
@click.option('--model', envvar='OPENROUTER_MODEL', default='openai/gpt-oss-20b:free', help='AI model to use for analysis')
@click.option('--output', '-o', type=click.Choice(['text', 'json']), default='text', help='Output format')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def analyze(url: str, api_key: str, model: str, output: str, verbose: bool):
    """
    Analyze a Mastodon/Fediverse post for scam or phishing content.
    
    URL: The URL of the Mastodon/Fediverse post to analyze
    """
    if not api_key:
        click.echo("Error: OpenRouter API key is required. Set OPENROUTER_API_KEY environment variable or use --api-key option.", err=True)
        sys.exit(1)
    
    if verbose:
        click.echo(f"Analyzing URL: {url}")
    
    # Extract post data
    extractor = MastodonPostExtractor()
    post_data = extractor.extract_post_data(url)
    
    if not post_data:
        click.echo("Error: Could not extract post data from URL", err=True)
        sys.exit(1)
    
    if verbose:
        click.echo(f"Extracted post from: {post_data.get('instance', 'unknown')}")
        click.echo(f"Author: {post_data.get('author', 'unknown')}")
        click.echo(f"Content preview: {post_data.get('content', '')[:100]}...")
    
    # Analyze for scams/phishing
    analyzer = ScamAnalyzer(api_key, model)
    analysis = analyzer.analyze_post(post_data)
    
    # Output results
    if output == 'json':
        result = {
            'url': url,
            'post_data': post_data,
            'analysis': analysis
        }
        click.echo(json.dumps(result, indent=2))
    else:
        _display_text_results(post_data, analysis)


def _display_text_results(post_data: Dict[str, Any], analysis: Dict[str, Any]):
    """Display analysis results in human-readable format."""
    click.echo("\n" + "="*60)
    click.echo("MASTODON POST ANALYSIS RESULTS")
    click.echo("="*60)
    
    # Post information
    click.echo(f"\nPost URL: {post_data.get('url', 'N/A')}")
    click.echo(f"Instance: {post_data.get('instance', 'N/A')}")
    click.echo(f"Author: {post_data.get('author', 'N/A')}")
    
    click.echo(f"\nContent:")
    click.echo("-" * 40)
    click.echo(post_data.get('content', 'No content extracted'))
    click.echo("-" * 40)
    
    # Analysis results
    if 'error' in analysis:
        click.echo(f"\n❌ Analysis Error: {analysis['error']}")
        return
    
    is_suspicious = analysis.get('is_suspicious', False)
    confidence = analysis.get('confidence', 0)
    category = analysis.get('category', 'unclear')
    
    # Status indicator
    if is_suspicious:
        status_icon = "🚨"
        status_text = "SUSPICIOUS"
        status_color = "red"
    else:
        status_icon = "✅"
        status_text = "APPEARS LEGITIMATE"
        status_color = "green"
    
    click.echo(f"\n{status_icon} Status: ", nl=False)
    click.secho(status_text, fg=status_color, bold=True)
    click.echo(f"Category: {category.upper()}")
    click.echo(f"Confidence: {confidence}%")
    
    # Explanation
    explanation = analysis.get('explanation', 'No explanation provided')
    click.echo(f"\nAnalysis:")
    click.echo(explanation)
    
    # Red flags
    red_flags = analysis.get('red_flags', [])
    if red_flags:
        click.echo(f"\n🚩 Red Flags Detected:")
        for flag in red_flags:
            click.echo(f"  • {flag}")
    
    # Recommendations
    recommendations = analysis.get('recommendations', '')
    if recommendations:
        click.echo(f"\n💡 Recommendations:")
        click.echo(recommendations)
    
    click.echo("\n" + "="*60)


if __name__ == '__main__':
    analyze()