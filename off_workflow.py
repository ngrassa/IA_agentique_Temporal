import asyncio
from temporalio.client import Client
from workflow import AutoScaleWorkflow   # 👈 ce fichier doit exister

async def start():
    client = await Client.connect("localhost:7233")

    result = await client.execute_workflow(
        AutoScaleWorkflow.run,
        "api-service",
        id="autoscale-workflow-1",
        task_queue="autoscale-task-queue",
    )

    print("Résultat:", result)

asyncio.run(start())
