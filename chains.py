import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()



class Chain:
    def __init__(self):
        self.llm = ChatGroq(
        temperature=0,
        groq_api_key = os.getenv("GROQ_API_KEY"),
        model_name = "llama-3.3-70b-versatile"
    )
    
    def extract_jobs(self,cleaned_text):
        prompt_extract = PromptTemplate.from_template(
        """ 
        ### Scraped Text from website
        {content}
        ### Instruction:
        The scraped text is from a job Notification of a webpage,
        your job is to extract the job posting and return them in json format containing the following fields:
        'role', 'experience', 'skills', and 'description'.
        Only return the valid JSON
        ### Valid JOSN (No Preamble):
        """
        )


        chain_extract = prompt_extract | self.llm

        res = chain_extract.invoke({"content": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException as e:
            raise OutputParserException("content too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]
    
    def write_email(self, job, links):
        prompt_email = PromptTemplate.from_template(
        """ 
        ### JOB DESCRIPTION:
        {job_description}
        ### Instruction:
        You are Mohan, a business development executive at AtliQ. AtliQ is an AI & software consulting company dedicated to facilitating
        the seamless integration of business processes through automated tools.
        over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability,
        process optimization, cost reduction and heightened overall efficiency.
        your job is to write a cold email to the client regarding the job mentioned above describing the capability of AtliQ
        in fullfilling their needs.
        Also add most relevant once from the links to showcase Atliq's portifolio:{link_list}
        remember you are Mohan, BDE at  AtlilQ.
        do not provide a preamble.
        ### EMAIL (No Preamble):
        """
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": str(links)})
        return res.content
    
if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))

