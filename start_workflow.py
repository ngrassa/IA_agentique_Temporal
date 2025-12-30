import asyncio
from temporalio.client import Client
from workflow import AutoScaleWorkflow  # Assure-toi que c’est bien le fichier 'workflows.py'

async def main():
    # Connexion au serveur Temporal
    client = await Client.connect("localhost:7233")

    # Lancer le workflow
    result = await client.execute_workflow(
        AutoScaleWorkflow.run,
        50,  # exemple de CPU load à passer au workflow
        id="autoscale-prod-006",
        task_queue="autoscale-queue"
    )

    print("Résultat :", result)

# Exécuter le script
asyncio.run(main())
