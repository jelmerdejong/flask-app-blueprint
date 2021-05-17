## 소개
- RTL-SDR 에서 나온 라디오 신호를 텍스트로 변환, 변환된 텍스트를 gpt-2 (SKT-AI) 에 입력하고, 출력된걸 같이 출력해주는 프로그램 입니다.

## 환경
- 700khz-1.7Ghz 안테나 USB SDR + Ubuntu 노트북
- AWS EC2 (GPT-2) ,Flask docker container

## 사용한 오픈소스
- https://github.com/jelmerdejong/flask-app-blueprint (Flask)
- https://github.com/randaller/fm2txt (radio signal to Text)
- https://github.com/SKT-AI/KoGPT2 (GPT2)

## 파일 설명
- project/textapi/views.py
- - -> / - static Page (Demo page : http://3.35.236.50:8001)
- -> /textapi/add -> 
- -> /textapi/update -> gpt2/main.py 에서 predict_text 변경
- radio_receiver/listen.py
- -> RTL-SDR 기반 USB 에서 수신한 라디오 신호를 텍스트로 변환, /textapi/add 를 통해 라디오 텍스트를 등록
- gpt2/main.py
- -> textapi/list 를 호출해서 라디오 텍스트를 가져온다.
- -> `input_ids = tokenizer.encode("<라디오 텍스트 >")` 여기에 값을 집어넣으면 GPT-2 를 통한 예측한 값이 나오고
- -> /textapi/update 를 통해 예측한 값 반영

## Format
- `<라디오 소리 Text -> GPT-2 결과>`
```
아 이것도 신청곡 바로 준비했네요 이거 노래 듣고 -> 아 이것도 신청곡 바로 준비했네요 이거 노래 듣고 싶어서요. 네. 자~ 오
```
