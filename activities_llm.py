from temporalio import activity
import asyncio

@activity.defn
async def analyze_with_llm(cpu_load: int) -> str:
    print(f"🔍 CPU load = {cpu_load}%")
    await asyncio.sleep(1)
    if cpu_load > 70:
        return "SCALE_UP"
    elif cpu_load < 30:
        return "SCALE_DOWN"
    else:
        return "NO_ACTION"








