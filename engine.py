import json
import re
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup

# --- Configuración del Perfil de Toño ---
USER_PROFILE = {
    'experiencia_core': ['fiserv', 'clip', 'adquirencia', 'pos', 'pagos digitales', 'payment', 'payments', 'pagos', 'acquiring', 'card', 'cards', 'adquirente'],
    'conocimientos_clave': ['kyc', 'aml', 'pagos transfronterizos', 'fintech', 'crypto', 'blockchain', 'compliance'],
    'roles_preferidos': ['sales', 'ventas', 'comercial', 'account', 'business development', 'bd', 'hunter', 'representative', 'growth', 'partnership', 'partner', 'ae', 'sdr', 'bdr', 'vendedor', 'acquisition', 'merchant', 'director', 'manager', 'lead'],
    'segmentos_preferidos': ['b2b', 'pyme', 'enterprise', 'latam', 'mexico'],
    'ubicacion_preferida': ['cancun', 'remoto', 'remote', 'mexico', 'latam', 'worldwide', 'global', 'americas', 'flexible'],
    'herramientas_bonus': ['salesforce', 'pipedrive', 'apollo', 'sales navigator'],
    'anios_experiencia_min': 5
}

# --- Filtro Geográfico Estricto ---
def is_location_compatible(location):
    if not location:
        return True # Si no hay ubicación especificada, la analizamos
        
    loc = location.lower()
    
    # Países y regiones restringidas donde Toño no puede trabajar legalmente desde México
    restricted_geos = [
        'uk', 'london', 'united kingdom', 'europe', 'germany', 'italy', 'portugal', 
        'spain', 'france', 'netherlands', 'sweden', 'belgium', 'emea', 'apac', 
        'usa only', 'us only', 'canada only', 'australia', 'uk only', 'ireland'
    ]
    
    # Si la vacante es restringida y no tiene mención explícita a México/LATAM/Americas, se descarta
    if any(r in loc for r in restricted_geos):
        if 'mexico' not in loc and 'latam' not in loc and 'americas' not in loc:
            return False
            
    # La ubicación debe contener palabras que indiquen compatibilidad regional o global
    allowed_geos = ['mexico', 'latam', 'remoto', 'remote', 'worldwide', 'global', 'anywhere', 'americas', 'cancun', 'flexible']
    if any(a in loc for a in allowed_geos):
        return True
        
    return False

# --- Filtro de Rol Estricto ---
def is_sales_role(title):
    title_lower = title.lower()
    
    # Palabras clave comerciales requeridas
    commercial_keywords = [
        'sales', 'ventas', 'comercial', 'account', 'business development', 'bd', 
        'hunter', 'representative', 'growth', 'partnership', 'partner', 'ae', 
        'sdr', 'bdr', 'vendedor', 'acquisition', 'merchant'
    ]
    
    # Palabras clave excluidas (descartan el puesto)
    excluded_keywords = [
        'engineer', 'engineering', 'developer', 'developers', 'programmer', 
        'architect', 'technical', 'tech lead', 'frontend', 'backend', 'fullstack',
        'qa', 'tester', 'designer', 'diseñador', 'data analyst', 'analista de datos',
        'contable', 'accountant', 'writer', 'escritor', 'assistant', 'asistente',
        'product manager', 'project manager', 'marketing manager', 'operations', 
        'support', 'soporte', 'content', 'hr', 'recursos humanos', 'recruiter', 
        'customer success manager', 'solution architect'
    ]
    
    # 1. Debe tener al menos una palabra clave comercial
    has_commercial = any(re.search(r'\b' + re.escape(kw) + r'\b', title_lower) for kw in commercial_keywords)
    
    # 2. No debe tener palabras clave excluidas
    has_exclusion = any(re.search(r'\b' + re.escape(kw) + r'\b', title_lower) for kw in excluded_keywords)
    
    return has_commercial and not has_exclusion

# --- Lógica de Scoring ---
def calculate_score(job_title, job_description, company, location):
    score = 0
    text_to_analyze = f"{job_title} {job_description} {company} {location}".lower()
    title_lower = job_title.lower()

    def contains_keyword(keyword, text):
        if len(keyword) <= 4 or keyword.isalnum():
            pattern = r'\b' + re.escape(keyword) + r'\b'
            return bool(re.search(pattern, text))
        else:
            return keyword in text

    # Nivel 1: Core Business (Pagos, Fintech, KYC/AML, Adquirencia) - Peso Alto
    core_keywords = USER_PROFILE['experiencia_core'] + USER_PROFILE['conocimientos_clave']
    matched_core = [kw for kw in core_keywords if contains_keyword(kw, text_to_analyze)]
    if matched_core:
        score += 40

    # Nivel 2: Rol Comercial - Peso Alto
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

    # Nivel 5: Ubicación/Modalidad (Prioridad a México y LATAM) - Peso Alto
    if 'mexico' in location.lower() or 'latam' in location.lower() or 'americas' in location.lower():
        score += 25  
    elif any(kw in location.lower() for kw in ['remoto', 'remote', 'worldwide', 'global', 'flexible']):
        score += 10  

    # Bonus por Herramientas Conocidas
    matched_tools = [kw for kw in USER_PROFILE['herramientas_bonus'] if contains_keyword(kw, text_to_analyze)]
    if matched_tools:
        score += 5

    return min(100, max(0, score))

