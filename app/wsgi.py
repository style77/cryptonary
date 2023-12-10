import logging
from app.lifetime import create_app

app = create_app()

debug = app.config.get("DEBUG")
app.logger.setLevel(logging.DEBUG if debug else logging.INFO)
logging.getLogger().setLevel(logging.DEBUG if debug else logging.INFO)