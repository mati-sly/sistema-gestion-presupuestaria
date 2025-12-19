from django.db import models
from django.core.validators import MinValueValidator, RegexValidator # Importado RegexValidator
from django.db.models.functions import Lower
from django.db.models import UniqueConstraint
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone # No es estrictamente necesario si ya se usa date, pero lo mantengo
#from datetime import date # Ya estaba importado, pero lo dejo por claridad

# --- MODELO PRESUPUESTO Y ITEMPRESUPUESTO (Sin Cambios) ---

class Presupuesto(models.Model):
    ESTADO_CHOICES = [
        ('abierto', 'Abierto'),
        ('cerrado', 'Cerrado'),
    ]
    
    PERIODO_CHOICES = [
        ('Mensual', 'Mensual'),
        ('Trimestral', 'Trimestral'),
        ('Semestral', 'Semestral'),
        ('Anual', 'Anual'),
    ]

    nombre = models.CharField(max_length=200, verbose_name='Nombre del Presupuesto')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')

    # Campo creado_por (Mantengo)
    creado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Creado Por'
    )
    
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_limite = models.DateField(verbose_name='Fecha Límite')

    estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default='abierto',
        verbose_name='Estado'
    )
    
    periodo = models.CharField(
        max_length=20,
        choices=PERIODO_CHOICES,
        default='Mensual',
        verbose_name='Período'
    )
    
    class Meta:
        verbose_name = 'Presupuesto'
        verbose_name_plural = 'Presupuestos'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return self.nombre
    
    @property
    def total(self):
        # El total de ítems
        total = self.items.aggregate(models.Sum('monto'))['monto__sum']
        return total or 0
        
    @property
    def total_transacciones(self):
        # Nuevo: Total pagado de todas las transacciones asociadas a este presupuesto
        total_pagado = self.transacciones.aggregate(models.Sum('monto'))['monto__sum']
        return total_pagado or 0

    def puede_modificar(self):
        return self.estado == 'abierto'


class ItemPresupuesto(models.Model):
    presupuesto = models.ForeignKey(
        Presupuesto,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Presupuesto'
    )

    nombre = models.CharField(max_length=200, verbose_name='Nombre del Ítem')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')

    monto = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Monto'
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    
    class Meta:
        verbose_name = 'Ítem de Presupuesto'
        verbose_name_plural = 'Ítems de Presupuesto'
        ordering = ['id']

        constraints = [
            UniqueConstraint(
                Lower('nombre'),
                'presupuesto',
                name='unique_item_nombre_por_presupuesto_ci'
            )
        ]
    
    def __str__(self):
        return f"{self.nombre} - ${self.monto}"

    @property
    def total_transacciones(self):
        # Nuevo: Total pagado de las transacciones asociadas a este ítem
        total_pagado = self.transacciones.aggregate(models.Sum('monto'))['monto__sum']
        return total_pagado or 0
    
# -----------------------------------------------------
# 1. REGISTRO DE TRANSACCIONES (NUEVO MODELO)
# -----------------------------------------------------

class Transaccion(models.Model):
    METODO_PAGO_CHOICES = [
        ('transferencia', 'Transferencia Bancaria'),
        ('efectivo', 'Efectivo'),
        ('cheque', 'Cheque'),
        ('tarjeta', 'Tarjeta de Crédito/Débito'),
        ('otros', 'Otros'),
    ]
    
    # FK al presupuesto general (para listados)
    presupuesto = models.ForeignKey(
        Presupuesto, 
        on_delete=models.CASCADE, 
        related_name='transacciones', 
        verbose_name='Presupuesto'
    )
    
    # FK al ítem específico del presupuesto
    item_presupuesto = models.ForeignKey(
        ItemPresupuesto, 
        on_delete=models.CASCADE, 
        related_name='transacciones', 
        verbose_name='Ítem del Presupuesto'
    )
    
    monto = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Monto Pagado')
    metodo_pago = models.CharField(
        max_length=20, 
        choices=METODO_PAGO_CHOICES, 
        default='transferencia', 
        verbose_name='Método de Pago'
    )
    referencia = models.CharField(max_length=100, blank=True, null=True, verbose_name='Referencia')
    fecha_pago = models.DateField(verbose_name='Fecha de Pago')
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    
    # AJUSTE CRÍTICO: Hacemos el usuario opcional para entornos sin login (null=True, blank=True)
    usuario = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Usuario'
    ) 
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Transacción {self.id} - {self.presupuesto.nombre} - ${self.monto}"
    
    class Meta:
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'
        ordering = ['-fecha_pago']


# -----------------------------------------------------
# 2. CUENTA POR PAGAR (MODIFICACIONES)
# -----------------------------------------------------

# Expresión regular para validar el formato de RUT chileno
# Acepta: 7 u 8 dígitos, guión, y dígito verificador (0-9, k, K)
RUT_VALIDATOR = RegexValidator(
    regex=r'^[0-9]{7,8}-[0-9kK]{1}$',
    message='El RUT debe tener el formato 12345678-9 (o 1234567-9)'
)

# Expresión regular para nombre de proveedor (letras, números, espacios, puntos, guiones, tildes)
NOMBRE_PROVEEDOR_VALIDATOR = RegexValidator(
    regex=r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s\.\-]+$',
    message='El nombre del proveedor solo puede contener letras, números, espacios, puntos y guiones.'
)

from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.db.models.functions import Lower
from django.db.models import UniqueConstraint
from django.contrib.auth.models import User
from datetime import date
from django.core.exceptions import ValidationError  # Importar ValidationError

