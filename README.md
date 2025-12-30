# Lien viédo sur ma chaine Youtube ( Nordine GRASSA)

https://youtu.be/E1VbDaT6BW8

# Temporal AutoScale Workflow

Ce projet est un exemple complet d'autoscaling simulé avec **Temporal**, intégrant la prise de décision via une activity simulant un LLM et l'exécution d'actions de scaling sur Kubernetes (Minikube).

Il permet de tester **scale up**, **scale down**, et **no action** selon la charge CPU simulée.

---

## 🛠 Prérequis

* Python 3.13+
* Temporal Server (local ou docker)
* Minikube ou cluster Kubernetes accessible
* `kubectl` installé et configuré pour accéder au cluster
* Virtualenv recommandé pour isoler les packages Python

---

## 📁 Structure du projet

```
tp-temporal/
├── activities_k8s.py       # Activity pour simuler le scale Kubernetes
├── activities_llm.py       # Activity pour analyser CPU et recommander SCALE_UP / SCALE_DOWN
├── workflow.py             # Workflow AutoScaleWorkflow
├── worker.py               # Worker Temporal
├── start_workflow.py       # Script pour lancer le workflow
├── venv/                   # Virtualenv Python
└── README.md
```

---

## ⚡ Setup

1. **Créer et activer l'environnement virtuel**

```bash
python3 -m venv venv
source venv/bin/activate
pip install temporalio
```

2. **Vérifier kubectl et Minikube**

```bash
kubectl version --client
minikube status
kubectl create namespace production
kubectl create deployment myapp --image=nginx -n production
```

3. **Démarrer le worker Temporal**

```bash
source venv/bin/activate
python worker.py
```

4. **Lancer le workflow**

```bash
python start_workflow.py
```

* Pour tester **scale up**, passer CPU > 80
* Pour tester **scale down**, passer CPU < 30
* Entre 30 et 80 → `"Aucune action"`

---

## 📝 Exemple de `start_workflow.py`

```python
import asyncio
from temporalio.client import Client
from workflow import AutoScaleWorkflow

async def main():
    client = await Client.connect("localhost:7233")
    result = await client.execute_workflow(
        AutoScaleWorkflow.run,
        20,  # CPU simulé pour test
        id="autoscale-prod-test",
        task_queue="autoscale-queue"
    )
    print("Résultat :", result)

asyncio.run(main())
```

---

## 📝 Exemple d’activity `analyze_with_llm`

```python
from temporalio import activity

@activity.defn
async def analyze_with_llm(cpu_load: int) -> str:
    print(f"🔍 CPU load reçu = {cpu_load}%")
    if cpu_load > 70:
        return "SCALE_UP"
    elif cpu_load < 30:
        return "SCALE_DOWN"
    else:
        return "NO_ACTION"
```

---

## 📝 Exemple d’activity `scale_k8s`

```python
import asyncio
import subprocess
from temporalio import activity

@activity.defn
async def scale_k8s(replicas: int) -> str:
    cmd = ["kubectl", "scale", "deployment", "myapp", f"--replicas={replicas}", "-n", "production"]
    try:
        result = await asyncio.to_thread(subprocess.run, cmd, check=True, capture_output=True, text=True)
        return f"Scaling appliqué avec succès : {result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"❌ Échec du scaling : {e.stderr}"
```

---

## 🔹 Points clés

* Workflow **AutoScaleWorkflow** :

  * Appelle `analyze_with_llm` pour décider de l’action
  * Appelle `scale_k8s` pour appliquer le scaling
* Worker exécute toutes les activities et les workflows
* Compatible avec l’UI Temporal pour visualiser chaque activity et son résultat
* Simule un autoscaling simple sur Kubernetes

---

## 🚀 Notes

* Assurez-vous que `kubectl` est dans le PATH du worker
* Pour tests locaux, le scale est appliqué sur un déploiement Minikube
* Les activités sont asynchrones pour éviter les crashs du worker
