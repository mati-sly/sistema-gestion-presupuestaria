# Sistema de Gestión Presupuestaria Integral

## 📋 Descripción del Proyecto

Sistema de gestión financiera integral desarrollado para digitalizar procesos administrativos de pequeñas y medianas empresas. El sistema transforma la gestión manual basada en registros físicos en un sistema automatizado que proporciona control financiero completo, análisis de datos y soporte para la toma de decisiones estratégicas.

## 🎯 Propósito del Sistema

El sistema resuelve problemas comunes en la gestión empresarial como:
- **Ausencia de control de costos reales**: Permite seguimiento detallado de gastos e ingresos
- **Ineficiencias en la gestión de inventarios y finanzas**: Automatiza procesos repetitivos
- **Limitaciones en la proyección de rentabilidad**: Proporciona herramientas de análisis predictivo
- **Toma de decisiones basada en intuición**: Ofrece datos concretos y reportes analíticos
- **Falta de estandarización en procesos administrativos**: Implementa flujos de trabajo estructurados

## 🏗️ Arquitectura del Sistema

### Tecnologías Utilizadas
- **Backend**: Django 4.2+, Python 3.12
- **Base de Datos**: MySQL 8.0
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Gráficos**: Chart.js para visualizaciones financieras
- **Reportes**: ReportLab (PDF), openpyxl (Excel)
- **Validaciones**: Django Forms + JavaScript del lado del cliente
- **Patrón de Diseño**: MVC (Modelo-Vista-Controlador)

### Estructura Técnica por Capas

#### Capa de Presentación (Frontend)
- **HTML5/CSS3/JavaScript**: Estructura, diseño e interactividad base
- **Bootstrap 5**: Framework CSS para interfaces responsivas y modernas
- **Chart.js**: Biblioteca para gráficos y visualizaciones de datos financieros

#### Capa de Aplicación (Django Templates & Views)
- **Templates Django**: Sistema de plantillas para renderizado dinámico
- **Formularios Django**: Validación y procesamiento de datos del usuario
- **Vistas**: Controladores que manejan la lógica de negocio y respuesta HTTP

#### Capa de Framework (Django MVC)
- **Models**: ORM (Object-Relational Mapping) para abstracción de base de datos
- **Views**: Controladores de negocio que procesan requests y retornan responses
- **Templates**: Capa de presentación con lógica mínima de visualización
- **MySQL**: Motor de base de datos relacional para persistencia de datos

#### Capa de Datos (Base de Datos)
- **Tablas normalizadas**: Diseño en tercera forma normal (3NF) para integridad
- **Relaciones ForeignKey**: Conexiones entre entidades principales del sistema
- **Transacciones ACID**: Atomicidad, Consistencia, Aislamiento y Durabilidad

## 📊 Módulos del Sistema

### 1. Módulo de Gestión de Presupuestos

#### Modelos Principales:
- **Presupuesto**: Almacena información de cabecera (nombre, período, estado)
- **ItemPresupuesto**: Elementos individuales dentro de un presupuesto

#### Funcionalidades:
- **Creación y Edición**: Formularios con validación de unicidad de nombres
- **Estados Automáticos**: "Abierto" (editable) y "Cerrado" (solo lectura)
- **Copia Inteligente**: Transferencia de ítems entre presupuestos con manejo de duplicados
- **Cálculos Automáticos**: Totales actualizados en tiempo real
- **Exportación**: Formatos PDF y Excel con diseño profesional

#### Validaciones Implementadas:
- Nombre único por presupuesto
- Fechas límite posteriores a fecha actual
- Montos positivos entre rangos definidos
- Prevención de modificación en presupuestos cerrados

### 2. Módulo de Cuentas por Pagar

#### Modelos Principales:
- **CuentaPorPagar**: Registro de facturas y obligaciones
- **HistorialPago**: Seguimiento de estados y movimientos

#### Funcionalidades:
- **Registro Avanzado**: Captura completa de datos de proveedores
- **Validación RUT**: Algoritmo chileno con formato automático
- **Sistema de Alertas**: Código de colores según proximidad de vencimiento
- **Gestión de Estados**: Pendiente → Pagado/Anulado
- **Filtros Dinámicos**: Por fechas, estados, proveedores
- **Historial Completo**: Auditoría de todos los movimientos

#### Proceso de Flujo:
```
Registro → Validación → Dashboard → Pago/Anulación → Historial
```

### 3. Módulo de Registro de Transacciones

