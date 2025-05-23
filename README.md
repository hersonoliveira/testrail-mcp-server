# TestRail MCP Server

This project is an MCP (Model Context Protocol) server that provides tools and resources for interacting with the TestRail API.

## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:hersonoliveira/testrail-mcp-server.git
   ```
2. Navigate to the project directory:
   ```bash
   cd testrail-mcp-server
   ```
3. Install dependencies using uv:
   ```bash
   uv sync
   ```

## Configuration

The server requires a configuration file with your TestRail instance details and API key. Create a file named `.env` in the project root with the following content:

```
TESTRAIL_URL=http://example.testrail.io
TESTRAIL_USERNAME=test@example.com
TESTRAIL_API_KEY=your_testrail_api_key
```

## Running the Server

To start the MCP server, run the following command:

```bash
uv run main.py
```

The server will start and be available for connection by MCP clients.

## Adding to Cline

Add the following configuration to cline MCP settings json:

```json
{
  "mcpServers": {
    "testrail": {
      "command": "python",
      "args": [
        "/absolute/path/to/testrail-mcp-server/main.py"
      ],
      "env": {
        "TESTRAIL_URL": "http://example.testrail.io",
        "TESTRAIL_USERNAME": "test@example.com",
        "TESTRAIL_API_KEY": "your_testrail_api_key"
      }
    }
  }
}
```

This way the server doesn't need to be started, Cline handles that.

## Available Tools

This MCP server provides a set of tools for interacting with the TestRail API, including:

- Getting projects, suites, cases, runs, and results.
- Adding, updating, and deleting projects, suites, cases, runs, and results.
- Managing milestones and plans.
- Adding and deleting attachments.
- Getting users and custom fields.

Refer to the tool definitions provided by the MCP server for detailed information on available tools and their parameters.

## Contributing

Contributions are welcome! Please see the [LICENSE](LICENSE) file for details.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
