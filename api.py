openapi.api_key = "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"

prompt = "Hello, how can I help you today?"
model = "text-davinci-002" # Or any other model you want to use
response = openai.Completion.create(
    engine=model,
    prompt=prompt,
    max_tokens=100,
    n=1,
    stop=None,
    temperature=0.5,
)

print(response.choices[0].text)