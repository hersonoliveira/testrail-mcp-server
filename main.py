import logging
from dotenv import load_dotenv

from mcp_testrail.mcp_server import TestRailMCPServer
from mcp_testrail.utils import get_env_var

logger = logging.getLogger("mcp-testrail")

load_dotenv()


def main():
    # Move these somewhere else?
    tr_url = get_env_var("TESTRAIL_URL")
    tr_username = get_env_var("TESTRAIL_USERNAME")
    tr_password = get_env_var("TESTRAIL_API_KEY")

    mcp = TestRailMCPServer(tr_url, tr_username, tr_password)
    mcp.run()


if __name__ == "__main__":
    main()
