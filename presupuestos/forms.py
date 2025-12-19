from django import forms
# Aseguramos la importación del nuevo modelo Transaccion
from .models import (
    Presupuesto, 
    ItemPresupuesto, 
    CuentaPorPagar, 
    HistorialPago, 
    Transaccion # AGREGADO
)
import re # AGREGADO para validación de RUT
from decimal import Decimal
from datetime import date, timedelta
from django.contrib.auth.models import User

# --- FORMULARIOS DE PRESUPUESTO Y ITEM (Se mantienen) ---

class PresupuestoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance_pk = getattr(self.instance, 'pk', None)

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        
        # Validación: no vacío
        if not nombre or not nombre.strip():
            raise forms.ValidationError("El nombre del presupuesto es obligatorio.")
        
        nombre = nombre.strip()
        
        # Validación: máximo 50 caracteres
        if len(nombre) > 50:
            raise forms.ValidationError("El nombre no puede exceder los 50 caracteres.")
        
        # Validación: nombre único sin importar mayúsculas/minúsculas, excluyendo la instancia actual
        queryset = Presupuesto.objects.filter(nombre__iexact=nombre)
        
        # Si estamos editando, excluir el presupuesto actual
        if self.instance_pk:
            queryset = queryset.exclude(pk=self.instance_pk)
        
        if queryset.exists():
            raise forms.ValidationError("Ya existe un presupuesto con ese nombre.")
        
        return nombre

    def clean_fecha_limite(self):
        # A diferencia de CuentaPorPagar, mantenemos la restricción para Presupuesto
        fecha_limite = self.cleaned_data.get('fecha_limite')
        if fecha_limite and fecha_limite <= date.today():
            raise forms.ValidationError('La fecha límite debe ser posterior al día de hoy.')
        return fecha_limite

    class Meta:
        model = Presupuesto
        fields = ['nombre', 'creado_por', 'fecha_limite', 'periodo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej: Presupuesto Enero 2026',
                'maxlength': '50'  # Agregar maxlength para validación HTML
            }),
            'creado_por': forms.Select(attrs={
                'class': 'form-input'
            }),
            'fecha_limite': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
                'min': (date.today() + timedelta(days=1)).isoformat()  # Mínimo mañana
            }),
            'periodo': forms.Select(attrs={
                'class': 'form-input'
            }),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.pk:
            instance.estado = 'abierto'
        if commit:
            instance.save()
        return instance

class ItemPresupuestoForm(forms.ModelForm):
    class Meta:
        model = ItemPresupuesto
        fields = ['nombre', 'descripcion', 'monto']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nombre del ítem',
                'required': True
            }),
            'descripcion': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Descripción del ítem'
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '10000',
                'max': '10000000',
                'placeholder': 'Monto entre $10.000 y $10.000.000',
                'required': True
            }),
        }
        
    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto and monto < Decimal('10000'):
            raise forms.ValidationError('El monto debe ser al menos $10.000')
        if monto and monto > Decimal('10000000'):
            raise forms.ValidationError('El monto no puede exceder $10.000.000')
        return monto


class PresupuestoFilterForm(forms.Form):
    # Formulario de filtro (Se mantiene)
    estado = forms.ChoiceField(
        choices=[('', '-- Todos --'), ('abierto', 'Abiertos'), ('cerrado', 'Cerrados')],
        required=False,
        widget=forms.Select(attrs={'class': 'filter-select'})
    )
    buscar = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'type': 'search',
            'placeholder': 'Nombre o Período...'
        })
    )


# -----------------------------------------------------
# 1. NUEVO FORMULARIO: TransaccionForm
# -----------------------------------------------------

