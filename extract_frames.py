import av

container = av.open("media/raw.avi")
stream = container.streams.video[0]
count = 0
for i, frame in enumerate(container.decode(stream)):
    if i % 60 == 0:  # 30fps 기준 2초마다 1장
        count += 1
        frame.to_image().save(f"media/frame_{count:02d}.jpg")
print(f"사진 {count}장 저장 완료")
