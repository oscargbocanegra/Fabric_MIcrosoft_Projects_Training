# 🏗️ Microsoft Fabric – Proyectos de Aprendizaje con Arquitectura Medallón

> Repositorio educativo con proyectos prácticos de **Microsoft Fabric** implementando la **Arquitectura Medallón** (Bronze → Silver → Gold) sobre **OneLake**.

---

## 📋 Tabla de Contenidos

1. [¿Qué es Microsoft Fabric?](#-qué-es-microsoft-fabric)
2. [Arquitectura Medallón](#-arquitectura-medallón)
3. [Estructura del Repositorio](#-estructura-del-repositorio)
4. [Proyectos](#-proyectos)
5. [Requisitos Previos](#-requisitos-previos)
6. [Cómo Empezar](#-cómo-empezar)
7. [Tecnologías y Herramientas](#-tecnologías-y-herramientas)
8. [Recursos y Referencias](#-recursos-y-referencias)
9. [Contribuir](#-contribuir)
10. [Licencia](#-licencia)

---

## 🌐 ¿Qué es Microsoft Fabric?

[Microsoft Fabric](https://learn.microsoft.com/es-es/fabric/get-started/microsoft-fabric-overview) es una plataforma de analítica unificada y de extremo a extremo que integra en un solo entorno SaaS capacidades de:

| Servicio | Descripción |
|---|---|
| **Data Factory** | Orquestación e integración de datos (ETL/ELT) |
| **Synapse Data Engineering** | Procesamiento de datos a escala con Apache Spark |
| **Synapse Data Warehouse** | Almacén de datos SQL de alto rendimiento |
| **Synapse Data Science** | Experimentación y operacionalización de modelos ML |
| **Real-Time Analytics** | Ingesta y análisis de datos en tiempo real (KQL) |
| **Power BI** | Visualización interactiva de datos y BI |
| **Data Activator** | Alertas y automatización basadas en datos |

Todos los servicios comparten un almacenamiento unificado llamado **OneLake**, que actúa como el "lago de datos" de toda la organización, eliminando silos y reduciendo la duplicación de datos.

---

## 🥇 Arquitectura Medallón

La **Arquitectura Medallón** (Medallion Architecture) es un patrón de diseño de datos que organiza los datos en capas progresivas de calidad dentro de un Data Lakehouse. Es el estándar recomendado por Microsoft para proyectos con Microsoft Fabric y OneLake.

```
┌──────────────────────────────────────────────────────────────┐
│                         OneLake                              │
│                                                              │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────────┐   │
│  │   🥉 BRONZE  │──▶│  🥈 SILVER  │──▶│    🥇 GOLD      │   │
│  │  (Raw Layer) │   │(Cleansed)   │   │  (Business)     │   │
│  └─────────────┘   └─────────────┘   └─────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

### 🥉 Capa Bronze (Raw / Landing)

- **Propósito:** Ingesta de datos tal como vienen de las fuentes originales, sin transformaciones.
- **Formato típico:** Parquet, Delta, CSV, JSON, Avro.
- **Principio:** "Append-only" — nunca se modifica el dato original.
- **En Fabric:** Lakehouse con tablas Delta o archivos en OneLake.

### 🥈 Capa Silver (Cleansed / Enriched)

- **Propósito:** Limpieza, validación, deduplicación y enriquecimiento de datos.
- **Transformaciones:** Normalización de tipos, tratamiento de nulos, joins entre fuentes.
- **Formato típico:** Tablas Delta con esquema definido.
- **En Fabric:** Notebooks Spark o Dataflows Gen2.

### 🥇 Capa Gold (Curated / Business-Ready)

- **Propósito:** Datos agregados y modelados listos para consumo analítico y reportes.
- **Modelado:** Esquemas estrella/copo de nieve, tablas de hechos y dimensiones.
- **Consumidores:** Power BI, Data Warehouse SQL, APIs.
- **En Fabric:** Warehouse SQL o vistas semánticas (Semantic Model).

---

## 📁 Estructura del Repositorio

```
Fabric_MIcrosoft_Projects_Training/
│
├── README.md                        # Este archivo
├── LICENSE                          # Licencia del proyecto
├── .gitignore
│
├── 01_foundations/                  # Conceptos fundamentales de Fabric
│   ├── README.md
│   ├── onelake_intro/
│   └── fabric_services_overview/
│
├── 02_bronze_layer/                 # Ingesta de datos (Raw)
│   ├── README.md
│   ├── data_factory_pipelines/      # Pipelines de Data Factory
│   ├── eventstream/                 # Ingesta en tiempo real
│   └── notebooks/                  # Notebooks de ingesta con Spark
│
├── 03_silver_layer/                 # Transformación y limpieza
│   ├── README.md
│   ├── spark_transformations/       # Notebooks PySpark
│   ├── dataflows_gen2/              # Dataflows Gen2
│   └── data_quality/               # Reglas de calidad de datos
│
├── 04_gold_layer/                   # Capa de negocio
│   ├── README.md
│   ├── star_schema/                 # Modelado dimensional
│   ├── warehouse_sql/               # Scripts T-SQL para Warehouse
│   └── semantic_models/            # Modelos semánticos Power BI
│
├── 05_reporting/                    # Visualización y reportes
│   ├── README.md
│   └── power_bi_reports/           # Archivos .pbix y plantillas DAX
│
├── 06_realtime_analytics/           # Análisis en tiempo real
│   ├── README.md
│   ├── kql_databases/              # Consultas KQL
│   └── eventstream_projects/
│
├── 07_data_science/                 # Machine Learning en Fabric
│   ├── README.md
│   ├── experiments/                # Experimentos MLflow
│   └── models/                     # Modelos entrenados
│
└── 08_projects/                     # Proyectos integradores
    ├── README.md
    └── project_01_sales_analytics/  # Ejemplo: Análisis de Ventas E2E
```

---

## 🚀 Proyectos

| # | Proyecto | Descripción | Capas | Estado |
|---|---|---|---|---|
| 01 | **Introducción a Fabric** | Configuración del workspace y exploración de OneLake | — | 🔄 En progreso |
| 02 | **Pipeline ETL Básico** | Ingesta CSV → Bronze → Silver con Data Factory y Spark | Bronze, Silver | 📋 Planificado |
| 03 | **Análisis de Ventas E2E** | Pipeline completo con Power BI dashboard final | Bronze→Gold | 📋 Planificado |
| 04 | **Streaming con EventStream** | Ingesta de eventos en tiempo real | Bronze, Silver | 📋 Planificado |
| 05 | **ML con Fabric Data Science** | Entrenamiento y despliegue de modelo predictivo | Silver, Gold | 📋 Planificado |

---

## ✅ Requisitos Previos

### Cuenta y Acceso

- [ ] **Cuenta Microsoft** (personal, educativa o corporativa)
- [ ] **Suscripción Microsoft Fabric** (Trial gratuito de 60 días disponible en [aka.ms/try-fabric](https://aka.ms/try-fabric))
- [ ] **Workspace de Fabric** con capacidad Fabric habilitada

### Herramientas Locales (Opcionales)

| Herramienta | Versión | Uso |
|---|---|---|
| [Git](https://git-scm.com/) | ≥ 2.40 | Control de versiones |
| [Python](https://www.python.org/) | ≥ 3.10 | Desarrollo de notebooks |
| [Visual Studio Code](https://code.visualstudio.com/) | Latest | Editor con extensiones de Fabric |
| [Power BI Desktop](https://powerbi.microsoft.com/desktop/) | Latest | Desarrollo de reportes |
| [Azure Data Studio](https://azure.microsoft.com/products/data-studio) | Latest | Queries SQL al Warehouse |

### Extensiones VS Code Recomendadas

```
ms-python.python
ms-toolsai.jupyter
ms-azure-devops.azure-pipelines
```

---

## 🛠️ Cómo Empezar

### 1. Clonar el Repositorio

```bash
git clone https://github.com/oscargbocanegra/Fabric_MIcrosoft_Projects_Training.git
cd Fabric_MIcrosoft_Projects_Training
```

### 2. Crear un Workspace en Microsoft Fabric

1. Acceder a [app.fabric.microsoft.com](https://app.fabric.microsoft.com)
2. Ir a **Workspaces** → **Nuevo workspace**
3. Asignar un nombre descriptivo (ej. `fabric-training-ws`)
4. Habilitar la licencia **Fabric** (Trial o Premium)

### 3. Configurar OneLake

1. Dentro del workspace, crear un **Lakehouse**
2. Definir la estructura de carpetas:
   ```
   Files/
   ├── bronze/
   ├── silver/
   └── gold/
   ```

### 4. Ejecutar el Primer Proyecto

Navega a `01_foundations/` y sigue el `README.md` específico de cada módulo.

---

## 🔧 Tecnologías y Herramientas

```
Microsoft Fabric
├── OneLake                  ← Almacenamiento unificado (Delta Lake)
├── Data Factory             ← Orquestación de pipelines
├── Synapse Spark            ← Procesamiento distribuido (PySpark / Scala)
├── Synapse Warehouse        ← SQL analítico (T-SQL)
├── Real-Time Analytics      ← KQL / EventStream
├── Data Science             ← MLflow / scikit-learn / PyTorch
└── Power BI                 ← Visualización y DAX

Lenguajes
├── Python / PySpark         ← Transformaciones en notebooks
├── T-SQL                    ← Consultas en Warehouse
├── KQL                      ← Kusto Query Language (tiempo real)
└── DAX                      ← Cálculos en Power BI

Formatos de Datos
├── Delta Lake               ← Formato principal en OneLake
├── Parquet                  ← Almacenamiento columnar
└── JSON / CSV               ← Ingesta de datos crudos
```

---

## 📚 Recursos y Referencias

### Documentación Oficial

- 📖 [Microsoft Fabric Documentation](https://learn.microsoft.com/fabric/)
- 🏗️ [Medallion Architecture in Fabric](https://learn.microsoft.com/fabric/onelake/onelake-medallion-lakehouse-architecture)
- 🔥 [Delta Lake Documentation](https://docs.delta.io/)
- 📊 [Power BI Documentation](https://learn.microsoft.com/power-bi/)

### Aprendizaje Guiado

- 🎓 [Microsoft Learn – Fabric](https://learn.microsoft.com/training/browse/?products=fabric)
- 🎓 [Fabric Analytics Engineer (DP-600)](https://learn.microsoft.com/certifications/fabric-analytics-engineer-associate/)
- 📺 [Microsoft Fabric YouTube Channel](https://www.youtube.com/@MicrosoftFabric)

### Comunidad

- 💬 [Microsoft Fabric Community](https://community.fabric.microsoft.com/)
- 🐙 [Microsoft Fabric Samples (GitHub)](https://github.com/microsoft/fabric-samples)

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Para contribuir:

1. Haz un **fork** del repositorio
2. Crea una rama descriptiva: `git checkout -b feature/nuevo-proyecto-ventas`
3. Realiza tus cambios y documenta con un `README.md` en la carpeta del proyecto
4. Envía un **Pull Request** con descripción detallada

Por favor sigue la estructura de carpetas definida en este README para mantener consistencia.

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

<div align="center">

**⭐ Si este repositorio te resulta útil, dale una estrella en GitHub ⭐**

Hecho con ❤️ para la comunidad de Microsoft Fabric en español

</div>
