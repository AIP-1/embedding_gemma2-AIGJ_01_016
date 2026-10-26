import glob
from eg2 import load
model = load(audio=True)
files = sorted(f for f in glob.glob("media/*.wav") if "/raw_" not in f)
aud = model.encode([{"audio": f} for f in files], normalize_embeddings=True)
queries = ["덥다고 냉방을 요청하는 목소리", "날카로운 경보음", "웅웅거리는 배경 소음", "사람이 말하는 소리"]
q = model.encode(queries, prompt_name="SearchQuery", normalize_embeddings=True)
print(" " * 24, "  ".join(f.split('/')[-1][:-4].rjust(6) for f in files))
for qi, row in zip(queries, q @ aud.T):
    print(qi[:20].ljust(22), "  ".join(f"{s:6.3f}" for s in row))