# ... (otros modelos permanecen igual)

# Expresión regular para nombre de proveedor (letras, números, espacios, puntos, guiones, tildes)
NOMBRE_PROVEEDOR_VALIDATOR = RegexValidator(
    regex=r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s\.\-]+$',
    message='El nombre del proveedor solo puede contener letras, números, espacios, puntos y guiones.'
)

class CuentaPorPagar(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('anulado', 'Anulado'),
    ]
    
    # CAMPO: Número de factura (Se mantiene)
    numero_factura = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name='Número de Factura',
        help_text='Máximo 50 caracteres'  # Agregar help_text para el formulario
    )
    
    # CAMPO MODIFICADO: Aplicación de validadores
    nombre_proveedor = models.CharField(
        max_length=100, # Reducido a 100 caracteres
        verbose_name='Nombre del Proveedor',
        validators=[NOMBRE_PROVEEDOR_VALIDATOR]
    )
    
    # CAMPO AGREGADO: RUT del Proveedor con validador
    rut_proveedor = models.CharField(
        max_length=12, # Suficiente para el formato 12345678-K
        validators=[RUT_VALIDATOR],
        verbose_name='RUT Proveedor'
    )
    
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    monto = models.IntegerField(
        verbose_name='Monto',
        validators=[MinValueValidator(1)]  # Agregar validador para mínimo 1
    )
    
    # CAMPO AGREGADO: Fecha de Emisión
    fecha_emision = models.DateField(verbose_name='Fecha de Emisión') 
    
    fecha_creacion = models.DateField(auto_now_add=True, verbose_name='Fecha de Registro')
    fecha_limite = models.DateField(verbose_name='Fecha Límite de Pago')
    fecha_pago = models.DateField(null=True, blank=True, verbose_name='Fecha de Pago')
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='pendiente',
        verbose_name='Estado'
    )
    
    observaciones = models.TextField(blank=True, verbose_name='Observaciones')
    
    # Nuevo campo para registro de actualización
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')
    
    class Meta:
        verbose_name = 'Cuenta por Pagar'
        verbose_name_plural = 'Cuentas por Pagar'
        ordering = ['fecha_limite']
    
    def __str__(self):
        return f"Factura {self.numero_factura} - {self.nombre_proveedor}"
    
    def clean(self):
        """Validación personalizada para el modelo"""
        super().clean()
        
        # Validar que el número de factura tenga menos de 50 caracteres
        if len(self.numero_factura) >= 50:
            raise ValidationError({
                'numero_factura': 'El número de factura debe tener menos de 50 caracteres.'
            })
    
    def save(self, *args, **kwargs):
        """Asegurar validaciones antes de guardar"""
        self.full_clean()  # Esto llama a clean() automáticamente
        super().save(*args, **kwargs)
    
    def dias_restantes(self):
        """Calcula los días restantes para el pago"""
        if self.estado in ['pagado', 'anulado']:
            return None
        hoy = date.today()
        dias = (self.fecha_limite - hoy).days
        return dias
    
    def get_color_estado(self):
        """Devuelve el color según los días restantes"""
        dias = self.dias_restantes()
        
        if self.estado in ['pagado', 'anulado'] or dias is None:
            return 'gray'
        elif dias < 0:
            return 'red'      # Vencido
        elif dias <= 1:
            return 'red'      # Hoy vence
        elif dias <= 5:
            return 'orange'   # 1-5 días
        else:
            return 'green'    # 6+ días
    
    def get_estado_display_color(self):
        """Devuelve el color para el badge de estado"""
        if self.estado == 'pagado':
            return 'green'
        elif self.estado == 'anulado':
            return 'gray'
        else:  # pendiente
            return self.get_color_estado()
    
    def puede_modificar(self):
        """Determina si la cuenta puede ser modificada"""
        return self.estado == 'pendiente'

# ... (el resto de los modelos permanece igual)


# -----------------------------------------------------
# 3. HISTORIAL DE PAGO (Sin Cambios)
# -----------------------------------------------------

class HistorialPago(models.Model):
    ESTADO_CHOICES = [
        ('pagado', 'Pagado'),
        ('anulado', 'Anulado'),
    ]
    
    METODO_PAGO_CHOICES = [
        ('transferencia', 'Transferencia'),
        ('efectivo', 'Efectivo'),
        ('cheque', 'Cheque'),
        ('tarjeta', 'Tarjeta'),
        ('otros', 'Otros'),
    ]
    
    cuenta = models.ForeignKey(
        CuentaPorPagar, 
        on_delete=models.CASCADE, 
        related_name='historial_pagos',
        verbose_name='Cuenta por Pagar'
    )
    fecha_pago = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Pago')
    monto_pagado = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Monto Pagado')
    metodo_pago = models.CharField(
        max_length=20, 
        choices=METODO_PAGO_CHOICES, 
        default='transferencia',
        verbose_name='Método de Pago'
    )
    referencia = models.CharField(max_length=100, blank=True, verbose_name='Referencia')
    observaciones = models.TextField(blank=True, verbose_name='Observaciones')
    usuario = models.ForeignKey(
        User, 
        on_delete=models.PROTECT,
        verbose_name='Usuario'
    )
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES,
        verbose_name='Estado del Pago'
    )
    
    class Meta:
        verbose_name = 'Historial de Pago'
        verbose_name_plural = 'Historial de Pagos'
        ordering = ['-fecha_pago']
    
    def __str__(self):
        return f"Pago {self.id} - {self.cuenta.numero_factura}"