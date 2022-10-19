from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from api import RecommendTense

class RequestInput(BaseModel):
    text: str
    feature: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/recommend_tense_v1")
def translate(request_sentence: RequestInput):
    text, standard_answer = request_sentence.text.split("$")
    print(f"Recommend tense v1: {text}\Standard answer: {standard_answer}")
    feature = request_sentence.feature
    if feature == 'recommend_tense_v1':
        recommend_sentence = RecommendTense()
        recommend = recommend_sentence(standard_answer, text)
        print(f"Result recommend: {recommend}")
        return {
            'IsSuccessed': True,
            'Message': 'Success',
            'ResultObj': {
                'src': text,
                'result': recommend
            }
        }
    else:
        return {
            'IsSuccessed': False,
            'Message': 'Fail',
            'ResultObj': {
                'src': text,
                'result': ""
            }
        }