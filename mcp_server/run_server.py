from mcp_server.server import mcp

# Register tools BEFORE server starts
import mcp_server.tools.product_tools   
import mcp_server.tools.auth_tools     
import mcp_server.tools.access_tools    
import mcp_server.tools.log_tools       
import mcp_server.tools.approval_tools
from mcp_server.tools.log_tools import fetch_activity_logs

mcp.tool()(fetch_activity_logs)

def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()