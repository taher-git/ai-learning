from openai import OpenAI
import whisper

# Initialize OpenAI client
client = OpenAI()

# Step 1: Transcribe audio with Whisper (local)
model = whisper.load_model("base")   # "tiny", "small", or "base"
audio_file = "AI Agent Demo/backend/Summarization AI/data/Meeting.mp3"

print("Transcribing audio...")
result = model.transcribe(audio_file)
transcript = result["text"]

print("\nTranscript:\n", transcript[:300], "...")  # preview first 300 chars

# Step 2: Summarize transcript with GPT
print("\nSummarizing transcript with GPT...")

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful meeting summarizer."},
        {"role": "user", "content": f"Summarize the following meeting transcript into 5-7 bullet points:\n\n{transcript}"}
    ]
)

summary = resp.choices[0].message.content

print("\nSummary:\n", summary)
