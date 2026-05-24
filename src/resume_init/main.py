#!/usr/bin/env python
from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from resume_init.crews.job_search_crew.job_search_crew import JobSearchCrew


class JobSearchState(BaseModel):
    search_query: str = "Java Technical Lead"
    job_search_results: str = ""


class JobSearchFlow(Flow[JobSearchState]):

    @start()
    def initialize_search(self, crewai_trigger_payload: dict = None):
        print("Initializing job search")

        # Use trigger payload if available
        if crewai_trigger_payload:
            self.state.search_query = crewai_trigger_payload.get('search_query', "Java Technical Lead")
            print(f"Using trigger payload: {crewai_trigger_payload}")
        else:
            self.state.search_query = "Java Technical Lead"

    @listen(initialize_search)
    def search_jobs(self):
        print(f"Searching jobs for: {self.state.search_query}")
        result = (
            JobSearchCrew()
            .crew()
            .kickoff()
        )

        print("Job search completed.")
        self.state.job_search_results = result.raw


def kickoff():
    job_search_flow = JobSearchFlow()
    job_search_flow.kickoff()


def plot():
    job_search_flow = JobSearchFlow()
    job_search_flow.plot()


def run_with_trigger():
    """
    Run the flow with trigger payload.
    """
    import json
    import sys

    # Get trigger payload from command line argument
    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    # Create flow and kickoff with trigger payload
    job_search_flow = JobSearchFlow()

    try:
        result = job_search_flow.kickoff({"crewai_trigger_payload": trigger_payload})
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the flow with trigger: {e}")


if __name__ == "__main__":
    kickoff()
