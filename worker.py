from temporalio.worker import Worker
from temporalio.client import Client
import asyncio

from workflow import AutoScaleWorkflow
from activities_llm import analyze_with_llm
from activities_k8s import scale_k8s

async def main():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="autoscale-queue",
        workflows=[AutoScaleWorkflow],
        activities=[analyze_with_llm, scale_k8s],
    )

    await worker.run()

asyncio.run(main())
