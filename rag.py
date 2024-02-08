from pipeline import build_pipeline


def qa_func(question):
    answer = query_engine.query(question)
    return answer

def main():
    print("Welcome to the Q&A terminal. Type 'exit' to end.")

    while True:
        user_input = input("Your Question :")

        if user_input.lower() == 'exit':
            print("Exiting the Q&A terminal. Goodbye!")
            break

        else:
            answer = qa_func(user_input)
            answer = str(answer) + " Thank You!"
            print(f"Answer: {answer}")
            
if __name__ == "__main__":
    # Build the index
    query_engine = build_pipeline()
    main()
