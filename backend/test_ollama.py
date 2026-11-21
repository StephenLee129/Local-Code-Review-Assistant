import ollama


def main():
    response = ollama.chat(
        model="qwen2.5-coder:7b",
        messages=[
            {
                "role": "user",
                "content": "Explain what a Python decorator is in two sentences."
            }
        ]
    )

    print(response.message.content)


if __name__ == "__main__":
    main()