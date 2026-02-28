from openai import OpenAI

client = OpenAI(api_key="API dal dena")
chunks = [
    {"start": "00:00:00", "end": "00:01:00", "text": "Hey there everyone and welcome to the section of functions in Python. Functions are nothing more than a wrapper. They wrap your code and make it reusable."},
    {"start": "00:01:00", "end": "00:02:00", "text": "Functions are known by different names like methods. The way they are defined is the same but depends on where you define them. Naming is very important."},
    {"start": "00:02:00", "end": "00:03:00", "text": "By the end of this chapter you will understand the purpose and benefit of functions. We will learn how to create reusable modular code using the def keyword."},
    {"start": "00:03:00", "end": "00:04:00", "text": "We are reducing code duplication. You are managing a busy chai stall and want to print each customer name and order. Write a function and call it multiple times."},
    {"start": "00:04:00", "end": "00:05:00", "text": "Every function starts with the def keyword. Then the function name. Parameters go inside brackets. What you accept are parameters, what you pass are arguments."},
    {"start": "00:05:00", "end": "00:06:00", "text": "Aman ordered masala chai, Hitesh ordered ginger chai, Jia ordered tulsi chai. Just by editing one place you get the change everywhere. This is the power of functions."},
]

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

print("Scoring chunks...\n")

results = []
for chunk in chunks:
    score = score_chunk(chunk)
    results.append({"start": chunk["start"], "end": chunk["end"], "score": score})
    print(f"{chunk['start']} → {chunk['end']} : score {score}")

# sort and pick top 2
results.sort(key=lambda x: x["score"], reverse=True)

print("\n--- TOP SEGMENTS ---")
for r in results[:2]:
    print(f"Start: {r['start']}  End: {r['end']}  Score: {r['score']}")