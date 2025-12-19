from django.contrib import admin
from .models import Presupuesto, ItemPresupuesto


class ItemPresupuestoInline(admin.TabularInline):
    model = ItemPresupuesto
    extra = 1
    fields = ['nombre', 'descripcion', 'monto']


@admin.register(Presupuesto)
class PresupuestoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'creado_por', 'fecha_creacion', 'fecha_limite', 'estado', 'periodo', 'get_total']
    list_filter = ['estado', 'periodo', 'fecha_creacion']
    search_fields = ['nombre', 'creado_por__username', 'creado_por__first_name', 'creado_por__last_name']
    date_hierarchy = 'fecha_creacion'
    inlines = [ItemPresupuestoInline]
    readonly_fields = ['fecha_creacion', 'get_total']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'creado_por', 'periodo')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_limite')
        }),
        ('Estado y Total', {
            'fields': ('estado', 'get_total')
        }),
    )
    
    def get_total(self, obj):
        return f"${obj.total:,.2f}"
    get_total.short_description = 'Total'


@admin.register(ItemPresupuesto)
class ItemPresupuestoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'presupuesto', 'monto', 'fecha_creacion']
    list_filter = ['presupuesto', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion', 'presupuesto__nombre']
    date_hierarchy = 'fecha_creacion'
    readonly_fields = ['fecha_creacion']
    
    fieldsets = (
        ('Información del Ítem', {
            'fields': ('presupuesto', 'nombre', 'descripcion')
        }),
        ('Monto y Fecha', {
            'fields': ('monto', 'fecha_creacion')
        }),
    )