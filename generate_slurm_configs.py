#!/usr/bin/env python3
"""
Generador de archivos de configuracion SLURM para DS21
Banco Central de Chile - Tecnologias Avanzadas Aplicadas SpA
"""

import os

# ─────────────────────────────────────────────────
# PARAMETROS DEL CLUSTER - AJUSTAR AQUI
# ─────────────────────────────────────────────────
CONFIG = {
    "cluster_name":      "ds21",
    "controller_host":   "srvdatscience21",
    "node_name":         "srvdatscience21",
    "cpus":              144,
    "sockets":           2,
    "cores_per_socket":  72,
    "threads_per_core":  1,
    "real_memory_mb":    3093504,   # ~3TB en MB
    "gpu_type":          "h200",
    "gpu_count":         1,
    "gpu_device":        "/dev/nvidia0",
    "partition_name":    "main",
    "def_mem_per_cpu":   4096,      # MB por defecto por CPU
    "max_mem_per_cpu":   32768,     # MB maximo por CPU
    "db_password":       "SlurmDBPass2026",
    "output_dir":        "/etc/slurm",
}

os.makedirs(CONFIG["output_dir"], exist_ok=True)

# ─────────────────────────────────────────────────
# slurm.conf
# ─────────────────────────────────────────────────
slurm_conf = f"""# slurm.conf - DS21 Banco Central de Chile
# Generado por generate_slurm_configs.py

ClusterName={CONFIG["cluster_name"]}
SlurmctldHost={CONFIG["controller_host"]}

# Autenticacion
AuthType=auth/munge
CryptoType=crypto/munge

# Puertos
SlurmctldPort=6817
SlurmdPort=6818

# Directorios
SlurmdSpoolDir=/var/spool/slurm/d
SlurmctldPidFile=/var/run/slurmctld.pid
SlurmdPidFile=/var/run/slurmd.pid
StateSaveLocation=/var/spool/slurm/ctld

# Logs
SlurmctldLogFile=/var/log/slurm/slurmctld.log
SlurmdLogFile=/var/log/slurm/slurmd.log
SlurmctldDebug=info
SlurmdDebug=info

# Scheduler
SchedulerType=sched/backfill
SelectType=select/cons_tres
SelectTypeParameters=CR_Core_Memory

# Prioridades y fairshare
PriorityType=priority/multifactor
PriorityWeightFairshare=100
PriorityWeightAge=10
PriorityWeightJobSize=10
PriorityDecayHalfLife=7-0

# Accounting (slurmdbd)
AccountingStorageType=accounting_storage/slurmdbd
AccountingStorageHost=localhost
AccountingStoragePort=6819
AccountingStorageTres=gres/gpu
JobAcctGatherType=jobacct_gather/cgroup
JobAcctGatherFrequency=30

# GPU
GresTypes=gpu

# Procesos y cgroups
MpiDefault=pmix
ProctrackType=proctrack/cgroup
TaskPlugin=task/cgroup,task/affinity

# Timeouts
SlurmctldTimeout=300
SlurmdTimeout=300
InactiveLimit=0
MinJobAge=300
KillWait=30
Waittime=0

# Nodo: controller + compute (nodo unico)
NodeName={CONFIG["node_name"]} \\
  CPUs={CONFIG["cpus"]} \\
  Sockets={CONFIG["sockets"]} \\
  CoresPerSocket={CONFIG["cores_per_socket"]} \\
  ThreadsPerCore={CONFIG["threads_per_core"]} \\
  RealMemory={CONFIG["real_memory_mb"]} \\
  Gres=gpu:{CONFIG["gpu_type"]}:{CONFIG["gpu_count"]} \\
  State=UNKNOWN

# Particion principal
PartitionName={CONFIG["partition_name"]} \\
  Nodes={CONFIG["node_name"]} \\
  Default=YES \\
  MaxTime=INFINITE \\
  State=UP \\
  DefMemPerCPU={CONFIG["def_mem_per_cpu"]} \\
  MaxMemPerCPU={CONFIG["max_mem_per_cpu"]}
"""

# ─────────────────────────────────────────────────
# gres.conf
# ─────────────────────────────────────────────────
gres_conf = f"""# gres.conf - Configuracion GPU DS21
# Generado por generate_slurm_configs.py

Name=gpu Type={CONFIG["gpu_type"]} File={CONFIG["gpu_device"]} COREs=0-{CONFIG["cpus"]-1}
"""

# ─────────────────────────────────────────────────
# cgroup.conf
# ─────────────────────────────────────────────────
cgroup_conf = """# cgroup.conf - DS21
# Generado por generate_slurm_configs.py

CgroupPlugin=cgroup/v2
ConstrainCores=yes
ConstrainRAMSpace=yes
ConstrainSwapSpace=yes
ConstrainDevices=yes
"""

# ─────────────────────────────────────────────────
# slurmdbd.conf
# ─────────────────────────────────────────────────
slurmdbd_conf = f"""# slurmdbd.conf - DS21 Banco Central de Chile
# Generado por generate_slurm_configs.py

AuthType=auth/munge
DbdHost=localhost
DbdPort=6819
SlurmUser=slurm
LogFile=/var/log/slurm/slurmdbd.log
PidFile=/var/run/slurmdbd.pid
StorageType=accounting_storage/mysql
StorageHost=localhost
StorageUser=slurm
StoragePass={CONFIG["db_password"]}
StorageLoc=slurm_acct_db
"""

# ─────────────────────────────────────────────────
# Escribir archivos
# ─────────────────────────────────────────────────
files = {
    "slurm.conf":    slurm_conf,
    "gres.conf":     gres_conf,
    "cgroup.conf":   cgroup_conf,
    "slurmdbd.conf": slurmdbd_conf,
}

for filename, content in files.items():
    path = os.path.join(CONFIG["output_dir"], filename)
    with open(path, "w") as f:
        f.write(content)
    print(f"Generado: {path}")

# slurmdbd.conf requiere permisos restrictivos
slurmdbd_path = os.path.join(CONFIG["output_dir"], "slurmdbd.conf")
os.chmod(slurmdbd_path, 0o600)
print(f"Permisos 600 aplicados a slurmdbd.conf")

print("\nArchivos generados en", CONFIG["output_dir"])
print("Ejecutar como root para aplicar permisos de ownership:")
print("  chown slurm:slurm /etc/slurm/slurmdbd.conf")
print("  chown slurm:slurm /etc/slurm/slurm.conf")
