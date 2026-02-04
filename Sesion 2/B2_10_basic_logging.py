import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)

logger = logging.getLogger("curso-graph")

logger.info("Aplicación iniciada")
logger.warning("Esto es solo un ejemplo")