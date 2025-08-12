from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    import uvicorn
    from app.config import settings

    uvicorn.run("app.main:app", host=settings.app_host, port=settings.app_port, reload=settings.reload, workers=1)
