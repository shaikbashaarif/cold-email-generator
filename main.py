import streamlit as st
from chains import Chain
from portifolio import Portfolio
from utils import extract_job_description

def create_streamlit_app(llm,portfolio,extract_job_description):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter the URL: ", value="https://careers.idfcfirstbank.com/in/en/job/P-100091/DevOps-Engineer")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            data = extract_job_description(url_input)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_email(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")



if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, extract_job_description)