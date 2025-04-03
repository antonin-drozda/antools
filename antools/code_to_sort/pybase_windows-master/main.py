import app_settings as sett
import app_constants as cs
from app_code.antools.base._logger import get_logger

if __name__ == "__main__":
    log = get_logger()
    log.info("Dummy message")
    log.finish()
