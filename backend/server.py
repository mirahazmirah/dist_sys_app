import uvicorn
import os

if __name__ == "__main__":
    # Get port from environment or use default 8000
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("0.0.0.0", "127.0.0.1")
    
    print(f"🚀 Starting Campus Ride Backend Server on http://{host}:{port}")
    
    # Run the uvicorn server pointing to the FastAPI app in app/main.py
    uvicorn.run(
        "app.main:app", 
        host=host, 
        port=port, 
        reload=True,
        log_level="info"
    )
