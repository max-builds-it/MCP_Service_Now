from fastmcp import FastMCP
import os
from dotenv import load_dotenv
from utils.config import ServerConfig, AuthType, AuthConfig, ApiKeyConfig
from utils.auth_manager import AuthManager
from tools.incident_tools import (
    create_incident, CreateIncidentParams,
    update_incident, UpdateIncidentParams,
    add_comment, AddCommentParams,
    resolve_incident, ResolveIncidentParams,
    list_incidents, ListIncidentsParams,
    get_incident_by_number, GetIncidentByNumberParams
)

load_dotenv()

SERVICENOW_INSTANCE = os.getenv("SERVICENOW_INSTANCE_URL")
SERVICENOW_API_KEY = os.getenv("SERVICENOW_API_KEY")

# Load configuration from environment variables
server_config = ServerConfig(
    instance_url=os.getenv("SERVICENOW_INSTANCE_URL"),
    auth=AuthConfig(
        type=AuthType.API_KEY,
        api_key=ApiKeyConfig(
            api_key=os.getenv("SERVICENOW_API_KEY"),
        )
    ),
    debug=True
)

auth_manager = AuthManager(server_config)
app = FastMCP("ServiceNow MCP Server")

@app.tool()
def mcp_create_incident(
    short_description: str,
    description: str = None,
    caller_id: str = None,
    category: str = None,
    subcategory: str = None,
    priority: str = None,
    impact: str = None,
    urgency: str = None,
    assigned_to: str = None,
    assignment_group: str = None
):
    """Create a new ServiceNow incident."""
    params = CreateIncidentParams(
        short_description=short_description,
        description=description,
        caller_id=caller_id,
        category=category,
        subcategory=subcategory,
        priority=priority,
        impact=impact,
        urgency=urgency,
        assigned_to=assigned_to,
        assignment_group=assignment_group
    )
    return create_incident(server_config, auth_manager, params)

@app.tool()
def mcp_update_incident(
    incident_id: str,
    short_description: str = None,
    description: str = None,
    state: str = None,
    category: str = None,
    subcategory: str = None,
    priority: str = None,
    impact: str = None,
    urgency: str = None,
    assigned_to: str = None,
    assignment_group: str = None,
    work_notes: str = None,
    close_notes: str = None,
    close_code: str = None
):
    """Update an existing ServiceNow incident."""
    params = UpdateIncidentParams(
        incident_id=incident_id,
        short_description=short_description,
        description=description,
        state=state,
        category=category,
        subcategory=subcategory,
        priority=priority,
        impact=impact,
        urgency=urgency,
        assigned_to=assigned_to,
        assignment_group=assignment_group,
        work_notes=work_notes,
        close_notes=close_notes,
        close_code=close_code
    )
    return update_incident(server_config, auth_manager, params)

@app.tool()
def mcp_add_comment(
    incident_id: str,
    comment: str,
    is_work_note: bool = False
):
    """Add a comment or work note to an incident."""
    params = AddCommentParams(
        incident_id=incident_id,
        comment=comment,
        is_work_note=is_work_note
    )
    return add_comment(server_config, auth_manager, params)

@app.tool()
def mcp_resolve_incident(
    incident_id: str,
    resolution_code: str,
    resolution_notes: str
):
    """Resolve an incident."""
    params = ResolveIncidentParams(
        incident_id=incident_id,
        resolution_code=resolution_code,
        resolution_notes=resolution_notes
    )
    return resolve_incident(server_config, auth_manager, params)

@app.tool()
def mcp_list_incidents(
    limit: int = 10,
    offset: int = 0,
    state: str = None,
    assigned_to: str = None,
    category: str = None,
    query: str = None
):
    """List ServiceNow incidents with optional filters."""
    params = ListIncidentsParams(
        limit=limit,
        offset=offset,
        state=state,
        assigned_to=assigned_to,
        category=category,
        query=query
    )
    return list_incidents(server_config, auth_manager, params)

@app.tool()
def mcp_get_incident_by_number(incident_number: str):
    """Get details of an incident by its number."""
    params = GetIncidentByNumberParams(incident_number=incident_number)
    return get_incident_by_number(server_config, auth_manager, params)

@app.tool()
def mcp_get_incident_by_date(
    start_date: str,
    end_date: str,
    limit: int = 10,
    offset: int = 0
):
    """Retrieve ServiceNow incidents created between two dates (inclusive). Dates must be in 'YYYY-MM-DD HH:MM:SS' format (UTC)."""
    params = ListIncidentsParams(
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        offset=offset
    )
    return list_incidents(server_config, auth_manager, params)
# ----------------------
# Run MCP server
# ----------------------
# if __name__ == "__main__":
#     app.run()
