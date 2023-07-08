


def run():
    try:
        main()
    except Exception as e:
        logging.error("Exception", exc_info=True)
        run()
