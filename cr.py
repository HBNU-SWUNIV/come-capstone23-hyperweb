import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd

async def get_article_body(session, idxno):
    base_url = "https://www.k-health.com/news/articleView.html?idxno="
    url = base_url + str(idxno)

    async with session.get(url) as response:
        if response.status == 200:
            soup = BeautifulSoup(await response.text(), 'html.parser')

            article_head_title = soup.find("div", {"class": "article-head-title"})
            article_body = soup.find("div", {"id": "article-view-content-div"})

            if article_head_title and "반려동물 건강이야기" in article_head_title.text:
                if article_body:
                    p_tags = article_body.find_all('p')
                    p_texts = [p.text.strip() for p in p_tags]
                    p_texts_string = "\n".join(p_texts)
                    save_to_excel(idxno, p_texts_string)
                    return "저장되었습니다."
                else:
                    return "해당 클래스를 찾을 수 없습니다."
            else:
                return "반려동물 건강이야기가 포함된 기사가 아닙니다."
        else:
            return f"HTTP 오류: {response.status}"

def save_to_excel(idx, text):
    file_name = 'articles.xlsx'
    
    try:
        # 기존 엑셀 파일을 읽어옴
        df = pd.read_excel(file_name, engine='openpyxl')
    except FileNotFoundError:
        # 파일이 없으면 새로운 데이터프레임 생성
        df = pd.DataFrame(columns=['idxno', 'content'])
        
    # 새로운 행 추가
    new_row = pd.DataFrame({'idxno': [idx], 'content': [text]})
    df = pd.concat([df, new_row], ignore_index=True)
    
    # 엑셀 파일로 저장
    df.to_excel(file_name, index=False, engine='openpyxl')


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for idxno in range(64000, 65000):
            tasks.append(asyncio.ensure_future(get_article_body(session, idxno)))
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())
    
 