# festival_recommend
콘텐츠 기반 추천 알고리즘

사용자가 좋아하는 축제를 "신년해맞이축제"와 "2024 해돋이 행사"라고 가정

출력 

![festival_recommend](https://github.com/leeseunghan713/festival_recommend/assets/127086663/3acb6234-bddb-4c92-b836-1714c6d6835d)

축제 데이터와 사용자가 좋아요한 축제를 축제명, 축제내용, 주관기관명, 제공기관명, 축제시작일자 를 기준으로 벡터화 
벡터화한 데이터의 코사인 유사도 계산후 유사도가 높은순으로 정렬
중복을 제거한 상위 10개의 인덱스 값을 이용해서 추천된 축제명을 출력

데이터셋 출처: https://www.data.go.kr/data/15013104/standard.do#/tab_layer_open
