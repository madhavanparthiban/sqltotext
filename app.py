from dotenv import load_dotenv
load_dotenv()

import streamlit as st 
import os
import sqlite3

import google.generativeai as genai

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def get_gemini_responseOld(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(prompt[0],question)
    return response.text

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    full_prompt = f"{prompt[0]} {question}"
    response = model.generate_content(full_prompt)
    return response.text

def read_sql_query(sql,db):
    conn= sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

prompt=[
    """
You are an expert in converting English question to sql query!
The SQL database has the name STUDENT and has the following columns- NAME, CLASS,
SECTION and  MARKS, \n\n For example 1- how many entries of records are present?,
the sql command will be something like this SELECT COUNT(*) FROM STUDNT;
\nExample 2- tell me all the students studying in data science class?,
the sql command will be something like this SELECT * FROM STUDENT 
where CLASS="Data Science"
also the sql code should not have ``` in beginning or end and sql word in the output
"""
]

st.set_page_config(page_title="retrieve any sql query")
st.header("Gemini App to Retrieve SQL data")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    data=read_sql_query(response,"student.db")
    st.subheader("the response is")
    for row in data:
        print(row)
        st.header(row)