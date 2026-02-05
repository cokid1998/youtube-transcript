from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

app = FastAPI(title="YouTube Transcript API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "YouTube Transcript API is running"}

@app.get("/transcript")
def get_transcript(id: str):
    try:
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(id, languages=['ko', 'en'])
        transcript_list = fetched_transcript.to_raw_data()
        full_text = " ".join([item['text'] for item in transcript_list])
        
        return {
            "video_id": id,
            "transcript": transcript_list,
            "full_text": full_text
        }
        
    except TranscriptsDisabled:
        raise HTTPException(status_code=404, detail="이 비디오는 자막이 비활성화되어 있습니다.")
    except NoTranscriptFound:
        raise HTTPException(status_code=404, detail="자막을 찾을 수 없습니다.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")

# 로컬 실행용 (Vercel은 이 부분을 무시함)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)