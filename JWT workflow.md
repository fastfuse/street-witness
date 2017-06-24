# JWT Authorization workflow

Endpoints:

* /auth/register
* /auth/login
* /auth/logout

Request:

    POST /auth/register
    HEADERS: content-type: application/json
    BODY: {"username":"user1","password":"user1"}

Response:

    {
        "auth_token": "<auth_token>",
        "message": "Successfully registered.",
        "status": "Success"
    }


Request:

    POST /auth/login
    HEADERS: content-type: application/json
    BODY: {"username":"user1","password":"user1"}

Response:

    {
        "auth_token": "<auth_token>",
        "message": "Successfully logged in.",
        "status": "Success"
    }


Request:

    GET /api/incidents/
    HEADERS: content-type: application/json, Authorization: "Bearer <auth_token>"

Response:

    {
        count: <count>,
        incidents: [...]
    }


Request:

    POST /auth/logout
    HEADERS: content-type: application/json, Authorization: "Bearer <auth_token>"

Response:

    {
        "message": "Successfully logged out.",
        "status": "Success"
    }
