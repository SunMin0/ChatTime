# Project : 💬 ChatTime
## Sub project : 🛒 ChatOrder
-----------------------------------------
## 📒Service Summary

### 저희 프로젝트는 Chatbot을 활용해서 정보제공, 추천, 쇼핑 등의 다양한 서비스를 챗봇웹으로 제공하기 위해서 만들어졌습니다.
### 구현한 프로젝트는 ChatOrder로 챗봇(인공지능)을 활용한 카페 메뉴 주문 서비스를 구현하였습니다.
### 필요한 데이터셋을 정제하고,  모델을 만들어 챗봇을 학습 시킨 후 챗봇을 활용한 서비스 
### 패쓰오더와 같이 카페메뉴를 주문할 수 있는 오더 시스템
### 챗봇을 활용하여 대화하는 기분으로 할 수 있는 사용자 친화적 서비스
### 익숙한 프론트를 사용하여 사용자가 익숙하게 사용할 수 있는 인터페이스
### 앱카드 결제까지 결제API를 활용한 결제 시스템
### ChatOrder는 시작일뿐, 확장성있어 많은 서비스를 할 수 있는 베이스
-----------------------------------------
## Notion URL
https://www.notion.so/Project-Chat-Time-7edccf0e361040fba461ecc3f7eed82a
* WBS, API 설계, Team 소개

-----------------------------------------
## 🎥 발표 영상(Youtube)
* 링크 : 
-----------------------------------------
## 📑문서

*  ELK 설정 config 파일
*  .py 파일
*  회의록
*  업무일지
*  .html 파일
*  static 정적 파일 
-----------------------------------------  

## 👨‍👨‍👦‍👦 팀 소개
|팀원|직무|
|------|---|
|김선민|Fullstack dev, AI(인공지능), Platform구축, Git master |
|양정헌|Backend dev, Frontend dev, DB설계, API 설계 |
-----------------------------------------  
## 🕹기능
* 회원가입/로그인/회원탈퇴/회원정보수정/비밀번호변경  
> a. 회원가입 기능    
> b. 로그인 기능  
> c. 소셜 로그인 기능(카카오,네이버)  
> d. 소셜 로그아웃 기능(카카오, 네이버)  
> e. 회원 탈퇴 기능   
* 프로필 변경기능  
> a. 닉네임 변경  
> b. 이메일 변경  
> c. 성별 변경  
> d. 출생 연월 변경  
* 즐겨찾기 기능  
> a. 자주 이용하는 서비스를 즐겨찾기    
* 챗봇 기능  
> a. 챗봇과의 대화 기능   
> b. 챗봇의 음료 추천 기능  
> c. 빠른 선택과 결제 기능    
> e. intent의 비교적 정확한 파악으로 소비자의 needs를 충족  
* 카페 메뉴 기능  
> a. espresso, juice, tea, bread 4가지로 구분  
> b. 메뉴를 고르고 옵션을 선택, 장바구니에 넣고 결제까지  
> c. 인기 메뉴 top3   
> e. 광고 배너 넣어서 간접광고 가능  
* 결제 기능  
> a. Iamport API를 이용한 카드 결제 기능  
> b. 결제 무결성 검증 코드로 back-front 결제 금액의 유효성 검사  
* 장바구니 기능  
> a. 챗봇을 통한 또는 직접 메뉴를 선택하고 장바구니에 add to cart 기능  
> b. 장바구니에 들어간 품목의 list 확인  
> c. Quantity 조절 기능  
* 주문 내역 보기 기능  
> a. Customer 자신의 주문 내역을 확인 가능  
> b. 점주는 Customer의 주문 내역 전체를 확인 가능  
> c. 총 매출 금액을 확인가능  
* Master 계정에 kibana 분석 제공  
> a. ELK의 활용으로 시각화된 분석 자료 제공  
> b. 분석 자료를 통해 전략 수립 가능  
* Kafka의 파이프 라인 관리 기능  
> a. 서로 다른 웹 서버의 Chat log data or Order 정보등을 Elasticsearch의 각각의 인덱스에 적재   
-----------------------------------------  
### 🛠Skill & Tools
![Skill_Tools](https://user-images.githubusercontent.com/97014086/172040253-9c1ea521-ed1c-40b8-bbae-50343e18ff50.png)

#### Backend
* Django  
* Python    

#### DB  
* MySQL  

#### Restful API
* Kakao Social Log-in API
* Naver Social Log-in API
* Google Map API

#### Frontend  
* HTML  
* CSS  
* Javascript

#### ML,DL
* Jupyter notebook
* Pytorch
* Tensorflow

#### Platforms  
* ElasticSearch
* Logstash
* Kibana
* Kafka

#### CI/CD
* Jenkins


-----------------------------------------
### 💴API 설계도
![API설계](https://user-images.githubusercontent.com/97925049/166633588-9c109dbc-7d1b-412b-a196-897017f3dcf2.png)
* 개발하면서 수정 예정
#### API 설계도에 따른 진행 상황
# 노션으로 체크박스 관리
* 회의록, API, WBS
> https://www.notion.so/API-c120523cd89b41a88107ce7579a8165e
* 업무일지, 해결일지
> https://www.notion.so/Project-Chat-Time-3eacf18eb2fc4865baea5c9c1e15220b
* 서비스 후 피드백 보완
> [https://nebulous-class-691.notion.site/1e40e33b7e014cc595060d2242793322?v=59c6c0257859477b957e424585cb7992](https://nebulous-class-691.notion.site/Start-9dbc2e6ce5114635a35df944b7bf1591)
-----------------------------------------

## 🎊산출물
> ERD, 프로세스정의 및 UI 설계 , WBS, 플랫폼 구성도
### 🖌 ER Diagram(ERD)
![ERD](https://user-images.githubusercontent.com/97014086/172041171-76737639-8fbd-4221-9fdd-0fd05e3ff84c.png)

https://github.com/SunMin0/ChatTime/issues/8#issue-1260987993

-----------------------------------------
### 🎨플랫폼 구성도

![pipeline0511](https://user-images.githubusercontent.com/97014086/167773819-690f8962-d7a0-4918-8527-1631c8639c2a.png)
-----------------------------------------
### 🖊프로세스정의
-----------------------------------------
### 🖥UI 설계

<img src="https://user-images.githubusercontent.com/97925049/166646657-146ab7b5-3ec5-4d11-ae4e-7d73b02ea672.png" width="450" height="650"/>

![통합본100퍼](https://user-images.githubusercontent.com/97014086/167525353-8cb7a6ec-181e-4588-a2b1-9fb4af35492f.png)

-----------------------------------------
### 📅 WBS
* notion으로 협업하면서 WBS 작성
> https://www.notion.so/WBS-Work-Broken-Structure-de61224f0d0b40b6ae4d800eafdfb0d2
![WBS](https://user-images.githubusercontent.com/97925049/168591525-677bc408-4363-48f2-a634-5fd36908df62.png)
-----------------------------------------

### 🎞구현
-----------------------------------------



## ✏참고

* 패쓰오더
* 카카오톡
* 쇼핑몰
