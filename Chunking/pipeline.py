from openai import OpenAI

client = OpenAI(api_key="API dal dena")
def parse_srt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = content.strip().split("\n\n")
    subtitles = []

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        timestamp = lines[1]
        text = " ".join(lines[2:])
        start = timestamp.split(" --> ")[0].strip().replace(",", ".")
        subtitles.append({"start": start, "text": text})

    return subtitles


def group_into_chunks(subtitles, chunk_seconds=60):
    chunks = []
    current_text = []
    current_start = subtitles[0]["start"]

    def time_to_seconds(t):
        h, m, s = t.split(":")
        return int(h) * 3600 + int(m) * 60 + float(s)

    start_time = time_to_seconds(current_start)

    for sub in subtitles:
        current_time = time_to_seconds(sub["start"])

        if current_time - start_time >= chunk_seconds:
            chunks.append({
                "start": current_start,
                "end": sub["start"],
                "text": " ".join(current_text)
            })
            current_start = sub["start"]
            start_time = current_time
            current_text = []

        current_text.append(sub["text"])

    if current_text:
        chunks.append({
            "start": current_start,
            "end": subtitles[-1]["start"],
            "text": " ".join(current_text)
        })

    return chunks


def score_chunk(chunk):
    prompt = f"""
You are a social media virality expert. Score the following transcript chunk out of 10 based on:
- How engaging or exciting it is
- Whether it could hook a viewer in the first 3 seconds
- Viral potential for short video reels

Respond with ONLY a number between 1 and 10. Nothing else.

Transcript: {chunk['text']}
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    score = float(response.choices[0].message.content.strip())
    return score


# --- MAIN ---
print("Reading transcript...\n")
subtitles = parse_srt("transcript.srt")
chunks = group_into_chunks(subtitles, chunk_seconds=60)

print(f"Found {len(chunks)} chunks. Scoring...\n")

results = []
for chunk in chunks:
    score = score_chunk(chunk)
    results.append({"start": chunk["start"], "end": chunk["end"], "score": score})
    print(f"{chunk['start']} → {chunk['end']} : score {score}")

results.sort(key=lambda x: x["score"], reverse=True)

print("\n--- TOP SEGMENTS TO CONVERT INTO REELS ---")
for r in results[:3]:
    print(f"Start: {r['start']}  End: {r['end']}  Score: {r['score']}")