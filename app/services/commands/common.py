import logging


def setup_logger(app):
    debug = app.config.get("DEBUG")
    app.logger.setLevel(logging.DEBUG if debug else logging.INFO)
    logging.getLogger().setLevel(logging.DEBUG if debug else logging.INFO)