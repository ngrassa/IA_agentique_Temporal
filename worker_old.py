import asyncio
from temporalio.worker import Worker
from temporalio.client import Client
from workflow import AutoScaleWorkflow

async def main():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="autoscale-task-queue",
        workflows=[AutoScaleWorkflow],
    )

    await worker.run()

asyncio.run(main())
