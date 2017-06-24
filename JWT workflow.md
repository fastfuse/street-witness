# JWT Authorization workflow

Endpoints:

* /api/register
* /api/login
* /api/logout

Request:

    POST /api/register
    HEADERS: content-type: application/json
    BODY: {"username":"user1","password":"user1"}

Response:

    {
        "auth_token": "<auth_token>",
        "message": "Successfully registered.",
        "status": "Success"
    }


Request:

    POST /api/login
    HEADERS: content-type: application/json
    BODY: {"username":"user1","password":"user1"}

Response:

    {
        "auth_token": "<auth_token>",
        "message": "Successfully logged in.",
        "status": "Success"
    }


Request:

    GET /api/incidents
    HEADERS: content-type: application/json, Authorization: "Bearer <auth_token>"

Response:

    {
        count: <count>,
        incidents: [...]
    }


Request:

    POST /api/logout
    HEADERS: content-type: application/json, Authorization: "Bearer <auth_token>"

Response:

    {
        "message": "Successfully logged out.",
        "status": "Success"
    }
