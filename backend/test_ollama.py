from app.analyzer import analyze_code


sample_code = """
def divide(a, b):
    return a / b
"""


def main():
    review = analyze_code(sample_code)

    print(review.model_dump_json(indent=2))


if __name__ == "__main__":
    main()