class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        # No se incluye presupuesto ni usuario, se asignan en la vista
        fields = ['item_presupuesto', 'monto', 'metodo_pago', 'referencia', 'fecha_pago', 'observaciones']
        widgets = {
            'fecha_pago': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-input'}),
            'monto': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-input'}),
            'item_presupuesto': forms.Select(attrs={'class': 'form-input'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-input'}),
            'referencia': forms.TextInput(attrs={'class': 'form-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        # Captura el ID del presupuesto para filtrar los ítems
        presupuesto_id = kwargs.pop('presupuesto_id', None)
        super().__init__(*args, **kwargs)
        
        if presupuesto_id:
            # Solo mostrar ítems del presupuesto específico
            self.fields['item_presupuesto'].queryset = ItemPresupuesto.objects.filter(
                presupuesto_id=presupuesto_id
            )
            self.fields['item_presupuesto'].empty_label = "Seleccione un ítem"
            self.fields['item_presupuesto'].required = True

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto and monto <= Decimal('0'):
            raise forms.ValidationError('El monto debe ser mayor a 0.')
        return monto


# -----------------------------------------------------
# 2. CUENTA POR PAGAR FORM (MODIFICADO)
# -----------------------------------------------------

class CuentaPorPagarForm(forms.ModelForm):
    
    # Campo para la fecha de emisión (añadido al Meta y widgets)
    # Campo para el RUT (añadido al Meta y widgets)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance_pk = getattr(self.instance, 'pk', None)
        # ELIMINADO: La configuración de 'creado_por' ya que se eliminó del modelo.
        
    def clean_nombre_proveedor(self):
        nombre = self.cleaned_data.get('nombre_proveedor')
        if len(nombre) > 100:
            raise forms.ValidationError("El nombre del proveedor no puede exceder los 100 caracteres.")
        # La validación Regex ahora se maneja en el modelo
        return nombre

    def clean_rut_proveedor(self):
        rut = self.cleaned_data.get('rut_proveedor')
        # Validación básica de formato RUT chileno
        # Esta validación se duplica con la del modelo, pero asegura un mensaje de error claro en el formulario
        if not re.match(r'^[0-9]{7,8}-[0-9kK]{1}$', rut):
            raise forms.ValidationError("El RUT debe tener el formato 12345678-9 (o 1234567-9)")
        return rut

    def clean_numero_factura(self):
        numero_factura = self.cleaned_data.get('numero_factura')
        queryset = CuentaPorPagar.objects.filter(numero_factura__iexact=numero_factura)
        
        if self.instance_pk:
            queryset = queryset.exclude(pk=self.instance_pk)
        
        if queryset.exists():
            raise forms.ValidationError("Ya existe una cuenta con este número de factura.")
        return numero_factura

    # ELIMINADA: La validación que forzaba a la fecha límite a ser futuro
    def clean_fecha_limite(self):
        fecha_limite = self.cleaned_data.get('fecha_limite')
        # Ahora permitimos cualquier fecha, ya que el modelo lo soporta
        return fecha_limite
        
    def clean_fecha_emision(self):
        fecha_emision = self.cleaned_data.get('fecha_emision')
        # Permitimos cualquier fecha
        return fecha_emision

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto and monto <= Decimal('0'):
            raise forms.ValidationError('El monto debe ser mayor a 0.')
        return monto

    class Meta:
        model = CuentaPorPagar
        fields = [
            'numero_factura', 
            'nombre_proveedor', 
            'rut_proveedor',       # CAMPO NUEVO
            'fecha_emision',       # CAMPO NUEVO
            'descripcion', 
            'monto', 
            'fecha_limite',
            'observaciones',
            # ELIMINADO: 'creado_por' (fue retirado del modelo)
        ]
        widgets = {
            'numero_factura': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ej: F001-2024'
            }),
            'nombre_proveedor': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nombre del proveedor'
            }),
            'rut_proveedor': forms.TextInput(attrs={ # WIDGET NUEVO
                'class': 'form-input',
                'placeholder': 'Ej: 12345678-9'
            }),
            'fecha_emision': forms.DateInput(attrs={ # WIDGET NUEVO
                'class': 'form-input',
                'type': 'date',
                'placeholder': 'Fecha de Emisión'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                'placeholder': 'Descripción de la cuenta por pagar'
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0.01',
                'step': '0.01',
                'placeholder': 'Monto a pagar'
            }),
            'fecha_limite': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
                # ELIMINADO: 'min' para permitir cualquier fecha
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                'placeholder': 'Observaciones adicionales'
            }),
            # ELIMINADO: 'creado_por' widget
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.pk:
            instance.estado = 'pendiente'
        if commit:
            instance.save()
        return instance


# --- FORMULARIOS DE HISTORIAL Y FILTROS (Se mantienen) ---

class HistorialPagoForm(forms.ModelForm):
    def clean_monto_pagado(self):
        monto_pagado = self.cleaned_data.get('monto_pagado')
        if monto_pagado and monto_pagado <= Decimal('0'):
            raise forms.ValidationError('El monto pagado debe ser mayor a 0.')
        return monto_pagado

    class Meta:
        model = HistorialPago
        fields = ['monto_pagado', 'metodo_pago', 'referencia', 'observaciones']
        widgets = {
            'monto_pagado': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': '0.01',
                'step': '0.01',
                'placeholder': 'Monto pagado'
            }),
            'metodo_pago': forms.Select(attrs={
                'class': 'form-input'
            }),
            'referencia': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Número de referencia o transacción'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                'placeholder': 'Observaciones del pago'
            }),
        }


class CuentasPorPagarFilterForm(forms.Form):
    ESTADO_CHOICES = [
        ('', 'Todos los estados'),
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('anulado', 'Anulado'),
    ]
    
    estado = forms.ChoiceField(
        choices=ESTADO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'filter-select'})
    )
    buscar = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'type': 'search',
            'placeholder': 'Proveedor o N° Factura...'
        })
    )
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-input',
            'type': 'date',
            'placeholder': 'Desde...'
        })
    )
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-input',
            'type': 'date',
            'placeholder': 'Hasta...'
        })
    )


class HistorialPagoFilterForm(forms.Form):
    ESTADO_CHOICES = [
        ('', 'Todos los estados'),
        ('pagado', 'Pagado'),
        ('anulado', 'Anulado'),
    ]
    
    estado = forms.ChoiceField(
        choices=ESTADO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'filter-select'})
    )
    buscar = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'type': 'search',
            'placeholder': 'Proveedor o N° Factura...'
        })
    )