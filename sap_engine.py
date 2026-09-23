import os
from dotenv import load_dotenv
from groq import Groq
from duckduckgo_search import DDGS

# 1. Automatically load secret variables from the .env file
load_dotenv()

# 2. Safely read the API key from environment memory
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing! Make sure it is defined inside your .env file.")

# 3. Initialize Groq client securely
groq_client = Groq(api_key=GROQ_API_KEY)


def search_web_for_sap(user_query: str) -> str:
    """
    Searches online resources (Reddit, SAP Forums, Google) via DuckDuckGo.
    """
    search_prompt = f"site:community.sap.com OR site:reddit.com/r/SAP {user_query}"
    search_results = []
    
    try:
        results = DDGS().text(search_prompt, max_results=5)
        for r in results:
            search_results.append(f"Title: {r.get('title')}\nSnippet: {r.get('body')}\nURL: {r.get('href')}")
        return "\n\n".join(search_results)
    except Exception as e:
        return f"Web search could not retrieve live data: {str(e)}"


def query_sap_assistant(user_query: str) -> str:
    """
    Queries the LLM using live web search context across Basis, S/4HANA, and ABAP.
    """
    # Fetch web context
    web_context = search_web_for_sap(user_query)

    # System prompt covering SAP Basis, S/4HANA, and ABAP
    system_prompt = f"""
    You are an expert Enterprise Support AI specialized in:
    1. SAP Basis Administration & System Diagnostics
    2. SAP S/4HANA Core Functionality & Configuration
    3. SAP ABAP Programming (Syntax, BAPIs, BAdIs, Enhancements, CDS Views)

    Analyze the user's issue using the online web and forum context below.

    Online Web/Forum Context:
    {web_context}

    CRITICAL FORMATTING INSTRUCTIONS:
    - DO NOT output Markdown tables. Tables break code rendering in Streamlit.
    - Write code snippets in standalone ```abap code blocks outside of lists or tables.

    Provide your response using this exact structure:

    ### 1. ISSUE / CONCEPT OVERVIEW
    Brief technical summary.

    ### 2. ROOT CAUSE / TECHNICAL DETAILS
    Technical breakdown using bold text and bullet points (BAdI Name, Interface, Methods).

    ### 3. STEP-BY-STEP SOLUTION & CODE SNIPPET
    Numbered action steps followed by complete, standalone ABAP code blocks.

    ### 4. SAP TRANSACTION CODES & ROLES
    List relevant T-Codes (e.g., SE18, SE19, ST22, SU53, SPRO, MIGO) and required Basis roles.
    """

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ],
        temperature=0.2,
        max_tokens=800
    )
    
    return response.choices[0].message.content