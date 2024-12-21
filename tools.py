from crewai_tools import tool
from exa_py import Exa
import os

exa_api_key = os.getenv("EXA_API_KEY")

@tool("market research")
def market_content_research_tool(company: str, industry: str) -> dict:
    """ Searches and extracts market and competitor resources"""
    exa = Exa(exa_api_key)

    # Query for market resources
    market_query = f"Market reports and articles about {industry}"
    market_response = exa.search_and_contents(
        market_query,
        type="auto",
        num_results=10,
        text=True
    )

    market_resource_content = {
        result.title: result.text for result in market_response.results
    }


    # Query for company resources
    company_query = f"Market reports and articles about {company}"
    company_response = exa.search_and_contents(
        company_query,
        type="auto",
        num_results=5,
        text=True
    )

    company_resource_content = {
        result.title: result.text for result in company_response.results
    }

    # Query for competitor reports
    competitor_query = f"Competitor annual reports for {company}"
    competitor_response = exa.search_and_contents(
        competitor_query,
        type="auto",
        num_results=5,
        highlights=False
    )

    competitor_reports = {
        result.title: result.url for result in competitor_response.results
    }

    return company_resource_content, market_resource_content, competitor_reports




@tool("genai research")
def genai_content_research_tool(industry: str) -> dict:
    """ Searches and extracts genai application resources"""
    exa = Exa(exa_api_key)

    # Query for genai resources
    genai_query = f"Generative AI, Machine Learning, and Automation applications in {industry}"
    genai_response = exa.search_and_contents(
        genai_query,
        type="auto",
        num_results=10,
        text=True
    )

    resource_content = {
        result.title: result.text for result in genai_response.results
    }
    resource_links = {
        result.title: result.url for result in genai_response.results
    }


    return resource_content, resource_links


@tool("dataset research")
def dataset_research_tool(usecase: str) -> dict:
    """ Searches and extracts dataset resources for use cases"""
    exa = Exa(exa_api_key)

    # Query for dataset resources
    dataset_query = f"datasets on {usecase}"
    dataset_response = exa.search_and_contents(
        dataset_query,
        type="neural",
        use_autoprompt=True,
        num_results=5,
        include_domains=["kaggle.com", "huggingface.com. github.com"]
    )

    dataset_resources = {
        result.title: result.url for result in dataset_response.results
    }

    return dataset_resources