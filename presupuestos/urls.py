from django.urls import path
from . import views

app_name = 'presupuestos'

urlpatterns = [
    # ==================== PRESUPUESTOS ====================
    # URLs existentes
    path('', views.lista_presupuestos, name='lista'),
    path('crear/', views.crear_presupuesto, name='crear'),
    path('<int:pk>/', views.detalle_presupuesto, name='detalle'),
    path('<int:pk>/editar/', views.editar_presupuesto, name='editar'),
    
    # Items
    path('<int:pk>/agregar-item/', views.agregar_item, name='agregar_item'),
    path('<int:pk>/editar-item/<int:item_id>/', views.editar_item, name='editar_item'),
    path('<int:pk>/eliminar-item/<int:item_id>/', views.eliminar_item, name='eliminar_item'),
    
    # ==================== COMPARAR PRESUPUESTO (NUEVO) ====================
    # AÑADE ESTAS 2 LÍNEAS:
    path('comparar-presupuesto/', views.comparar_presupuesto, name='comparar_presupuesto'),
    path('api/comparar-presupuesto/<int:presupuesto_id>/', views.api_comparar_presupuesto, name='api_comparar_presupuesto'),
    
    # ==================== TRANSACCIONES (NUEVO MÓDULO) ====================
    # Transacciones dentro de presupuesto específico
    path('<int:pk>/transacciones/', views.lista_transacciones, name='lista_transacciones'),
    path('<int:pk>/transacciones/registrar/', views.registrar_transaccion, name='registrar_transaccion'),
    
    # Módulo completo de transacciones (INDEPENDIENTE)
    path('transacciones/', views.lista_transacciones_completa, name='lista_transacciones_completa'),
    path('transacciones/nueva/', views.crear_transaccion_general, name='crear_transaccion_general'),
    
    # NUEVA URL: Formulario simple específico
    path('transacciones/registrar-pago/', views.crear_transaccion_simple, name='crear_transaccion_simple'),
    
    path('transacciones/<int:pk>/editar/', views.editar_transaccion_completa, name='editar_transaccion_completa'),
    path('transacciones/<int:pk>/detalle/', views.detalle_transaccion_completa, name='detalle_transaccion_completa'),
    path('transacciones/<int:pk>/eliminar/', views.eliminar_transaccion_completa, name='eliminar_transaccion_completa'),
    
    # API endpoints para AJAX
    path('api/presupuestos-cerrados/', views.api_presupuestos_cerrados, name='api_presupuestos_cerrados'),
    path('api/items-presupuesto/<int:presupuesto_id>/', views.api_items_presupuesto, name='api_items_presupuesto'),
    path('api/saldo-disponible/<int:item_id>/', views.api_saldo_disponible, name='api_saldo_disponible'),
    
    # Exportación de transacciones
    path('transacciones/exportar-excel/', views.exportar_transacciones_excel, name='exportar_transacciones_excel'),
    path('transacciones/exportar-pdf/', views.exportar_transacciones_pdf, name='exportar_transacciones_pdf'),
    
    # ==================== OTRAS FUNCIONALIDADES DE PRESUPUESTO ====================
    path('<int:pk>/copiar-items/', views.copiar_items, name='copiar_items'),
    path('<int:pk>/copiar-presupuesto/', views.copiar_presupuesto, name='copiar_presupuesto'),
    
    # Acciones presupuesto
    path('<int:pk>/cerrar/', views.cerrar_presupuesto, name='cerrar'),
    path('<int:pk>/eliminar/', views.eliminar_presupuesto, name='eliminar'),
    
    # Exportar presupuestos
    path('exportar/excel/', views.exportar_excel, name='exportar_excel'),
    path('exportar/pdf/', views.exportar_pdf, name='exportar_pdf'),
    path('<int:pk>/exportar-items/excel/', views.exportar_items_excel, name='exportar_items_excel'),
    path('<int:pk>/exportar-items/pdf/', views.exportar_items_pdf, name='exportar_items_pdf'),
    
    # ==================== DASHBOARD ====================
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # ==================== CUENTAS POR PAGAR ====================
    # URLs MÁS ESPECÍFICAS PRIMERO
    path('cuentas-por-pagar/crear/', views.crear_cuenta_por_pagar, name='crear_cuenta'),
    path('cuentas-por-pagar/historial/', views.historial_pagos, name='historial_pagos'),
    
    # NUEVAS URLs PARA EXPORTAR HISTORIAL
    path('cuentas-por-pagar/historial/exportar-excel/', views.exportar_historial_excel, name='exportar_historial_excel'),
    path('cuentas-por-pagar/historial/exportar-pdf/', views.exportar_historial_pdf, name='exportar_historial_pdf'),
    
    path('cuentas-por-pagar/exportar/excel/', views.exportar_cuentas_excel, name='exportar_cuentas_excel'),
    path('cuentas-por-pagar/exportar/pdf/', views.exportar_cuentas_pdf, name='exportar_cuentas_pdf'),
    
    # URLs con parámetros DESPUÉS
    path('cuentas-por-pagar/<int:pk>/registrar-pago/', views.registrar_pago, name='registrar_pago'),
    path('cuentas-por-pagar/<int:pk>/anular/', views.anular_cuenta, name='anular_cuenta'),
    path('cuentas-por-pagar/<int:pk>/eliminar/', views.eliminar_cuenta_por_pagar, name='eliminar_cuenta'),
    
    # URL de detalle ANTES de la lista
    path('cuentas-por-pagar/<int:pk>/', views.detalle_cuenta_por_pagar, name='detalle_cuenta'),
    
    # URL de lista AL FINAL (menos específica)
    path('cuentas-por-pagar/', views.lista_cuentas_por_pagar, name='lista_cuentas'),
]