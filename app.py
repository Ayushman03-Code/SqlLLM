from dotenv import load_dotenv
load_dotenv()  # Load environment variables

import streamlit as st
import os
import sqlite3
import openai  # Import the OpenAI package

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure your .env file has this key

# Function to load GPT-4 Turbo and provide query as response
def get_llm_response(question, prompt):
    try:
        # Combine the prompt and the question
        full_prompt = f"{prompt[0]} {question}"

        # Call the OpenAI API to get the response from GPT-4 Turbo
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "user", "content": full_prompt}
            ]
        )
        
        # Extract the text from the response
        response_text = response['choices'][0]['message']['content'].strip()
        print(f"Generated Response: {response_text}")  # Log the response for debugging
        
        # Ensure the response is a valid SQL query
        if not response_text:
            return "No SQL query generated. Please check your input."
        
        return response_text
    except Exception as e:
        return f"Error: {str(e)}"

# Function to retrieve query from the SQL database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        return rows
    except sqlite3.OperationalError as e:
        print(f"SQL Error: {str(e)}")
        return []  # Return an empty list on error
    finally:
        conn.commit()
        conn.close()

# Define your prompt template
prompt = [
    """
    You are an expert in converting English questions into SQL queries.
    The SQL Database is named STUDENT and has the following columns: NAME, CLASS, SECTION, and MARKS.
    
    Examples:
    1. Question: "How many entries of records are present?"
       SQL Command: "SELECT COUNT(*) FROM STUDENT;"
    
    2. Question: "Tell me all the students studying in the Data Science class."
       SQL Command: "SELECT * FROM STUDENT WHERE CLASS = 'Data Science';"
    
    Please provide the SQL command without any additional text or formatting.
    """
]

# Streamlit App
st.set_page_config(page_title="I can Retrieve Any SQL Query")
st.header("Database LLM")

question = st.text_input("Input:", key="input")
submit = st.button("Ask the question")

# If submit is clicked, get LLM response and execute SQL
if submit:
    response = get_llm_response(question, prompt)
    st.subheader("Generated SQL Query")
    st.write(response)  # Display the generated query for debugging
    
    # Ensure the generated SQL is valid before executing it
    if "Error" in response or not response:
        st.error("Invalid SQL query generated. Please check your input.")
    else:
        data = read_sql_query(response, "student.db")
        st.subheader("Query Result")
        
        # Display each row of the result
        if data:
            for row in data:
                st.write(row)
        else:
            st.write("No results found.")
