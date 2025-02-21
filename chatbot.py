import os
import psycopg2
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import LlamaCpp

# Load Llama model
llm = LlamaCpp(model_path=r"C:\Users\admin\AppData\Local\nomic.ai\GPT4All\Llama-3.2-3B-Instruct-Q4_0.gguf")

# Database connection
try:
    conn = psycopg2.connect(
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432")
    )
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_goals (
        username TEXT,
        goal TEXT,
        weightage NUMERIC
    );
    ''')
    conn.commit()

except psycopg2.Error as e:
    print(f"Database connection error: {e}")
    exit()

memory = ConversationBufferMemory()

prompt_template = """You are a helpful goal-setting assistant. 
A user will provide you with their goals and a weightage for each goal. 
Ask clarifying questions and suggest ways to make their goals SMART 
(Specific, Measurable, Achievable, Relevant, and Time-bound). 
Provide encouragement and motivation. 
Consider the conversation history: {conversation}
"""

prompt = PromptTemplate(
    input_variables=["conversation"],
    template=prompt_template
)

chatbot = LLMChain(prompt=prompt, llm=llm, memory=memory)

def start_chat():
    print("Hello! I am your goal-setting assistant.")
    username = input("What's your name? ").strip()
    if not username:
        print("Username cannot be empty.")
        return

    goals = []
    total_weightage = 0

    while True:
        goal = input("Please enter a goal (or type 'done' to finish): ").strip()
        if goal.lower() == 'done':
            break

        if not goal:
            print("Goal cannot be empty. Please try again.")
            continue

        while True:
            try:
                weightage = float(input(f"Assign a weightage for '{goal}': "))
                if weightage <= 0 or weightage > 100:
                    print("Weightage must be between 1 and 100. Please try again.")
                    continue

                if total_weightage + weightage > 100:
                    print("Total weightage exceeds 100%. Please adjust your inputs.")
                    continue

                goals.append((goal, weightage))
                total_weightage += weightage
                break
            except ValueError:
                print("Invalid input. Please enter a numeric weightage.")

    if total_weightage != 100:
        print("The total weightage must be 100%. Please adjust your inputs.")
        return

    print("\nYour goals:")
    for goal, weightage in goals:
        print(f"- {goal}: {weightage}%")

    confirmation = input("Are these goals correct? (yes/no): ").lower().strip()
    if confirmation != 'yes':
        print("Goal setting process cancelled.")
        return

    try:
        for goal, weightage in goals:
            cursor.execute(
                "INSERT INTO user_goals (username, goal, weightage) VALUES (%s, %s, %s)",
                (username, goal, weightage)
            )
        conn.commit()
        print("Thank you! Your goals have been recorded.")

        # LLM interaction
        conversation_history = "\n".join([f"Goal: {g} (Weightage: {w}%)" for g, w in goals])
        llm_response = chatbot.invoke({"conversation": conversation_history})
        print("\nLLM Feedback on your goals:\n", llm_response)

    except psycopg2.Error as e:
        conn.rollback()
        print(f"Database error: {e}")
        print("There was an issue saving your goals. Please try again later.")

    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    start_chat()
