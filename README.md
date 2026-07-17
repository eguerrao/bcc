# DS21 Setup - Banco Central de Chile

Configuracion completa del servidor de datascience DS21.

## Especificaciones del servidor
- OS: RHEL 9.8
- CPU: Intel Xeon 6736P - 144 CPUs totales (2 sockets x 72 cores)
- RAM: ~3 TB
- GPU: NVIDIA H200 NVL
- Storage: 3.5 TB en /data

## Uso

```bash
git clone https://github.com/eguerrao/ds21-setup.git
cd ds21-setup
```

Leer setup_ds21.txt y ejecutar bloque por bloque como root.

## Bloques

| Bloque | Descripcion |
|--------|-------------|
| 1 | Preparacion SO |
| 2 | Usuario modules y EasyBuild |
| 3 | Configuracion global LMOD |
| 4 | Drivers NVIDIA H200 + CUDA 12.6 |
| 5 | FOSS Toolchain via EasyBuild |
| 6 | Python 3.12/3.13/3.14, R 4.4, Julia |
| 7 | UV gestor de entornos |
| 8 | RStudio Server |
| 9 | VSCode Server |
| 10 | SLURM 24.11 + slurmdbd |
| 11 | JupyterHub + BatchSpawner |
| 12 | Active Directory (SSSD) |
| 13 | HuggingFace + Nexus |
| 14 | Librerias GIS base |
| 15 | NFS hacia estaciones de escritorio |
| 16 | Monitoreo Grafana/Prometheus |
| 17 | Hardening |
| 18 | Miniconda |
| 19 | Verificaciones finales |

## Notas importantes
- Ajustar dominio AD (bcch.local) segun configuracion real
- Ajustar red NFS segun segmento real de las estaciones
- Ajustar URL de Nexus
- El bloque 4 requiere reboot antes de instalar driver NVIDIA
- El bloque 5 tarda varias horas compilando
