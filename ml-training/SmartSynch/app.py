import os
import sys
from pathlib import Path

# Get the absolute path of the project root
ROOT_DIR = Path(__file__).resolve().parent
sys.path.append(str(ROOT_DIR))

# Import the FastAPI app
from smartsynch.api.main import app
