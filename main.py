from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from tools import market_content_research_tool, genai_content_research_tool, dataset_research_tool

llm = LLM(model="gpt-4o")


@CrewBase
class Multiagent():
	"""Multiagent crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	

	@agent
	def market_content_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['market_content_researcher'],
			tools=[market_content_research_tool]
		)
	
	@agent
	def market_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['market_researcher'],
			allow_delegation=True,
			verbose=True,
			llm=llm
		)
	
	@agent
	def genai_content_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['genai_content_researcher'],
			tools=[genai_content_research_tool]
		)
	
	@agent
	def resource_collector(self) -> Agent:
		return Agent(
			config=self.agents_config['resource_collector'],
			allow_delegation=True,
		)
	
	@agent
	def genai_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['genai_researcher'],
			allow_delegation=True,
			verbose=True
		)
	
	@agent
	def dataset_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['dataset_researcher'],
			tools=[dataset_research_tool],
			allow_delegation=True,
		)

	
	@task
	def market_content_research_task(self) -> Task:
		return Task(
			config=self.tasks_config['market_content_research_task']
		)
	
	@task
	def market_research_task(self) -> Task:
		return Task(
			config=self.tasks_config['market_research_task'],
			verbose=True,
			output_file='Market_Report.md'
		)
	
	@task
	def genai_content_research_task(self) -> Task:
		return Task(
			config=self.tasks_config['genai_content_research_task'],
		)
	
	@task
	def resource_collection_task(self) -> Task:
		return Task(
			config=self.tasks_config['resource_collection_task'],
			output_file='GenAi_Resources.md'
		)
	
	@task
	def genai_research_task(self) -> Task:
		return Task(
			config=self.tasks_config['genai_research_task'],
			verbose=True,
			output_file='Usecase_Report.md'
		)
	
	@task
	def dataset_research_task(self) -> Task:
		return Task(
			config=self.tasks_config['dataset_research_task'],
			output_file='Implementation_Resources.md'
		)
	
	

	@crew
	def crew(self) -> Crew:

		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
			output_log_file="logs.txt"
		)


if __name__ == "__main__":
	inputs = {
        "company":"Maruti Suzuki",
        "industry":"Automotive Manufacturing"
    }
	result = Multiagent().crew().kickoff(inputs=inputs)
