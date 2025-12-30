from temporalio import workflow

@workflow.defn
class AutoScaleWorkflow:
    @workflow.run
    async def run(self, service_name: str):
        return f"Autoscaling triggered for {service_name}"
