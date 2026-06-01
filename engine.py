import json
import pandas as pd
from datetime import datetime

# --- Configuración del Perfil de Toño ---
# Ajustado según las últimas conversaciones
USER_PROFILE = {
    'experiencia_core': ['fiserv', 'clip', 'adquirencia', 'pos', 'pagos digitales'],
    'conocimientos_clave': ['kyc', 'aml', 'pagos transfronterizos', 'fintech'],
    'roles_preferidos': ['sales', 'ventas', 'comercial', 'account', 'business development', 'bd manager', 'hunter', 'director', 'lider'],
    'segmentos_preferidos': ['b2b', 'pyme', 'enterprise', 'latam', 'mexico'],
    'ubicacion_preferida': ['cancun', 'remoto', 'remote', 'mexico'],
    'herramientas_bonus': ['salesforce', 'pipedrive', 'apollo', 'sales navigator'],
    'anios_experiencia_min': 5 # Ajustado a tu nivel de experiencia
}

# --- Lógica de Scoring (Ajustada y Mejorada) ---
def calculate_score(job_title, job_description, company, location, url):
    score = 0
    text_to_analyze = (job_title + " " + job_description + " " + company + " " + location).lower()

    # Nivel 1: Core Business (Pagos, Fintech, KYC/AML, Adquirencia) - Peso Alto
    if any(keyword in text_to_analyze for keyword in USER_PROFILE['experiencia_core'] + USER_PROFILE['conocimientos_clave']):
        score += 40

    # Nivel 2: Rol Específico (Ventas, BD, Account Management) - Peso Alto
    if any(keyword in job_title.lower() for keyword in USER_PROFILE['roles_preferidos']):
        score += 30

    # Nivel 3: Segmento (B2B, LATAM, Enterprise) - Peso Medio
    if any(keyword in text_to_analyze for keyword in USER_PROFILE['segmentos_preferidos']):
        score += 15

    # Nivel 4: Tecnología/SaaS - Peso Medio
    if 'saas' in text_to_analyze or 'software' in text_to_analyze or 'tech' in text_to_analyze:
        score += 10

    # Nivel 5: Ubicación/Modalidad (Prioridad Remoto/México/LATAM) - Peso Bajo
    if any(keyword in location.lower() for keyword in USER_PROFILE['ubicacion_preferida']):
        score += 5

    # Bonus por Herramientas Conocidas
    if any(tool in text_to_analyze for tool in USER_PROFILE['herramientas_bonus']):
        score += 5 # Pequeño bonus por herramientas que ya dominas

    # Penalización por roles puramente técnicos o junior
    if any(keyword in job_title.lower() for keyword in ['engineer', 'developer', 'contable', 'analista de datos', 'junior', 'entry level']):
        score -= 20 # Penalización moderada

    # Asegurar que el score no sea negativo
    return max(0, score)

