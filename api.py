import openai
openai.api_key = "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"



prompt = input("please enter a question")

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
