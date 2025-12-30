from temporalio import workflow
from activities import say_hello
from datetime import timedelta

@workflow.defn
class HelloWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        result = await workflow.execute_activity(
            say_hello,
            name,
            start_to_close_timeout=timedelta(seconds=10),
        )
        return result
