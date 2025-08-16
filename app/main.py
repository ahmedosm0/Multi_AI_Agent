import subprocess
import threading
import time
from dotenv import load_dotenv

from app.common.logger import get_logger
from app.common.custom_exception import CustomException

load_dotenv()

logger = get_logger(__name__)

def run_backend():
    try:
        logger.info('Conencting to Backend')
        subprocess.run(['uvicorn','app.backend.api:app', '--host', '127.0.0.1', '--port', '9999'], check = True)
        
    except CustomException as e:
        logger.error('Problem with Backend Service')
        raise CustomException(f"Failed to start backend", e)

def run_frontend():
    try:
        logger.info("Connecting to Frontend")
        subprocess.run(['streamlit', 'run', 'frontend/ui.py'], check = True)
    except CustomException as e:
        logger.error("Problem with Frontend")
        raise CustomException("Failed to start Frontend", e)

if __name__ == '__main__':
    try:
        threading.Thread(target= run_backend).start()
        time.sleep(2)
        run_frontend()
    except CustomException as e:
        logger.exception(f'CustomException occured: {str(e)}')