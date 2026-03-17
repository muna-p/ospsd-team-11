from fastapi import FastAPI, Query

app = FastAPI(
    title="Google Calendar Service",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    """Return service health status."""
    return {"status": "ok"}


@app.get("/auth/login")
def login() -> dict[str, str]:
    """Start the OAuth login flow."""
    return {"message": "OAuth login not implemented yet"}


@app.get("/auth/callback")
def callback(code: str | None = Query(default=None)) -> dict[str, str]:
    """Handle the OAuth callback from the provider."""
    if code is None:
        return {"message": "Missing authorization code"}
    return {"message": "OAuth callback not implemented yet"}


@app.get("/events")
def list_events() -> dict[str, str]:
    """List calendar events."""
    return {"message": "List events endpoint not implemented yet"}