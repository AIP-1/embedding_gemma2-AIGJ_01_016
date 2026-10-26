# 7단계 도메인 미세 조정 (README 요약)

- 작업 폴더: `~/jetson-aip-LLM` (README는 `~/eg2-lab` 기준이지만 이 젯슨은 여기서 실습)
- 데이터: `data/train.jsonl` 282쌍, `data/eval.jsonl` 60쌍 (README상 제공)
- 스크립트: `eval_ir.py` (학습 전후 평가), `train_ft.py` (MatryoshkaLoss+MNRL, 3 epoch, batch 8, accum 2, lr 2e-5, bf16, gradient checkpointing 직접 켬)
- 순서: datasets 설치(`-c ~/eg2/torch-pin.txt`) → 줄 수 확인 → 기준 평가 → `nohup python train_ft.py > train.log 2>&1 &` → `tail -f train.log` → `python eval_ir.py models/eg2-classroom`
- OOM이면 batch 4, accum 4. 점수가 떨어지면 epoch 1~2 또는 lr 1e-5.

## 결과

| 모델 | accuracy@1 | accuracy@3 | ndcg@10 | 학습 시간 |
| --- | --- | --- | --- | --- |
| 기준 (google/embeddinggemma-2) | 0.867 | 1.0 | 0.946 | - |
| 미세 조정 (eg2-classroom) | 0.9 | 1.0 | 0.959 | 874.5초 (약 14.6분) |

## 학습 기록 (train.log)

- 54 step (3 epoch), loss 2.087 → 1.107 → 0.603 → 0.536 → 0.593, train_loss 평균 0.945
- epoch마다 평가: accuracy@1 0.9, accuracy@3 1.0, ndcg@10 0.9587, mrr@10 0.9444 (epoch 1~3 동일)
- OOM 없이 batch 8로 완료

## 결론

- 평가 60문제 중 1위 정답이 52개 → 54개로 늘었다 (accuracy@1 0.867 → 0.9). 3위 안 정답은 학습 전후 모두 100%.
- 기준 모델이 이미 높아서 오른 폭은 작다. epoch 1 이후 점수가 그대로라 1 epoch만 학습해도 비슷했을 것으로 보인다.
- 데이터는 README 설명(문서 94개·질문 282개 / 평가 문서 20개·질문 60개, 겹침 없음)에 맞춰 새로 작성한 것(`make_step7.py`).
- `eval_ir.py` 실행 시 `sentence_transformers.evaluation` DeprecationWarning이 나오지만 결과에는 영향 없음.

## 일반 질의 확인 (3단계 test_text.py, 질의 2개)

| 차원 | 기준 모델 | 미세 조정 모델 |
| --- | --- | --- |
| 768 | 둘 다 정답 1위 (0.717 / 0.725), 250 ms | 둘 다 정답 1위 (0.518 / 0.615), 260 ms |
| 256 | 둘 다 정답 1위 (0.734 / 0.754), 185 ms | 둘 다 정답 1위 (0.548 / 0.652), 183 ms |
| 128 | 둘 다 정답 1위 (0.785 / 0.810), 182 ms | "졸리고 머리가 맑지 않아요" → 조도 문장으로 틀림 (0.564), 냉방은 정답 (0.677), 178 ms |

- 유사도 숫자 자체가 낮아진 건 학습 방식(MNRL) 때문에 점수 분포가 바뀐 것이라 순위가 더 중요하다.
- 128차원에서 1개가 틀렸다. README 확인 포인트대로 epoch를 1로 줄여 다시 학습해 볼 수 있다 (epoch 1 이후 평가 점수가 그대로였음).
- 미세 조정 모델 비교는 복사본 `eg2_ft.py`, `test_text_ft.py`로 했고 원래 `eg2.py`는 그대로다.
