"""Main entrypoint. Checks migrations are not needed and if all is OK starts uvicorn"""

import asyncio
import sys

import uvicorn

from .migrator import migrate_database
from .routes import app

if __name__ == "__main__":
    # Check that migrations have been run.
    if not asyncio.run(migrate_database(False)):
        sys.exit(1)
    else:
        watch = "watch" in sys.argv
        watch_dirs = ["query"] if watch else None
        uvicorn.run(
            app,
            port=5510,
            host="0.0.0.0",
            reload=watch,
            reload_dirs=watch_dirs,
            log_config=None,
        )
