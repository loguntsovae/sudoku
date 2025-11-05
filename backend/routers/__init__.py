from .games import router as games_router
from .puzzles import router as puzzles_router
from .auth import router as auth_router
from .websocket_routes import websocket_game_endpoint

__all__ = ["games_router", "puzzles_router", "auth_router", "websocket_game_endpoint"]
