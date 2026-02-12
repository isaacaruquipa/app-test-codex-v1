# Sistema Integral de Gestión de Chismes (SIGC)

Plataforma de nueva generación para **captura, análisis, verificación, moderación y aprendizaje** de chismes con enfoque:

- **Holístico:** combina señales sociales, lingüísticas, temporales y de red.
- **Interdisciplinar:** integra comunicación, sociología, analítica de datos, ética y gobernanza.
- **Ultra avanzado:** priorización automatizada, trazabilidad, score de confianza, gestión de riesgos y recomendaciones de acción.

## Capacidades clave

1. **Ingesta multicanal**
   - Mensajería interna, formularios, reportes de terceros, notas de analistas.
   - Normalización del texto y metadatos.

2. **Perfilado dinámico de fuentes**
   - Historial de precisión.
   - Sensibilidad temática.
   - Penalización por ruido o sesgo sistemático.

3. **Evaluación probabilística de chismes**
   - Score de credibilidad por evidencia.
   - Ajuste por calidad de fuentes.
   - Penalización por carga emocional extrema (señal de posible distorsión).

4. **Motor de riesgo integral**
   - Riesgo reputacional.
   - Riesgo de daño interpersonal.
   - Riesgo legal/compliance.

5. **Workflow inteligente**
   - Derivación automática a observación, verificación manual o escalado crítico.
   - Recomendaciones accionables.

6. **Gobernanza ética y explicabilidad**
   - Toda decisión es auditable.
   - Justificación textual de score y acción.
   - Política configurable.

## Arquitectura propuesta

- **Capa de Captura:** APIs, conectores y formularios.
- **Capa de Inteligencia:** scoring de credibilidad, análisis semántico, priorización.
- **Capa de Decisión:** reglas + políticas + flujos de revisión humana.
- **Capa de Aprendizaje:** retroalimentación y recalibración de perfiles.
- **Capa de Gobierno:** auditoría, privacidad, retención y cumplimiento.

## Implementación incluida en este repositorio

Este repositorio incluye un **MVP funcional** en Python con:

- Modelo de `GossipReport` y `SourceProfile`.
- `ChismeIntelligenceEngine` para:
  - score de credibilidad,
  - score de riesgo,
  - clasificación de severidad,
  - recomendación de acciones.
- Configuración de políticas mediante YAML.
- Pruebas automáticas.

## Ejecución rápida

```bash
python -m pytest -q
```

## Siguientes extensiones de vanguardia

- Integración con embeddings y detección semántica de contradicciones.
- Grafo de propagación de rumores.
- Simulación de impacto reputacional por escenarios.
- Panel de control con monitoreo en tiempo real.
- Agentes de investigación colaborativa humano+IA.
