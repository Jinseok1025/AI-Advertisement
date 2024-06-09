import streamlit as st
import requests
import pandas as pd

st.title('광고 문구 서비스앱')
generate_ad_url = 'http://127.0.0.1:8000/create_ad'
get_ads_url = 'http://127.0.0.1:8000/ads'

product_name = st.text_input('제품 이름')
details = st.text_input('주요 내용')
options = st.multiselect('광고 문구의 느낌', options=['기본', '재밌게', '차분하게', '과장스럽게', '참신하게', '고급스럽게'], default=['기본'])

if st.button("광고 문구 생성하기"):
    try:
        response = requests.post(
            generate_ad_url,
            json={"product_name": product_name,
                  "details": details,
                  "tone_and_manner": ", ".join(options)})
        if response.status_code == 200:
            ad = response.json()['ad']
            st.success(ad)
        else:
            st.error(f"에러: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"연결 실패! 에러: {str(e)}")

if st.button("저장된 광고 문구 보기"):
    try:
        response = requests.get(get_ads_url)
        if response.status_code == 200:
            ads = response.json()['ads']
            if ads:
                df = pd.DataFrame(ads)
                st.dataframe(df)
            else:
                st.warning("저장된 광고 문구가 없습니다.")
        else:
            st.error(f"에러: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"연결 실패! 에러: {str(e)}")
