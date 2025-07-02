import os

class Config:
    
    # Bot token from environment or hardcoded fallback
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    
    # Admin user IDs
    ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
    
    # GIF URLs for different states
    START_GIF = "https://c.tenor.com/OF2oQX_PQ9UAAAAC/tenor.gif"
    PROCESSING_GIF = "https://c.tenor.com/M_oXsH0cwlwAAAAd/tenor.gif"
    RESULT_GIF = "https://c.tenor.com/fFUaQ62gNx8AAAAd/tenor.gif"
    
    # Request settings
    REQUEST_TIMEOUT = 10
    MAX_REDIRECTS = 5
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    
    # GraphQL common paths to check (expanded)
    GRAPHQL_PATHS = [
        "/graphql",
        "/api/graphql",
        "/v1/graphql",
        "/query",
        "/api/query",
        "/graphql-api",
        "/graphql/playground",
        "/graphiql",
        "/api/v2/graphql",
        "/v2/graphql",
        "/graphql-explorer",
        "/graphql/query",
        "/gql",
        "/_graphql",
        "/graphql/v1"
    ]
    
    # Common CAPTCHA indicators (expanded)
    CAPTCHA_INDICATORS = [
        "recaptcha",
        "hcaptcha",
        "captcha",
        "g-recaptcha",
        "h-captcha",
        "cf-turnstile",
        "turnstile",
        "geetest",
        "arkose",
        "arkose-labs",
        "funcaptcha",
        "bot-detection",
        "captcha-id",
        "turnstile-widget",
        "datadome",
        "perimeterx"
    ]
    
    # WordPress/WooCommerce indicators (expanded)
    WORDPRESS_INDICATORS = [
        "wp-content",
        "wp-includes",
        "wordpress",
        "woocommerce",
        "wp-admin",
        "wp-json",
        "wp-login",
        "wp-cron",
        "wp-signup",
        "wp-comments-post",
        "wp-blog-header",
        "wp-trackback",
        "xmlrpc.php"
    ]
    
    # Payment gateway patterns (comprehensive collection)
    PAYMENT_GATEWAY_PATTERNS = {
        "PayPal": r"paypal\.com|paypalobjects|paypal\.js|paypal-checkout",
        "Stripe": r"stripe\.com|stripejs|stripe-api|js\.stripe\.com|pk_live_|pk_test_|stripe\.js",
        "Braintree": r"braintreegateway\.com|braintree\.js|braintree-web",
        "Square": r"squareup\.com|square\.js|connect\.squareup\.com|js\.squareup\.com",
        "Authorize.net": r"authorize\.net|authorizenet|accept\.js",
        "2Checkout": r"2checkout\.com|avangate", 
        "Adyen": r"adyen\.com|adyen\.js",
        "Worldpay": r"worldpay\.com",
        "SagePay": r"sagepay\.com",
        "Razorpay": r"razorpay\.com|checkout\.razorpay\.com",
        "Klarna": r"klarna\.com|klarna\.js",
        "Amazon Pay": r"pay\.amazon\.com|amazon-payments",
        "WePay": r"wepay\.com",
        "PayU": r"payu\.in|payu\.com",
        "Mollie": r"mollie\.com|mollie\.js",
        "Payoneer": r"payoneer\.com",
        "Paytm": r"paytm\.com|securegw\.paytm",
        "Alipay": r"alipay\.com",
        "Afterpay": r"afterpay\.com",
        "Sezzle": r"sezzle\.com",
        "Affirm": r"affirm\.com",
        "Zip": r"zip\.co",
        "Revolut": r"revolut\.com",
        "Shopify": r"shopify\.com|shopify|cdn\.shopify\.com|shop\.js|shopify-pay"
    }
    
    # Security headers to check (expanded)
    SECURITY_HEADERS = [
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "X-XSS-Protection",
        "Referrer-Policy",
        "Permissions-Policy",
        "Cross-Origin-Opener-Policy",
        "Cross-Origin-Embedder-Policy",
        "Cross-Origin-Resource-Policy",
        "X-Permitted-Cross-Domain-Policies",
        "Expect-CT",
        "Access-Control-Allow-Origin"
    ]
    
    # CDN and Protection Service Headers (expanded)
    CLOUDFLARE_HEADERS = [
        "cf-ray",
        "cf-cache-status",
        "cf-request-id",
        "cf-apo-via",
        "cf-edge-cache",
        "cf-bgj",
        "server-timing",
        "x-amz-cf-id",
        "x-amz-cf-pop"
    ]
    
    # WAF and Security Service Indicators
    WAF_INDICATORS = [
        "X-Sucuri-ID",
        "X-Akamai-Transformed",
        "X-FireEye",
        "X-Distil-CS",
        "X-Imunify360",
        "X-StackPath-Cache",
        "X-CDN",
        "X-Powered-By-360wzb"
    ]
