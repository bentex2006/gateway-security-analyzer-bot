#!/usr/bin/env python3
"""
Test script for website analysis
"""

import sys
sys.path.append('.')

from analyzers.website_analyzer import WebsiteAnalyzer
from config import Config

def test_website_analysis():
    """Test the website analysis with the reported problematic URL"""
    
    config = Config()
    analyzer = WebsiteAnalyzer(config)
    
    # Test the website that was incorrectly analyzed
    url = 'https://pierogerie.ca/'
    
    try:
        print(f"Testing URL: {url}")
        print("-" * 50)
        
        results = analyzer.analyze_website(url)
        
        print("Analysis Results:")
        print(f"  Cloudflare Detected: {results['cloudflare']['detected']}")
        print(f"  Cloudflare Evidence: {results['cloudflare']['evidence']}")
        print(f"  CAPTCHA Detected: {results['captcha']['detected']}")
        print(f"  CAPTCHA Types: {results['captcha'].get('types', [])}")
        print(f"  WordPress Detected: {results['wordpress']['detected']}")
        print(f"  WooCommerce Detected: {results['woocommerce']['detected']}")
        print(f"  CMS Detected: {results['cms']['detected']}")
        print(f"  GraphQL Detected: {results['graphql']['detected']}")
        
        return True
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        return False

if __name__ == "__main__":
    test_website_analysis()