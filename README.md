# Fintech Job Radar 🚀

**Motor de búsqueda autónomo de vacantes para Antonio Gutiérrez Jiménez**

Un sistema inteligente que busca, califica y actualiza automáticamente las mejores oportunidades de empleo en Fintech y Pagos, enfocadas en tu perfil profesional.

---

## 🎯 ¿Qué es?

**Fintech Job Radar** es un motor de búsqueda personalizado que:

- **Busca automáticamente** vacantes en portales de empleo especializados en Fintech y Pagos.
- **Califica cada vacante** según tu perfil (experiencia en Fiserv, Clip, KYC/AML, Pagos, etc.).
- **Se actualiza diariamente** sin que tengas que hacer nada.
- **Muestra un ranking** de las mejores oportunidades en un sitio web interactivo.

---

## 📊 Perfil de Evaluación

El motor evalúa cada vacante basándose en:

| Criterio | Peso | Ejemplos |
| --- | --- | --- |
| **Core Business** | +40 pts | Pagos, Fintech, KYC/AML, Adquirencia |
| **Rol Comercial** | +30 pts | Sales, Ventas, Account Manager, BD Manager |
| **Segmento** | +15 pts | B2B, PyME, Enterprise, LATAM |
| **Tecnología** | +10 pts | SaaS, Software, Plataformas |
| **Ubicación** | +5 pts | Remoto, México, LATAM |
| **Herramientas Bonus** | +5 pts | Salesforce, Pipedrive, Apollo |

---

## 🛠️ Estructura del Proyecto

```
job-radar-tono/
├── engine.py                    # Motor de búsqueda y scoring
├── vacancies.json               # Base de datos de vacantes (se actualiza automáticamente)
├── index.html                   # Interfaz web del radar
├── vercel.json                  # Configuración para Vercel
├── .github/
│   └── workflows/
│       └── update_radar.yml     # GitHub Actions para automatización diaria
└── README.md                    # Este archivo
```

---

## 🚀 Instalación y Configuración

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/agutierrez11/job-radar-tono.git
cd job-radar-tono
```

### Paso 2: Instalar Dependencias

```bash
pip install pandas requests beautifulsoup4
```

### Paso 3: Ejecutar el Motor Manualmente (Opcional)

```bash
python engine.py
```

Esto actualizará `vacancies.json` con las últimas vacantes encontradas.

### Paso 4: Desplegar en Vercel

1. Ve a [vercel.com](https://vercel.com)
2. Importa tu repositorio `job-radar-tono`
3. Vercel detectará automáticamente que es un sitio estático
4. ¡Listo! Tu radar estará en vivo en una URL como `job-radar-tono.vercel.app`

---

## ⚙️ Automatización Diaria

El archivo `.github/workflows/update_radar.yml` configura GitHub Actions para:

- **Ejecutar el motor** automáticamente cada día a las 12:00 PM UTC
- **Buscar nuevas vacantes** en portales especializados
- **Actualizar `vacancies.json`** con los resultados
- **Hacer un commit automático** con los cambios

**No requiere configuración adicional.** GitHub Actions se ejecutará automáticamente.

---

## 📱 Interfaz Web

La interfaz (`index.html`) muestra:

- **Tarjetas de vacantes** con información completa
- **Score de coincidencia** (0-100%) en cada vacante
- **Justificación** de por qué cada vacante es un match
- **Buscador en tiempo real** para filtrar por empresa o cargo
- **Estadísticas** de vacantes activas y top matches
- **Última actualización** del radar

---

## 📝 Estructura del JSON

Cada vacante en `vacancies.json` tiene esta estructura:

```json
{
  "empresa": "Binance",
  "puesto": "Institutional Sales Manager (LATAM)",
  "match_score": 0.96,
  "url": "https://www.binance.com/es/careers",
  "ubicacion": "Remote - LATAM",
  "justificacion": "Gestión de relaciones con clientes institucionales e impulso de ventas de productos cripto de Binance a grandes instituciones financieras en LATAM."
}
```

---

## 🔧 Personalización

### Modificar el Perfil

Edita `engine.py` y actualiza el diccionario `USER_PROFILE`:

```python
USER_PROFILE = {
    'experiencia_core': ['fiserv', 'clip', 'adquirencia', 'pos', 'pagos digitales'],
    'conocimientos_clave': ['kyc', 'aml', 'pagos transfronterizos', 'fintech'],
    'roles_preferidos': ['sales', 'ventas', 'comercial', 'account', 'business development'],
    'segmentos_preferidos': ['b2b', 'pyme', 'enterprise', 'latam', 'mexico'],
    'ubicacion_preferida': ['cancun', 'remoto', 'remote', 'mexico'],
    'herramientas_bonus': ['salesforce', 'pipedrive', 'apollo', 'sales navigator'],
    'anios_experiencia_min': 5
}
```

### Cambiar la Hora de Ejecución

Edita `.github/workflows/update_radar.yml` y modifica el `cron`:

```yaml
schedule:
  - cron: '0 12 * * *'  # Cambiar a tu hora preferida
```

---

## 📊 Próximos Pasos

Para mejorar el radar, puedes:

1. **Integrar scrapers reales** para LinkedIn, Indeed, Glassdoor, etc.
2. **Añadir notificaciones** por email cuando se encuentren vacantes con score > 90%
3. **Crear un dashboard** con gráficos de tendencias
4. **Integrar APIs** de portales de empleo para datos en tiempo real

---

## 📞 Soporte

Si tienes preguntas o necesitas ajustes, contacta a **Antonio Gutiérrez** o abre un issue en el repositorio.

---

## 📄 Licencia

Este proyecto es de uso personal. Todos los derechos reservados.

---

**Última actualización:** Junio 2026  
**Versión:** 1.0.0 (Beta)
