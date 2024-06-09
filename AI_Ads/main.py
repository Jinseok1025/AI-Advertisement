import openai
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel

openai.api_key = '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'

app = FastAPI()

# MongoDB Atlas 연결 설정
client = MongoClient("mongodb+srv://wlstjr201025:QHfsSwjJqf60MI13@cluster0.xuwz7y3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.advertisement
ad_collection = db.ad_word

class AdGenerator:
    def __init__(self, engine='gpt-3.5-turbo'):
        self.engine = engine

    def using_engine(self, prompt):
        response = openai.ChatCompletion.create(
            model=self.engine,
            messages=[
                {"role": "system", "content": "assistant는 마케팅 문구 작성 도우미로 동작한다. user의 내용을 참고하여 마케팅 문구를 작성해라"},
                {"role": "user", "content": prompt}
            ]
        )
        result = response['choices'][0]['message']['content'].strip()
        return result

    def generate(self, product_name, details, tone_and_manner):
        prompt = f'제품 이름: {product_name}\n주요 내용: {details}\n광고 문구의 스타일: {tone_and_manner} 위 내용을 참고하여 마케팅 문구를 만들어라'
        result = self.using_engine(prompt=prompt)
        return result

class Product(BaseModel):
    product_name: str
    details: str
    tone_and_manner: str

@app.post('/create_ad')
async def create_ad(product: Product):
    ad_generator = AdGenerator()
    try:
        ad = ad_generator.generate(product_name=product.product_name,
                                   details=product.details,
                                   tone_and_manner=product.tone_and_manner)
        # MongoDB에 저장
        ad_collection.insert_one({
            "product_name": product.product_name,
            "details": product.details,
            "tone_and_manner": product.tone_and_manner,
            "ad": ad
        })
        return {'ad': ad}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/ads')
async def get_ads():
    ads = []
    try:
        for ad in ad_collection.find({}, {'_id': 0}):
            ads.append(ad)
        return {'ads': ads}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