#### Modelos Principales:
- **Transaccion**: Vinculación entre pagos y presupuestos
- **Relaciones**: Transacción → Ítem → Presupuesto

#### Funcionalidades:
- **Vinculación Estricta**: Pagos asociados a ítems de presupuestos cerrados
- **Carga Dinámica**: Selectores dependientes (presupuesto → ítems)
- **Comparativas**: Gráficos de barras presupuestado vs. ejecutado
- **Indicadores Visuales**: Etiquetas de estado (dentro/excedido)
- **Acumulación**: Múltiples transacciones por ítem

#### Análisis Proporcionado:
- Desviaciones por categoría
- Tendencias de gasto
- Proyecciones basadas en ejecución
- Alertas de sobregiro

## 🔐 Sistema de Roles y Permisos

### Rol: Administrador/Propietario
- **Acceso Completo**: CRUD en todos los módulos
- **Cierre de Presupuestos**: Autorización exclusiva
- **Validación Final**: Aprobación de reportes
- **Configuración**: Parámetros del sistema

### Características de Seguridad:
- Autenticación por sesión de Django
- Protección CSRF en todos los formularios
- Validación en servidor y cliente
- Sanitización de entradas contra inyecciones
- Control de acceso basado en estado de registros

## 📈 Características Técnicas Avanzadas

### Base de Datos
- **Normalización**: Hasta 3NF para integridad referencial
- **Índices Optimizados**: Para búsquedas frecuentes
- **Transacciones ACID**: Para operaciones críticas
- **Backup Automático**: Scripts de respaldo programados

### Performance
- **Consultas Optimizadas**: Uso de select_related y prefetch_related
- **Cache de Templates**: Para vistas con alta frecuencia
- **Paginación Inteligente**: Para listas extensas
- **Assets Minificados**: CSS y JavaScript comprimidos

### Escalabilidad
- **Arquitectura Modular**: Apps de Django independientes
- **Configuración por Entorno**: Desarrollo/Producción
- **API REST Ready**: Para futuras integraciones
- **Contenedorización**: Preparado para Docker

## 🛠️ Flujos de Trabajo Principales

### Flujo 1: Ciclo Presupuestario
```
1. Crear Presupuesto (Abierto)
2. Agregar Ítems
3. Validar y Ajustar
4. Cerrar Presupuesto
5. Registrar Transacciones
6. Monitorear Ejecución
7. Generar Reportes
```

### Flujo 2: Gestión de Proveedores
```
1. Registrar Factura
2. Validar Datos (RUT, montos, fechas)
3. Priorizar por Vencimiento
4. Ejecutar Pago
5. Actualizar Estados
6. Archivar Comprobantes
```

### Flujo 3: Análisis Financiero
```
1. Consolidar Datos
2. Calcular Métricas
3. Generar Visualizaciones
4. Identificar Tendencias
5. Producir Reportes
6. Sugerir Ajustes
```

## 📋 Especificaciones Técnicas

### Requisitos del Sistema
- **Python**: 3.8 o superior
- **Django**: 4.2+
- **MySQL**: 5.7+ o MariaDB 10.3+
- **Navegador**: Chrome 80+, Firefox 75+, Safari 13+
- **RAM**: 2 GB mínimo (4 GB recomendado)
- **Espacio Disco**: 500 MB para aplicación + datos

### Estándares de Código
- **PEP 8**: Estilo de código Python
- **Convenciones Django**: Apps, modelos, vistas
- **HTML5 Semántico**: Etiquetas con significado
- **CSS BEM**: Metodología de nomenclatura
- **JavaScript ES6+**: Funciones arrow, async/await

## 🚀 Metodología de Desarrollo

### Enfoque Utilizado
- **Metodología Ágil**: Scrum con sprints de 2 semanas
- **AUP (Agile Unified Process)**: Para gestión de proyecto
- **POO (Programación Orientada a Objetos)**: Para diseño de software
- **Patrones de Diseño**: GRASP, GOF, SOLID

### Control de Calidad
- **Testing**: Unit tests para modelos y vistas
- **Validación**: Formularios Django + JavaScript
- **Code Review**: Revisión por pares obligatoria
- **Documentación**: Inline comments + documentación técnica

## 📊 Métricas y KPI del Sistema

### Indicadores Generados
- **Ejecución Presupuestaria**: % cumplimiento por categoría
- **Flujo de Caja**: Proyecciones basadas en vencimientos
- **Análisis de Proveedores**: Frecuencia y montos
- **Tendencias**: Comparativas históricas
- **Alertas**: Desviaciones significativas

