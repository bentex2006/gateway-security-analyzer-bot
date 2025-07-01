"""
Configuration settings for the Gateway Bot
"""

import os

class Config:
    """Configuration class for bot settings"""
    
    # Bot token from environment or hardcoded fallback
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7993523214:AAE9n49ZyssohfTf70WRrvov9f-pZQ0166Y")
    
    # Admin user IDs
    ADMIN_IDS = [7581739321, 6496521179]
    
    # GIF URLs for different states
    START_GIF = "https://c.tenor.com/OF2oQX_PQ9UAAAAC/tenor.gif"
    PROCESSING_GIF = "https://c.tenor.com/M_oXsH0cwlwAAAAd/tenor.gif"
    RESULT_GIF = "https://c.tenor.com/fFUaQ62gNx8AAAAd/tenor.gif"
    
    # Request settings
    REQUEST_TIMEOUT = 10
    MAX_REDIRECTS = 5
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    
    # GraphQL common paths to check
    GRAPHQL_PATHS = [
        "/graphql",
        "/api/graphql",
        "/v1/graphql",
        "/query",
        "/api/query",
        "/graphql-api"
    ]
    
    # Common CAPTCHA indicators
    CAPTCHA_INDICATORS = [
        "recaptcha",
        "hcaptcha",
        "captcha",
        "g-recaptcha",
        "h-captcha",
        "cf-turnstile",
        "turnstile",
        "geetest"
    ]
    
    # WordPress/WooCommerce indicators
    WORDPRESS_INDICATORS = [
        "wp-content",
        "wp-includes",
        "wordpress",
        "woocommerce",
        "wp-admin",
        "wp-json"
    ]
    
    # Payment system indicators
    PAYMENT_INDICATORS = {
        "stripe": ["stripe", "js.stripe.com"],
        "paypal": ["paypal", "paypalobjects.com"],
        "square": ["square", "squareup.com"],
        "braintree": ["braintree", "js.braintreegateway.com"],
        "authorize.net": ["authorize.net", "authorizenet"],
        "razorpay": ["razorpay", "checkout.razorpay.com"],
        "coinbase": ["coinbase", "coinbase.com"],
        "bitcoin": ["bitcoin", "btc"],
        "cryptocurrency": ["crypto", "bitcoin", "ethereum", "litecoin"]
    }
    
    # Security headers to check
    SECURITY_HEADERS = [
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "X-XSS-Protection",
        "Referrer-Policy",
        "Permissions-Policy"
    ]
    
    # Cloudflare indicators
    CLOUDFLARE_HEADERS = [
        "cf-ray",
        "cf-cache-status",
        "cf-request-id",
        "server"
    ]
