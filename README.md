# MCP (Model Context Protocol) Project

## Overview
This project implements a Model Context Protocol (MCP) system for automated flight searches and browser interactions. It provides a seamless interface for searching flights across multiple airlines and travel services using natural language commands.

## Features
- Interactive chat-based flight search
- Automated browser interactions
- Support for multiple airlines and travel services
- Rate limiting protection
- Conversation memory for context-aware interactions

## Prerequisites
- Python 3.13 or higher
- Node.js (for MCP servers)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MehmetCelik53/MCP.git
cd MCP
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root and add your API keys:
```env
GOOGLE_API_KEY=your_google_api_key
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Enter your flight search queries in natural language:
Example queries:
- "Find flights from Istanbul to Izmir"
- "Search for flights to Izmir on August 16, 2025"
- "Show me morning flights from Istanbul to Izmir"

## Project Structure

```
├── app.py              # Main application file
├── appwait.py          # Rate-limited version of the app
├── browser_mcp.json    # MCP server configuration
├── pyproject.toml      # Project dependencies and metadata
├── .env                # Environment variables (create this)
└── README.md           # Project documentation
```

## Configuration

The `browser_mcp.json` file contains configurations for different MCP servers:
- Playwright for browser automation
- Airline-specific servers
- Search engines

## Features in Detail

### Rate Limiting Protection
The application includes built-in rate limiting protection to prevent API throttling:
- Minimum delay between requests
- Automatic retry mechanism
- Configurable delay settings

### Conversation Memory
The chat agent maintains conversation context for more natural interactions:
- Remembers previous search criteria
- Understands context-dependent queries
- Supports conversation history clearing

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository.
