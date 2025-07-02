# Gateway Security Analyzer Bot

## Overview

This is a comprehensive Telegram bot designed for website security and technology analysis. The bot allows users to analyze websites for various security features, payment systems, technology stacks, and security configurations. It provides detailed insights about website protection mechanisms, SSL certificates, and underlying technologies.

## System Architecture

The application follows a modular architecture with clear separation of concerns:

- **Main Application**: Entry point that orchestrates the bot functionality
- **Configuration Layer**: Centralized configuration management
- **Database Layer**: Simple file-based storage for user approvals and settings
- **Handler Layer**: Separated command handlers for different functionalities
- **Analyzer Layer**: Specialized modules for different types of website analysis
- **Utility Layer**: Common utilities for validation and formatting

## Key Components

### Core Components

1. **GatewayBot (`main.py`)**: Main bot class that initializes all components and handles the application lifecycle
2. **Configuration (`config.py`)**: Centralized configuration including bot token, admin IDs, and various detection patterns
3. **Database (`database.py`)**: File-based JSON storage for user approvals and group settings

### Handler Components

1. **AdminHandlers**: Manages admin-only commands like user approval and group usage controls
2. **URLHandler**: Processes URL analysis requests and orchestrates various analyzers

### Analyzer Components

1. **WebsiteAnalyzer**: Detects technologies, CMS platforms, and general website characteristics
2. **SecurityAnalyzer**: Analyzes security headers and configurations
3. **SSLAnalyzer**: Examines SSL certificates and their validity
4. **PaymentAnalyzer**: Identifies payment systems and gateways

### Utility Components

1. **URLValidator**: Validates and normalizes URLs
2. **MessageFormatter**: Formats analysis results into readable Telegram messages

## Data Flow

1. User sends `/url <website>` command to the bot
2. URLHandler validates user permissions based on chat type and approval status
3. URL is validated and normalized by URLValidator
4. Multiple analyzers run in parallel to examine different aspects of the website
5. Results are aggregated and formatted by MessageFormatter
6. Formatted response is sent back to the user with analysis results

## External Dependencies

### Third-Party Libraries
- **python-telegram-bot**: Telegram Bot API integration
- **requests**: HTTP client for website analysis
- **beautifulsoup4**: HTML parsing and analysis
- **urllib**: URL parsing and manipulation

### External Services
- **Telegram Bot API**: Primary interface for bot communication
- **Target Websites**: Analyzed through HTTP requests and SSL connections

## Deployment Strategy

The bot is designed for VPS deployment with the following characteristics:

- **Polling-based**: Uses long polling to receive updates from Telegram
- **File-based Storage**: Simple JSON file storage for persistence
- **Environment Variables**: Bot token configurable via environment variables
- **Error Handling**: Comprehensive error handling with graceful degradation
- **Logging**: Structured logging for monitoring and debugging

### Deployment Requirements
- Python 3.7+
- Network access for HTTP/HTTPS requests
- Write permissions for database file storage
- Telegram Bot Token

## Changelog

```
Changelog:
- July 01, 2025: Initial setup and architecture design
- July 01, 2025: Fixed python-telegram-bot installation and import issues
- July 01, 2025: Bot successfully deployed and running with all features operational
- July 02, 2025: Fixed critical analysis accuracy issues:
  * Fixed Cloudflare detection false positives (nginx servers incorrectly flagged)
  * Improved GraphQL detection to avoid false matches from generic HTML content
  * Updated payment gateway detection to use regex patterns from reference script
  * Eliminated payment system false positives (Square/Stripe/PayPal from CSS/FontAwesome)
- July 02, 2025: Comprehensive detection expansion based on professional security analysis patterns:
  * Expanded GraphQL paths: Added /graphiql, /graphql/playground, /gql, /_graphql and 6 more variants
  * Enhanced CAPTCHA detection: Added Arkose Labs, FunCaptcha, DataDome, PerimeterX and 4 more systems
  * Extended WordPress indicators: Added wp-login, xmlrpc.php, wp-cron and 5 more endpoints
  * Payment gateways expansion: Added 9 additional providers (Mollie, Alipay, Afterpay, Revolut, etc.)
  * Security headers upgrade: Added 6 modern headers (Cross-Origin policies, Expect-CT)
  * CDN detection enhancement: Added AWS CloudFront, Cloudflare APO headers
  * WAF detection: Added Sucuri, Akamai, FireEye, StackPath and 4 more WAF indicators
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```

### Architecture Decisions

**File-based Database**: Chosen for simplicity and ease of deployment. The application uses JSON file storage instead of a full database system, making it lightweight and reducing deployment complexity. This approach is suitable for the expected user base and provides persistence without additional infrastructure requirements.

**Modular Analyzer Design**: Each type of analysis (security, SSL, payment, website) is handled by a separate analyzer class. This design allows for easy extension of functionality and maintains clear separation of concerns. New analysis types can be added without modifying existing code.

**Permission System**: Implements a dual-permission system with admin approval for individual users and group-level controls. Admins can approve users globally or enable/disable bot usage per group, providing flexible access control.

**Asynchronous Architecture**: Uses python-telegram-bot's async framework for handling multiple requests efficiently, ensuring the bot remains responsive under load.

**Error Handling Strategy**: Implements comprehensive error handling with timeouts, graceful degradation, and user-friendly error messages. Network issues, invalid URLs, and analysis failures are handled without crashing the bot.