def clean_description(html_content):
    if not html_content:
        return ""
    # Remover HTML con BeautifulSoup
    soup = BeautifulSoup(html_content, "lxml")
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text(separator=" ")
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:200] + "..." if len(text) > 200 else text

# --- Scrapers de APIs ---
def fetch_muse_jobs():
    print("Buscando vacantes de Ventas Remotas en The Muse...")
    jobs = []
    # Consultamos 3 páginas de la API (60 vacantes de ventas remotas de alta calidad)
    for page in range(3):
        url = f"https://www.themuse.com/api/public/jobs?category=Sales&location=Flexible%20%2F%20Remote&page={page}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                results = response.json().get("results", [])
                for job in results:
                    locs = [l.get("name") for l in job.get("locations", []) if l.get("name")]
                    loc_str = ", ".join(locs) if locs else "Remote"
                    jobs.append({
                        "empresa": job.get("company", {}).get("name"),
                        "puesto": job.get("name"),
                        "descripcion": clean_description(job.get("contents", "")),
                        "ubicacion": loc_str,
                        "url": job.get("refs", {}).get("landing_page")
                    })
            time.sleep(1) # Pausa amigable
        except Exception as e:
            print(f"Error al conectar con The Muse en página {page}: {e}")
    return jobs

def fetch_jobicy_jobs():
    print("Buscando vacantes de Ventas en Jobicy...")
    url = "https://jobicy.com/api/v2/remote-jobs?count=100&tag=sales"
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
            print(f"Error en Jobicy ({response.status_code})")
    except Exception as e:
        print(f"Error al conectar con Jobicy: {e}")
    return jobs

def fetch_remotive_jobs():
    print("Buscando vacantes de Ventas (Sales) en Remotive...")
    url = "https://remotive.com/api/remote-jobs?category=sales&limit=100"
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
            print(f"Error en Remotive ({response.status_code})")
    except Exception as e:
        print(f"Error al conectar con Remotive: {e}")
    return jobs

def fetch_all_live_vacancies():
    all_jobs = fetch_muse_jobs()
    time.sleep(2)
    all_jobs += fetch_jobicy_jobs()
    time.sleep(2)
    all_jobs += fetch_remotive_jobs()
        
    print(f"Se obtuvieron {len(all_jobs)} vacantes brutas en total.")
    
    unique_jobs = {job['url']: job for job in all_jobs}.values()
    print(f"Quedaron {len(unique_jobs)} vacantes únicas después de deduplicar.")
    
    processed_jobs = []
    for job in unique_jobs:
        # --- FILTRO 1: GEOGRÁFICO ---
        if not is_location_compatible(job['ubicacion']):
            continue
            
        # --- FILTRO 2: ROL COMERCIAL ESTRICTO ---
        if not is_sales_role(job['puesto']):
            continue
            
        score = calculate_score(job['puesto'], job['descripcion'], job['empresa'], job['ubicacion'])
        
        # Construir justificación dinámica basada en los matches
        justification_parts = []
        text_lower = f"{job['puesto']} {job['descripcion']} {job['empresa']} {job['ubicacion']}".lower()
        
        matched_cores = [kw for kw in USER_PROFILE['experiencia_core'] + USER_PROFILE['conocimientos_clave'] if kw.lower() in text_lower]
        if matched_cores:
            justification_parts.append(f"Sector: Coincide con tu experiencia en {', '.join(matched_cores[:3]).upper()}.")
            
        matched_roles = [kw for kw in USER_PROFILE['roles_preferidos'] if kw.lower() in job['puesto'].lower()]
        if matched_roles:
            justification_parts.append(f"Rol: Posición comercial de {', '.join(matched_roles[:2]).capitalize()}.")
            
        if 'mexico' in job['ubicacion'].lower() or 'latam' in job['ubicacion'].lower() or 'americas' in job['ubicacion'].lower():
            justification_parts.append(f"Ubicación ideal: {job['ubicacion']}.")
        else:
            justification_parts.append("Modalidad: Remoto Global compatible.")
            
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

def update_job_radar():
    new_jobs = fetch_all_live_vacancies()
    
    # Mantener solo vacantes comerciales legítimas con score >= 40%
    relevant_new_jobs = [job for job in new_jobs if job['match_score'] >= 0.40]
    
    all_vacancies_dict = {job['url']: job for job in relevant_new_jobs}
    sorted_vacancies = sorted(list(all_vacancies_dict.values()), key=lambda x: x['match_score'], reverse=True)[:50]

    with open('vacancies.json', 'w', encoding='utf-8') as f:
        json.dump(sorted_vacancies, f, indent=4, ensure_ascii=False)
    
    print(f"Radar actualizado. Se guardaron {len(sorted_vacancies)} vacantes de ventas reales y compatibles.")

if __name__ == "__main__":
    update_job_radar()
