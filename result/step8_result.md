# 8단계 웹캠 실시간 물체 추출과 웹 검색

측정일: 2026-10-26 · 장비: Jetson Orin Nano Super 8GB · 웹캠 Logitech C920 (`/dev/video0`)

- 작업 폴더: `~/jetson-aip-LLM` (README는 `~/eg2-lab` 기준)
- 코드: `app.py` 하나, `--mode yolo | relabel | yoloe`
- 순서: 설치 → 웹캠 확인 → 8-1 yolo (문제 확인) → 8-2 relabel (개선 1) → 8-3 yoloe (개선 2) → 8-4 표 정리
- `LABELS`에 `("pen", "볼펜")`, `("toothbrush", "칫솔")`을 추가함 (8-2부터 적용)

## 8-4 결과 비교

| 물체 | yolo 라벨 | relabel 라벨 (점수) | yoloe 라벨 | 비고 |
| --- | --- | --- | --- | --- |
| 노트북 | laptop 0.96 | laptop 0.95 | laptop 0.92 | 세 모드 모두 정답 |
| 휴대폰 | cell phone 0.89 | cell phone 0.71 | cell phone 0.75 | 세 모드 모두 정답 |
| 드럼 세탁기 (노트북 화면 사진) | microwave 0.82 (오인식) | washing machine 0.73 (정답) | drum washing machine 0.79 (정답) |  |
| 건전지 | cell phone 0.8 (오인식) | AA battery 0.751 (정답) | AA battery 0.45 (정답) | yoloe는 신뢰도 낮음 |
| 텀블러 | - | water bottle 0.645 | cup 0.32 | LABELS에 tumbler 없음, 둘 다 근접한 답 |
| 볼펜 | toothbrush 0.64 (오인식) | 미검출 (박스 없음) | pen 0.69 (정답) | relabel의 한계를 yoloe가 해결 |
| 마우스 | mouse 0.97 | - | - | 8-1에서만 확인 |
| 키보드 | keyboard 0.9 | - | - | 8-1에서만 확인 |
| 가방 | backpack 0.72 | - | - | 8-1에서만 확인 |

- relabel 열의 숫자는 크롭 임베딩과 라벨 문구의 유사도, yolo·yoloe 열의 숫자는 검출 신뢰도라서 서로 직접 비교하지 않는다.

| 모드 | 검출 fps | 임베딩 ms/개 | RAM (MB, tegrastats) |
| --- | --- | --- | --- |
| yolo | 13.1 | 852 | 측정 안 함 |
| relabel | 12.0 | 837 | 측정 안 함 |
| yoloe | 12.2 | 838 | 측정 안 함 |

## 정리

- **yolo**: COCO 물체(노트북·휴대폰·마우스 등)는 정확하지만, 80종 밖의 물체는 모양이 비슷한 클래스로 틀린다 (세탁기 → microwave, 건전지 → cell phone, 볼펜 → toothbrush).
- **relabel**: 박스가 잡힌 물체의 라벨은 바로잡는다 (세탁기·건전지). 하지만 박스가 안 잡히면 고칠 수 없다 (볼펜 미검출).
- **yoloe**: 6개 물체를 모두 맞게 찾았고, relabel에서 놓친 볼펜도 검출했다. 건전지처럼 작은 물체는 신뢰도가 0.45로 낮다.
- **속도**: 세 모드 모두 12~13 fps, 임베딩 약 840 ms/개로 거의 같다. README는 yoloe가 느려질 수 있다고 했지만 이 젯슨에서는 차이가 없었다.
- **강의실 서비스 추천**: yoloe. 속도 손해 없이 목록에 넣은 물체를 박스부터 직접 찾아서 정확도가 가장 높다. 새 물체는 `LABELS`에 영문 이름만 추가하면 된다.

## 메모

- 영상 접속: VS Code 포트 연결(`localhost:8000`)은 약 8초 지연 → `http://172.25.230.248:8000` 직접 접속으로 해결
- `'half' is deprecated` 경고가 프레임마다 나옴: `python -u app.py ... 2>&1 | grep --line-buffered -v "half' is deprecated"`로 숨김. 단 첫 실행(다운로드 중)에는 진행 막대가 가려지니 grep 없이 실행
- 자동 설치: 첫 yolo 실행 때 `lap`, 첫 yoloe 실행 때 `clip`. 설치 후 "다시 실행" 안내가 나오면 Ctrl+C 후 재실행. torch 2.14.1+cu132, CUDA True 유지 확인
- 웹캠 MJPG 지원 확인 (640x480 이상)
