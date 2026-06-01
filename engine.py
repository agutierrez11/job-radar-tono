import json
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup

# --- Configuración del Perfil de Toño ---
USER_PROFILE = {
    'experiencia_core': ['fiserv', 'clip', 'adquirencia', 'pos', 'pagos digitales', 'payment', 'payments', 'pagos', 'acquiring', 'card', 'cards'],
    'conocimientos_clave': ['kyc', 'aml', 'pagos transfronterizos', 'fintech', 'crypto', 'blockchain', 'compliance'],
    'roles_preferidos': ['sales', 'ventas', 'comercial', 'account', 'business development', 'bd manager', 'hunter', 'director', 'lider', 'manager', 'lead', 'representative', 'growth'],
    'segmentos_preferidos': ['b2b', 'pyme', 'enterprise', 'latam', 'mexico'],
    'ubicacion_preferida': ['cancun', 'remoto', 'remote', 'mexico', 'latam'],
    'herramientas_bonus': ['salesforce', 'pipedrive', 'apollo', 'sales navigator'],
    'anios_experiencia_min': 5
}

# --- Lógica de Scoring con Regex y Límites de Palabra ---
def calculate_score(job_title, job_description, company, location):
    score = 0
    text_to_analyze = f"{job_title} {job_description} {company} {location}".lower()
    title_lower = job_title.lower()

    # Función auxiliar para buscar coincidencia exacta de palabra
    def contains_keyword(keyword, text):
        keyword = keyword.lower()
        if len(keyword) <= 4 or keyword.isalnum():
            # Exige límites de palabra completa (\b)
            pattern = r'\b' + re.escape(keyword) + r'\b'
            return bool(re.search(pattern, text))
        else:
            # Búsqueda substring para términos largos o compuestos
            return keyword in text

    # Nivel 1: Core Business (Pagos, Fintech, KYC/AML, Adquirencia) - Peso Alto
    core_keywords = USER_PROFILE['experiencia_core'] + USER_PROFILE['conocimientos_clave']
    matched_core = [kw for kw in core_keywords if contains_keyword(kw, text_to_analyze)]
    if matched_core:
        score += 40

    # Nivel 2: Rol Específico (Ventas, BD, Account Management, Growth) - Peso Alto
    matched_roles = [kw for kw in USER_PROFILE['roles_preferidos'] if contains_keyword(kw, title_lower)]
    if matched_roles:
        score += 30

    # Nivel 3: Segmento (B2B, LATAM, Enterprise) - Peso Medio
    matched_segments = [kw for kw in USER_PROFILE['segmentos_preferidos'] if contains_keyword(kw, text_to_analyze)]
    if matched_segments:
        score += 15

    # Nivel 4: Tecnología/SaaS - Peso Medio
    if any(contains_keyword(kw, text_to_analyze) for kw in ['saas', 'software', 'tech', 'technology', 'plataforma', 'platform']):
        score += 10

    # Nivel 5: Ubicación/Modalidad (Prioridad Remoto/México/LATAM) - Peso Bajo
    matched_locations = [kw for kw in USER_PROFILE['ubicacion_preferida'] if contains_keyword(kw, location.lower())]
    if matched_locations:
        score += 5

    # Bonus por Herramientas Conocidas
    matched_tools = [kw for kw in USER_PROFILE['herramientas_bonus'] if contains_keyword(kw, text_to_analyze)]
    if matched_tools:
        score += 5

    # Penalización por roles puramente técnicos o no relacionados
    tech_keywords = [
        'engineer', 'engineering', 'developer', 'developers', 'programmer', 
        'architect', 'technical', 'tech lead', 'frontend', 'backend', 'fullstack',
        'qa', 'tester', 'designer', 'diseñador', 'data analyst', 'analista de datos',
        'contable', 'accountant', 'junior', 'entry level'
    ]
    matched_tech = [kw for kw in tech_keywords if contains_keyword(kw, title_lower)]
    if matched_tech:
        score -= 50  # Penalización severa para evitar roles de software o analistas técnicos

    # Asegurar que el score no sea negativo ni exceda 100
    return min(100, max(0, score))

def clean_description(html_content):
    """Limpia el contenido HTML de las descripciones para guardarlo como texto limpio."""
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, "lxml")
    # Remover scripts y estilos
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text(separator=" ")
    # Limpiar espacios en blanco adicionales
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:200] + "..." if len(text) > 200 else text

