import logging

def setup_logger():
    # Main application logger
    main_logger = logging.getLogger("TableRollerApp.Main")
    main_logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    main_logger.addHandler(handler)

    # Models logger
    models_logger = logging.getLogger("TableRollerApp.Models")
    models_logger.setLevel(logging.DEBUG)
    models_logger.addHandler(handler)

    #FileHandler logger
    fhandler_logger = logging.getLogger("TableRollerApp.FileHandler")
    fhandler_logger.setLevel(logging.DEBUG)
    fhandler_logger.addHandler(handler)

    return main_logger, models_logger, fhandler_logger