## 소개
- RTL-SDR 에서 나온 라디오 신호를 텍스트로 변환, 변환된 텍스트를 gpt-2 (SKT-AI) 에 입력하고, 출력된걸 같이 출력해주는 웹 어플리케이션 입니다.
- Demo : http://3.35.236.50:8001


## 환경
- 700khz-1.7Ghz 안테나 USB SDR + Ubuntu 노트북
- AWS EC2 (GPT-2) ,Flask docker container
- <img width="410" alt="image" src="https://user-images.githubusercontent.com/3627483/118436225-66b3ee00-b71b-11eb-9bd0-b08b29009d3a.png">
<img width="387" alt="image" src="https://user-images.githubusercontent.com/3627483/118436233-6c113880-b71b-11eb-9224-c6ca2e31a9a6.png">
<img width="390" alt="image" src="https://user-images.githubusercontent.com/3627483/118436243-716e8300-b71b-11eb-8df8-13e502c67109.png">
<img width="387" alt="image" src="https://user-images.githubusercontent.com/3627483/118436250-759aa080-b71b-11eb-9eaa-9ab3a5c6efd0.png">


## 사용한 오픈소스
- https://github.com/jelmerdejong/flask-app-blueprint (Flask)
- https://github.com/randaller/fm2txt (radio signal to Text)
- https://github.com/SKT-AI/KoGPT2 (GPT2)

## API
- project/textapi/views.py
- - -> / - static Page 
- -> /textapi/add -> 
- -> /textapi/update -> gpt2/main.py 에서 predict_text 변경

## Radio signal to text
- radio_receiver/listen.py
- -> RTL-SDR 기반 USB 에서 수신한 라디오 신호를 텍스트로 변환, /textapi/add 를 통해 라디오 텍스트를 등록

## GPT2
- gpt2/main.py
- -> textapi/list 를 호출해서 라디오 텍스트를 가져온다.
- -> `input_ids = tokenizer.encode("<라디오 텍스트 >")` 여기에 값을 집어넣으면 GPT-2 를 통한 예측한 값이 나오고
- -> /textapi/update 를 통해 예측한 값 반영



## Format
- `<라디오 소리 Text -> GPT-2 결과>`
```
Example)
아 이것도 신청곡 바로 준비했네요 이거 노래 듣고 -> 아 이것도 신청곡 바로 준비했네요 이거 노래 듣고 싶어서요. 네. 자~ 오
```
