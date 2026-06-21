# Fintech Job Radar 🚀🕵️‍♂️

<p align="center">
  <a href="#-english">🇺🇸 English</a> | 
  <a href="#-español">🇪🇸 Español</a>
</p>

---

## 🇺🇸 English

### What is Fintech Job Radar?
Fintech Job Radar is an autonomous search and recommendation engine designed to source, grade, and display job openings in the Fintech, Payments, and Identity Verification sectors that match a specific candidate profile.

### How it Works
1. **Autonomous Search (`engine.py`):** A Python engine query specialized job portals and corporate career sites.
2. **Matching Profile Score:** The system grades each role based on keyword matching and semantic alignment:
   * **Core Business (+40 pts):** Payments, Adquirers, KYC/AML, POS.
   * **Commercial Role (+30 pts):** Enterprise Sales, Account Management, BD Manager.
   * **Segment (+15 pts):** B2B, SME, LATAM.
   * **Tools & Tech (+15 pts):** SaaS, Salesforce, Pipedrive, Apollo.
3. **GitHub Actions Automation:** Runs automatically every day via a cron schedule, executing the python script and committing the updated database (`vacancies.json`) directly to the repository.
4. **Vercel Web App:** The frontend (`index.html`) displays active vacancies ranked by score with an AI-generated match justification.

### Tech Stack
* **Engine:** Python, pandas, requests, BeautifulSoup
* **Database:** JSON (`vacancies.json` / `active_vacancies_may_2026.json`)
* **Automation:** GitHub Actions (.yml workflow)
* **Frontend:** Vanilla HTML5 / Tailwind CSS
* **Deployment:** Vercel

---

## 🇪🇸 Español

### ¿Qué es Fintech Job Radar?
Fintech Job Radar es un motor autónomo de búsqueda y recomendación diseñado para recopilar, calificar y mostrar vacantes de empleo en los sectores de Fintech, Medios de Pago y Verificación de Identidad que coincidan con un perfil profesional específico.

### Cómo Funciona
1. **Búsqueda Autónoma (`engine.py`):** Un motor en Python consulta portales especializados y bolsas de trabajo corporativas.
2. **Puntaje de Coincidencia (Matching Score):** El sistema califica cada puesto analizando palabras clave y alineación semántica:
   * **Core Business (+40 pts):** Medios de pago, Adquirencia, KYC/AML, terminales punto de venta (POS).
   * **Rol Comercial (+30 pts):** Ventas Corporativas (Enterprise Sales), Gestión de Cuentas (Account Management), Gerente de Desarrollo de Negocios (BD Manager).
   * **Segmento (+15 pts):** B2B, PyMEs, LATAM.
   * **Herramientas y Tecnología (+15 pts):** SaaS, Salesforce, Pipedrive, Apollo.
3. **Automatización con GitHub Actions:** Se ejecuta de forma autónoma diariamente mediante un cron, corre el motor en Python y realiza un commit automático de la base de datos actualizada (`vacancies.json`) al repositorio.
4. **Interfaz Web en Vercel:** El frontend (`index.html`) muestra los puestos activos ordenados por puntaje de afinidad, incluyendo una justificación generada por IA sobre el ajuste del perfil.

### Stack Tecnológico
* **Motor:** Python, pandas, requests, BeautifulSoup
* **Base de Datos:** Archivos JSON (`vacancies.json` / `active_vacancies_may_2026.json`)
* **Automatización:** GitHub Actions (flujo de trabajo .yml)
* **Frontend:** HTML5 básico / Tailwind CSS
* **Despliegue:** Vercel