# --- Función para simular la búsqueda de vacantes (Aquí iría el scraping real) ---
def fetch_new_vacancies():
    # En una implementación real, aquí se integrarían los scrapers para LinkedIn, Indeed, etc.
    # Por ahora, usamos una lista de ejemplo para demostrar el scoring.
    print("Simulando la búsqueda de nuevas vacantes...")
    new_jobs_data = [
        {
            "empresa": "Stripe",
            "puesto": "Sales Lead, LATAM",
            "descripcion": "Drive revenue growth for Stripe in Latin America, focusing on enterprise clients and payment solutions.",
            "ubicacion": "Remote - LATAM",
            "url": "https://stripe.com/careers/sales-lead-latam"
        },
        {
            "empresa": "Adyen",
            "puesto": "Account Executive, Mexico",
            "descripcion": "Manage a portfolio of key enterprise accounts in Mexico, selling Adyen's payment platform.",
            "ubicacion": "Mexico City, Mexico (Hybrid)",
            "url": "https://adyen.com/careers/account-executive-mexico"
        },
        {
            "empresa": "Ebanx",
            "puesto": "Business Development Manager, Cross-Border Payments",
            "descripcion": "Identify and close new business opportunities for cross-border payment solutions in LATAM. Experience with KYC/AML a plus.",
            "ubicacion": "Remote - Brazil (LATAM)",
            "url": "https://ebanx.com/careers/bd-manager"
        },
        {
            "empresa": "Nuvei",
            "puesto": "VP, Solutions and Implementations (Americas)",
            "descripcion": "Lead the solutions and implementation team for payment processing across the Americas. Strong B2B experience required.",
            "ubicacion": "Remote - Americas",
            "url": "https://nuvei.com/careers/vp-solutions"
        },
        {
            "empresa": "Rapyd",
            "puesto": "Commercial Director (LATAM)",
            "descripcion": "Oversee commercial strategy and drive sales for Rapyd's Fintech-as-a-Service platform in Latin America.",
            "ubicacion": "Remote - LATAM",
            "url": "https://rapyd.net/careers/commercial-director-latam"
        },
        {
            "empresa": "Bitso",
            "puesto": "General Manager (Bitso Business)",
            "descripcion": "Lead Bitso Business operations, focusing on crypto payment solutions for B2B clients in Mexico.",
            "ubicacion": "Mexico (Remote)",
            "url": "https://bitso.com/careers/general-manager"
        },
        {
            "empresa": "OKX",
            "puesto": "Principal Product Manager (Growth - LATAM)",
            "descripcion": "Define product strategy for growth initiatives in Latin America, focusing on crypto and fintech products.",
            "ubicacion": "Remote - LATAM",
            "url": "https://okx.com/careers/product-manager"
        },
        {
            "empresa": "Binance",
            "puesto": "Institutional Sales Manager (LATAM)",
            "descripcion": "Manage institutional client relationships and drive sales of Binance's crypto products to large financial institutions in LATAM.",
            "ubicacion": "Remote - LATAM",
            "url": "https://binance.com/es/careers/institutional-sales"
        },
        {
            "empresa": "Valutico",
            "puesto": "Account Executive: LATAM",
            "descripcion": "Sell Valutico's AI-powered valuation platform to financial professionals across Latin America. B2B SaaS sales experience required.",
            "ubicacion": "Remote - LATAM",
            "url": "https://jobs.workable.com/view/ePQ6cvqtqVMK4Qyeo65j3a/remote-account-executive%3A-latam-(portuguese-or-spanish-speaking)-in-mexico-at-valutico"
        },
        {
            "empresa": "Sumsub",
            "puesto": "Business Development Manager, Mexico",
            "descripcion": "Drive sales for Sumsub's KYC/AML verification platform in Mexico. Hunter mentality and strong LATAM network required.",
            "ubicacion": "Remote - Mexico",
            "url": "https://careers.sumsub.com/jobs/7068282-business-development-manager-mexico"
        }
    ]
    
    processed_jobs = []
    for job in new_jobs_data:
        score = calculate_score(job['puesto'], job['descripcion'], job['empresa'], job['ubicacion'], job['url'])
        processed_jobs.append({
            "empresa": job["empresa"],
            "puesto": job["puesto"],
            "ubicacion": job["ubicacion"],
            "url": job["url"],
            "match_score": round(score / 100, 2), # Normalizar a 0-1 para el JSON
            "justificacion": f"Score basado en: {job['descripcion'][:50]}..."
        })
    return processed_jobs

# --- Función principal para actualizar el radar ---
def update_job_radar():
    current_vacancies = []
    try:
        with open('vacancies.json', 'r', encoding='utf-8') as f:
            current_vacancies = json.load(f)
    except FileNotFoundError:
        print("vacancies.json no encontrado, creando uno nuevo.")
    except json.JSONDecodeError:
        print("Error al leer vacancies.json, se creará uno nuevo.")

    new_jobs = fetch_new_vacancies()
    updated_vacancies = []
    existing_urls = {v['url'] for v in current_vacancies}

    for job in new_jobs:
        if job['url'] not in existing_urls:
            updated_vacancies.append(job)
        else:
            # Si ya existe, podríamos actualizar el score o la justificación si es necesario
            # Por ahora, simplemente mantenemos la existente si no hay cambios significativos
            pass

    # Combinar y eliminar duplicados (si el scraper trae duplicados)
    all_vacancies = current_vacancies + updated_vacancies
    unique_vacancies = {v['url']: v for v in all_vacancies}.values()

    # Ordenar por score de mayor a menor
    sorted_vacancies = sorted(list(unique_vacancies), key=lambda x: x['match_score'], reverse=True)

    with open('vacancies.json', 'w', encoding='utf-8') as f:
        json.dump(sorted_vacancies, f, indent=4, ensure_ascii=False)
    
    print(f"Radar actualizado. Se añadieron {len(updated_vacancies)} nuevas vacantes. Total: {len(sorted_vacancies)}.")

if __name__ == "__main__":
    update_job_radar()
