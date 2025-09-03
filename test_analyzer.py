#!/usr/bin/env python3
"""
Test script for the Mastodon Post Analyzer
"""

import os
import sys
from mastodon_analyzer import MastodonPostExtractor, ScamAnalyzer

def test_post_extraction():
    """Test post extraction functionality with mock data."""
    print("Testing post extraction...")
    
    extractor = MastodonPostExtractor()
    
    # Test URL parsing
    test_urls = [
        "https://mastodon.social/@user/123456789",
        "https://fosstodon.org/@developer/987654321",
        "https://mas.to/@someone/555666777"
    ]
    
    for url in test_urls:
        post_id = extractor._extract_post_id(url)
        print(f"URL: {url} -> Post ID: {post_id}")

def test_analysis_with_mock_data():
    """Test analysis with mock post data."""
    print("\nTesting analysis with mock data...")
    
    # Mock API key for testing (won't actually call API)
    api_key = os.getenv('OPENROUTER_API_KEY', 'test-key')
    
    if api_key == 'test-key':
        print("⚠️  No real API key found. Set OPENROUTER_API_KEY to test with real API.")
        return
    
    analyzer = ScamAnalyzer(api_key)
    
    # Test with suspicious content
    suspicious_post = {
        'content': '🚨 URGENT! Your account will be suspended! Click here: bit.ly/verify-now Send password to confirm!',
        'author': 'fake_support',
        'instance': 'suspicious.example',
        'url': 'https://suspicious.example/@fake_support/123'
    }
    
    print("Analyzing suspicious post...")
    result = analyzer.analyze_post(suspicious_post)
    print(f"Result: {result}")
    
    # Test with legitimate content
    legitimate_post = {
        'content': 'Just finished reading a great book about cybersecurity. Highly recommend "The Art of Deception" by Kevin Mitnick!',
        'author': 'book_lover',
        'instance': 'mastodon.social',
        'url': 'https://mastodon.social/@book_lover/456'
    }
    
    print("\nAnalyzing legitimate post...")
    result = analyzer.analyze_post(legitimate_post)
    print(f"Result: {result}")

def show_usage_examples():
    """Show usage examples."""
    print("\n" + "="*60)
    print("USAGE EXAMPLES")
    print("="*60)
    
    examples = [
        "# Basic URL analysis",
        "python mastodon_analyzer.py 'https://mastodon.social/@user/123456789'",
        "",
        "# Direct text analysis",
        "python mastodon_analyzer.py 'URGENT! Click here to verify your account!' --text",
        "",
        "# Simple JSON output",
        "python mastodon_analyzer.py 'Check out this crypto opportunity!' --text --json",
        "",
        "# Full JSON output",
        "python mastodon_analyzer.py 'https://mas.to/@user/123' --output json",
        "",
        "# Verbose mode with text",
        "python mastodon_analyzer.py 'Send me your password to confirm!' --text --verbose",
        "",
        "# Read from stdin",
        "echo 'Free Bitcoin! Click now!' | python mastodon_analyzer.py --stdin --json",
        "",
        "# From file via stdin",
        "cat suspicious_message.txt | python mastodon_analyzer.py --stdin",
        "",
        "# With API key from command line",
        "python mastodon_analyzer.py 'https://example.social/@user/123' --api-key 'your-key'"
    ]
    
    for example in examples:
        print(example)

if __name__ == '__main__':
    print("Mastodon Post Analyzer - Test Suite")
    print("="*50)
    
    test_post_extraction()
    test_analysis_with_mock_data()
    show_usage_examples()
    
    print(f"\n✅ Tests completed!")
    print(f"📝 To use the analyzer, first set your OpenRouter API key:")
    print(f"   export OPENROUTER_API_KEY='your-api-key-here'")
    print(f"🚀 Then run: python mastodon_analyzer.py 'https://your-mastodon-url'")