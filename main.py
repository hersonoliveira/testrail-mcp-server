import logging
from dotenv import load_dotenv

from mcp_testrail.mcp_server import create_server
from mcp_testrail.utils import get_env_var

logger = logging.getLogger("mcp-testrail")

load_dotenv()


def main():
    # Move these somewhere else?
    tr_url = get_env_var("TESTRAIL_URL")
    tr_username = get_env_var("TESTRAIL_USERNAME")
    tr_apikey = get_env_var("TESTRAIL_API_KEY")

    if not all([tr_url, tr_username, tr_apikey]):
        raise ValueError(
            "Missing required environment variables: TESTRAIL_URL, TESTRAIL_USERNAME, TESTRAIL_API_KEY"
        )

    mcp = create_server(tr_url, tr_username, tr_apikey)
    mcp.run()


if __name__ == "__main__":
    main()
