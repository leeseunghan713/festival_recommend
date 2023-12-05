# festival_recommend.py

# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from scipy.sparse import hstack
from datetime import datetime

# csv 파일 불러오기
festivals = pd.read_csv('./festivaldataset.csv', parse_dates=['축제시작일자'], encoding='cp949')

# 필요한 열만 선택하기
festivals = festivals[['축제명', '축제시작일자', '축제내용', '주관기관명', '제공기관명']]

# 현재 날짜 이후의 데이터만 선택하기
current_date = datetime.now()
future_festivals = festivals[festivals['축제시작일자'] > current_date].reset_index(drop=True)

# 결측값을 빈 값으로 대체
future_festivals['축제명'] = future_festivals['축제명'].fillna('')
future_festivals['축제시작일자'] = future_festivals['축제시작일자'].fillna('')
future_festivals['축제내용'] = future_festivals['축제내용'].fillna('')
future_festivals['주관기관명'] = future_festivals['주관기관명'].fillna('')
future_festivals['제공기관명'] = future_festivals['제공기관명'].fillna('')

# 사용자가 좋아요한 축제
liked_festivals = festivals[(festivals['축제명'] == '신년해맞이축제') | (festivals['축제명'] == '2024 해돋이 행사')]

# 축제 데이터를 텍스트로 변환
festivals_text = [';'.join([str(fest['축제명']), str(fest['축제내용']), str(fest['주관기관명']), str(fest['제공기관명']), str(fest['축제시작일자'])]) for index, fest in future_festivals.iterrows()]
liked_festivals_text = [';'.join([str(fest['축제명']), str(fest['축제내용']), str(fest['주관기관명']), str(fest['제공기관명']), str(fest['축제시작일자'])]) for index, fest in liked_festivals.iterrows()]

# TF-IDF 벡터화
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(festivals_text)

# 사용자가 좋아요한 축제에 대한 TF-IDF 벡터 가져오기
liked_festivals_tfidf = tfidf_vectorizer.transform(liked_festivals_text)  # transform 사용

# 코사인 유사도 계산
cosine_similarities = linear_kernel(liked_festivals_tfidf, tfidf_matrix).flatten()

# 유사한 축제 정렬
similar_festivals_indices = cosine_similarities.argsort()[::-1]

for i in range(len(similar_festivals_indices)):
  if(similar_festivals_indices[i] >= len(future_festivals)):
    similar_festivals_indices[i] = similar_festivals_indices[i] - len(future_festivals)

similar_festivals_indices = list(dict.fromkeys(similar_festivals_indices))

# 사용자가 좋아요한 축제에 대한 축제명 가져오기
liked_festival_names = liked_festivals['축제명'].tolist()

# 추천된 축제 출력 (이미 좋아요한 축제는 제외)
recommended_festivals = [future_festivals.iloc[i] for i in similar_festivals_indices if future_festivals.iloc[i]['축제명'] not in liked_festival_names]

for fest in recommended_festivals[:10]:
    print(fest['축제명'])