import logging

from app.lifetime import create_app


def main():
    app = create_app()

    debug = app.config.get("DEBUG")
    app.logger.setLevel(logging.DEBUG if debug else logging.INFO)
    logging.getLogger().setLevel(logging.DEBUG if debug else logging.INFO)

    app.run(host=app.config.get("HOST"),
            port=app.config.get("PORT"),
            debug=debug)


if __name__ == "__main__":
    main()
