from langchain.prompts import PromptTemplate

def init_prompt():
    prompt_extract = PromptTemplate.from_template(
        """
        ### DICTIONARY CONTAINING PAGE_NUMBER AS KEY AND SLA CONTENT IN THAT PAGE AS VALUE
        {sla_docs}

        ### INSTRUCTION
        You are a helpful assistant that extracts information from the SLA document based on the user's question.

        ### USER QUESTION
        {user_question}

        ### RESPONSE
        Always Provide a valid string(which can be easily converted to json using json.loads) with no PREAMBLE containing the following keys SLA Name, Parties Involved(An array), System Concerned, Description, 
        Associated Metrics(an Array) and Page Number). If the information is not available, set the value to 'N/A'.
        """
    )

    return prompt_extract

def qna_prompt():
    prompt_template = PromptTemplate.from_template(
        """
        You are a helpful Q and A Tool, that helps in answering crisp and concise answers given a context and a question. 
        Context: {context}

        Question: {question}
        """
    )

    return prompt_template