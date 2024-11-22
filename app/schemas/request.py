import re

from pydantic import BaseModel, HttpUrl, field_validator


class ReviewRequest(BaseModel):
    url: HttpUrl

    @field_validator("url")
    def validate_repo_url(cls, url: HttpUrl):
        if re.match(r"https://github\.com/[\w-]+/[\w-]+", url):
            return url

        raise ValueError("Invalid repository URL")
