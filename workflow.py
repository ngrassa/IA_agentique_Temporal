from temporalio import workflow
from datetime import timedelta
from activities_llm import analyze_with_llm
from activities_k8s import scale_k8s

@workflow.defn
class AutoScaleWorkflow:

    @workflow.run
    async def run(self, cpu_usage: int) -> str:

        # 1️⃣ Analyse via LLM (activity)
        recommendation = await workflow.execute_activity(
            analyze_with_llm,
            cpu_usage,
            start_to_close_timeout=timedelta(seconds=30),
        )

        # 2️⃣ Décision déterministe avec scale up et scale down
        if cpu_usage > 70 and recommendation == "SCALE_UP":
            await workflow.execute_activity(
                scale_k8s,
                10,  # réplicas pour scale up
                start_to_close_timeout=timedelta(seconds=30),
            )
            return "Scaling UP exécuté"

        elif cpu_usage < 30 and recommendation == "SCALE_DOWN":
            await workflow.execute_activity(
                scale_k8s,
                2,  # réplicas pour scale down
                start_to_close_timeout=timedelta(seconds=30),
            )
            return "Scaling DOWN exécuté"

        return "Aucune action"
