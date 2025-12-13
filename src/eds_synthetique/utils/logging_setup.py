"""Configuration centralisée du logging."""

import logging
import sys


def configurer_logging(niveau: int = logging.INFO) -> None:
    """
    Configure le logging pour l'application.

    Parameters
    ----------
    niveau : int
        Niveau de logging (ex: logging.INFO, logging.DEBUG)
    """
    logging.basicConfig(
        level=niveau,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