# --- Scrapers de APIs de Empleo Reales ---
def fetch_jobicy_jobs(query):
    print(f"Buscando en Jobicy para: '{query}'...")
    url = f"https://jobicy.com/api/v2/remote-jobs?count=50&tag={query}"
    jobs = []
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            raw_jobs = response.json().get("jobs", [])
            for r in raw_jobs:
                jobs.append({
                    "empresa": r.get("companyName"),
                    "puesto": r.get("jobTitle"),
                    "descripcion": clean_description(r.get("jobDescription")),
                    "ubicacion": r.get("jobGeo", "Remote"),
                    "url": r.get("url")
                })
        else:
            print(f"Error de Jobicy ({response.status_code}) para '{query}'")
    except Exception as e:
        print(f"Error al conectar con Jobicy para '{query}': {e}")
    return jobs

def fetch_remotive_jobs(query):
    print(f"Buscando en Remotive para: '{query}'...")
    url = f"https://remotive.com/api/remote-jobs?search={query}&limit=50"
    jobs = []
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            raw_jobs = response.json().get("jobs", [])
            for r in raw_jobs:
                jobs.append({
                    "empresa": r.get("company_name"),
                    "puesto": r.get("title"),
                    "descripcion": clean_description(r.get("description")),
                    "ubicacion": r.get("candidate_required_location", "Remote"),
                    "url": r.get("url")
                })
        else:
            print(f"Error de Remotive ({response.status_code}) para '{query}'")
    except Exception as e:
        print(f"Error al conectar con Remotive para '{query}': {e}")
    return jobs

def fetch_all_live_vacancies():
    all_jobs = []
    # Consultamos términos relevantes para el perfil de Toño
    search_queries = ["payments", "fintech", "sales"]
    
    for query in search_queries:
        all_jobs += fetch_jobicy_jobs(query)
        all_jobs += fetch_remotive_jobs(query)
        
    print(f"Se obtuvieron {len(all_jobs)} vacantes brutas en total.")
    
    # Eliminar duplicados por URL de vacante
    unique_jobs = {job['url']: job for job in all_jobs}.values()
    print(f"Quedaron {len(unique_jobs)} vacantes únicas después de deduplicar.")
    
    processed_jobs = []
    for job in unique_jobs:
        score = calculate_score(job['puesto'], job['descripcion'], job['empresa'], job['ubicacion'])
        
        # Guardamos la justificación explicando por qué es un match
        justification_parts = []
        text_lower = f"{job['puesto']} {job['descripcion']} {job['empresa']} {job['ubicacion']}".lower()
        
        # Construir justificación dinámica basada en los matches
        matched_cores = [kw for kw in USER_PROFILE['experiencia_core'] + USER_PROFILE['conocimientos_clave'] if kw.lower() in text_lower]
        if matched_cores:
            justification_parts.append(f"Sector: Coincide con tu experiencia en {', '.join(matched_cores[:3]).upper()}.")
            
        matched_roles = [kw for kw in USER_PROFILE['roles_preferidos'] if kw.lower() in job['puesto'].lower()]
        if matched_roles:
            justification_parts.append(f"Rol: Posición de {', '.join(matched_roles).capitalize()}.")
            
        if any(kw in job['ubicacion'].lower() for kw in USER_PROFILE['ubicacion_preferida']):
            justification_parts.append("Modalidad: Remoto / Cobertura LATAM.")
            
        justification = " ".join(justification_parts) if justification_parts else "Coincidencia de perfil comercial tecnológico."
        
        processed_jobs.append({
            "empresa": job["empresa"],
            "puesto": job["puesto"],
            "ubicacion": job["ubicacion"],
            "url": job["url"],
            "match_score": round(score / 100, 2),
            "justificacion": justification
        })
        
    return processed_jobs

# --- Función Principal para Actualizar el Radar ---
def update_job_radar():
    # Para limpiar los datos mock previos y enlaces caídos, 
    # nos enfocaremos únicamente en las vacantes frescas obtenidas hoy en vivo.
    new_jobs = fetch_all_live_vacancies()
    
    # Filtrar para mantener solo trabajos con match_score >= 0.40 (40%+)
    relevant_new_jobs = [job for job in new_jobs if job['match_score'] >= 0.40]
    
    # Usamos únicamente las vacantes vivas
    all_vacancies_dict = {job['url']: job for job in relevant_new_jobs}
        
    # Ordenar todas por score de mayor a menor y limitar a las mejores 50
    sorted_vacancies = sorted(list(all_vacancies_dict.values()), key=lambda x: x['match_score'], reverse=True)[:50]

    with open('vacancies.json', 'w', encoding='utf-8') as f:
        json.dump(sorted_vacancies, f, indent=4, ensure_ascii=False)
    
    print(f"Radar actualizado. Se guardaron las mejores {len(sorted_vacancies)} vacantes vivas con score >= 40%.")

if __name__ == "__main__":
    update_job_radar()
