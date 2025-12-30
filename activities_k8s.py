from temporalio import activity
import subprocess

@activity.defn
async def scale_k8s(replicas: int):
    subprocess.run(
        [
            "kubectl",
            "scale",
            "deployment",
            "myapp",
            f"--replicas={replicas}",
            "-n",
            "production"
        ],
        check=True
    )
