from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI QA Bug Triage Automation Agent"
    app_env: str = "development"
    database_url: str = "sqlite:///./bug_triage.db"
    human_review_severities: str = "critical,high"
    duplicate_threshold: int = 82

    openai_api_key: str = ""
    openai_model: str = "gpt-5.6-luna"
    use_openai: bool = False

    jira_enabled: bool = False
    jira_base_url: str = ""
    jira_email: str = ""
    jira_api_token: str = ""
    jira_project_key: str = "QA"
    jira_issue_type: str = "Bug"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def review_severities(self) -> set[str]:
        return {x.strip().lower() for x in self.human_review_severities.split(",") if x.strip()}


@lru_cache
def get_settings() -> Settings:
    return Settings()
