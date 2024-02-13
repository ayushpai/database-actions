from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com", "https://3146-2610-148-1f00-4000-6dab-cde2-6cad-71bd.ngrok-free.app"],  # Update your ngrok URL here
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)


@app.post('/api/news')
async def get_news(request: Request):
    try:
        body = await request.json()

        api_key = "38fa723a3fb643a89a45cd6220b5a15d"
        if not api_key:
            raise HTTPException(status_code=500, detail="NEWS_API_KEY not found in environment variables")

        query = body.get('query', 'superbowl')
        page_size = int(body.get('pageSize', 20))
        language = body.get('language', 'en')

        url = "https://newsapi.org/v2/everything"
        params = {'q': query, 'pageSize': page_size, 'language': language, 'apiKey': api_key}

        response = requests.get(url, params=params)
        if response.status_code != 200:
            return JSONResponse(status_code=response.status_code, content=response.json())

        return response.json()

    except Exception as e:
        return {'error': str(e)}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=4000)
