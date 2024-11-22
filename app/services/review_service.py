from typing import List

from app.repositories.openai import OpenAIClient


class CodeReviewService:
    def __init__(self, llm_client: OpenAIClient):
        self.llm_client = llm_client

    async def review_code(self, files: List[dict], repo_name: str) -> str:
        """
        Asks the AI to review code.

        This method takes a list of files and a repository name, and asks the AI
        to review the code. The AI is given the repository name and the contents
        of each file, and is asked to provide a review of the code.

        :param files: A list of dictionaries, each containing the file name and
                      content.
        :type files: List[dict]
        :param repo_name: The name of the repository to review.
        :type repo_name: str
        :return: The AI's review of the code.
        :rtype: str
        """
        messages = [
            {"role": "system", "content": "You are a code reviewer."},
            {"role": "user", "content": f"Review the following code: {repo_name}"},
        ]

        for file in files:
            messages.append(
                {
                    "role": "user",
                    "content": f"File: {file['path']}\n\n{file['content']}",
                }
            )

        return await self.llm_client.send_request(messages)
