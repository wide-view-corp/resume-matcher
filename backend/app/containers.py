from dependency_injector import containers, providers
from app.services.llm import LLM
from app.services.resume_processor import ResumeProcessor

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    llm = providers.Singleton(LLM)
    resume_processor = providers.Singleton(ResumeProcessor)