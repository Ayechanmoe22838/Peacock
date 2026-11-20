import uvicorn
import os
import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from app.core.config import settings

if __name__ == "__main__":
    port = int(os.getenv("PORT", settings.PORT))
    host = os.getenv("HOST", settings.HOST)
    env = os.getenv("ENVIRONMENT", settings.ENVIRONMENT)
    
    print("=" * 65)
    print("🌟 Starting PEACOCK – Smart Wedding Reception Management System")
    print(f"📍 Binding: http://{host}:{port}")
    print(f"🌍 Environment: {env}")
    print("🔑 Admin Account: admin@peacock.com / AdminPassword123!")
    print("💖 Customer Account: customer@peacock.com / CustomerPassword123!")
    print("=" * 65)
    
    uvicorn.run("app.main:app", host=host, port=port, reload=(env == "development"))