### Reportes Automatizados
- **Ejecutivo**: Resumen para toma de decisiones
- **Operativo**: Detalle para gestión diaria
- **Legal**: Para requerimientos fiscales
- **Personalizado**: Filtros y segmentaciones ad-hoc

## 🔄 Mantenimiento y Soporte

### Tipos de Mantenimiento
- **Correctivo**: Corrección de errores críticos
- **Adaptativo**: Ajustes a cambios normativos
- **Perfectivo**: Mejoras de funcionalidad
- **Preventivo**: Optimizaciones proactivas

### SLA (Acuerdos de Nivel de Servicio)
- **Crítico**: Respuesta < 1 hora, Resolución < 4 horas
- **Alto**: Respuesta < 4 horas, Resolución < 24 horas
- **Medio**: Respuesta < 8 horas, Resolución < 3 días
- **Bajo**: Respuesta < 24 horas, Resolución < 5 días

## 📚 Documentación Adicional

### Incluida en el Proyecto
- **Documento de Arquitectura**: Decisiones técnicas y diagramas
- **Manual de Usuario**: Guías paso a paso por módulo
- **API Documentation**: Endpoints para integraciones futuras
- **Guía de Despliegue**: Instrucciones para producción
- **Plan de Mantenimiento**: Procedimientos de soporte

### Diagramas Generados
- **Modelo de Datos**: Entidades y relaciones
- **Diagramas de Flujo**: Procesos empresariales
- **Arquitectura de Software**: Componentes y capas
- **Wireframes**: Diseño de interfaces

## 💡 Casos de Uso Clave

### 1. Planificación Financiera Anual
- Definición de presupuestos por departamento
- Asignación de recursos según objetivos estratégicos
- Establecimiento de límites de gasto por categoría
- Programación de revisiones periódicas

### 2. Control de Gastos Operativos
- Seguimiento diario de desembolsos
- Validación de facturas de proveedores
- Conciliación bancaria automatizada
- Detección de anomalías en tiempo real

### 3. Análisis de Rentabilidad
- Cálculo de márgenes por producto/servicio
- Identificación de áreas de mejora
- Optimización de costos operativos
- Proyecciones de crecimiento basadas en datos históricos

## 🔧 Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior instalado
- MySQL 5.7+ configurado y funcionando
- Git para clonar el repositorio
- Entorno virtual Python configurado

### Pasos de Instalación
1. Clonar el repositorio
2. Crear y activar entorno virtual
3. Instalar dependencias con pip
4. Configurar variables de entorno
5. Ejecutar migraciones de base de datos
6. Crear superusuario administrativo
7. Ejecutar servidor de desarrollo

### Configuración de Producción
- Configuración de base de datos optimizada
- Servidor WSGI (Gunicorn)
- Proxy inverso (Nginx)
- Configuración de seguridad HTTPS
- Backup automático de datos

## 🤝 Contribución al Proyecto

### Directrices para Contribuyentes
1. Crear fork del repositorio
2. Desarrollar en ramas feature separadas
3. Seguir convenciones de código establecidas
4. Escribir tests para nuevas funcionalidades
5. Documentar cambios y mejoras
6. Enviar pull request con descripción detallada

### Estructura de Commits
- feat: Nueva funcionalidad
- fix: Corrección de errores
- docs: Cambios en documentación
- style: Cambios de formato
- refactor: Reestructuración de código
- test: Adición o modificación de tests

## 📞 Soporte y Contacto

### Canales de Soporte
- Issues en GitHub para reportar bugs
- Wiki del proyecto para documentación
- Foro de discusión para preguntas generales
- Correo electrónico para soporte prioritario

### Política de Actualizaciones
- Actualizaciones de seguridad: Inmediatas
- Mejoras de funcionalidad: Mensuales
- Actualizaciones mayores: Trimestrales
- Soporte para versiones: 12 meses desde lanzamiento

---

## 👥 Equipo de Desarrollo

**Rol Scrum**: Desarrollo y Testing
- **Programador**: Desarrollo de funcionalidades principales
- **Ingeniero en Jefe**: Arquitectura y decisiones técnicas
- **Tester**: Control de calidad y validación

**Rol de Gestión**:
- **Scrum Master**: Metodología y seguimiento
- **Product Owner**: Definición de requerimientos

---

*Sistema desarrollado como proyecto integral de gestión empresarial, implementando mejores prácticas de desarrollo de software y metodologías ágiles. Diseñado para ser escalable, mantenible y adaptable a las necesidades cambiantes del entorno empresarial.*