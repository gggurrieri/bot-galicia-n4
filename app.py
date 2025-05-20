import os
import random
import requests
from flask import Flask
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from threading import Thread

TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Galicia N4 activo"

URLS_N4 = [
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/codigos-de-concepto-mas-frecuentes-para-transferir",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-abro-una-cuenta-cera",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-acepto-o-repudio-un-cheque-electronico",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-activo-el-office-token-gm",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-actualizo-el-componente-de-mi-firma-digital",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-agendo-un-contacto",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-agendo-un-contacto2",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-agrego-o-elimino-a-mi-nomina-la-cuenta-de-un-empleado",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-consulto-los-estados-de-apertura-de-cuentas-de-empleados-y-que-significan",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-consulto-mi-calificacion-y-mi-disponible",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-consulto-mis-debitos-automaticos-vigentes",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-consulto-mis-operaciones-vigentes",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-consulto-veps-pedientes",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-consulto-y-descargo-mis-comprobantes-de-afip",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-deposito-un-cheque-electronico",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-doy-de-alta-el-qr",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-doy-de-alta-un-convenio-de-cobranza-integrada",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-edito-los-permisos-de-los-usuarios",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-el-cliente-puede-retirar-un-saldo-remanente",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-elimino-un-servicio-activo",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-emito-un-cheque-electronico",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-emito-un-cheque-fisico",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-funciona-una-factura-de-credito-electronica",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-funciona-un-debin",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-hago-para-cobrar-con-debin",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-hago-una-suscripcion-o-rescate-de-un-fondo-fima",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-instalo-mi-firma-digital-en-la-computadora",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-invierto-en-acciones-cedear-y-etf",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-modifico-las-condiciones-de-una-prestacion-de-pago-directo",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-otorgo-o-modifico-permisos-pagos",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-pago-la-financiacion",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-pago-mis-consumos-en-dolares-con-sus-impuestos",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-pago-mi-tarjeta-galicia-rural-de-forma-manual",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-pago-un-servicio",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-pago-un-servicio-que-no-esta-adherido-a-mi-office-banking",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-pago-un-vep",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-paso-de-usar-office-banking-a-office-express",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-preparo-autorizo-operaciones-reconocimiento-facial",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-puedo-abrir-una-cuenta-sueldo-para-un-empleado-con-nacionalidad-extranjera",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-puedo-aceptar-la-utilizacion-y-cual-es-el-proceso",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-puedo-cobrar-con-qr",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-puedo-pausar-mi-tarjeta-si-no-la-encuentro",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-realizo-el-pago-de-una-cobranza-integrada",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-solicito-el-alta-y-o-baja-de-un-convenio-de-fondo-de-cese-laboral",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-solicito-el-extracto-para-reporte-de-impuestos",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-solicito-una-chequera",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-solicito-un-pedido-de-excepcion",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-uso-mi-firma-digital-en-otra-computadora-",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-y-donde-puedo-depositar-mi-cheque-fisico",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/conoce-lo-principal-sobre-comisiones-historiales-y-debitos-gm",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/cual-es-la-diferencia-entre-saldo-actual-y-disponible",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/cuales-son-los-beneficios-impositivos-de-un-prestamo-leasing",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/cuales-son-los-montos-limites-que-se-deben-tener-en-cuenta-para-operar",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/cuales-son-los-plazos-de-liquidacion",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/cuales-son-los-requisitos-para-vender-cheques",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/cuando-y-como-puedo-comprar-dolar-mep",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/cuanto-demora-y-a-donde-envian-las-tarjetas-de-mis-empleados",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/cuanto-tardan-en-acreditarse-mis-ventas-y-donde-puedo-consultarlas",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/cuanto-tiempo-demora-y-donde-puedo-retirar-mi-tarjeta-visa-business",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/cuanto-tiempo-tarda-el-analisis-y-aprobacion-de-mi-solicitud",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/de-que-formas-se-pueden-hacer-pagos-de-afip",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/desde-donde-se-retira-el-dinero",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/donde-consulto-mis-empleados-adheridos",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/donde-descargo-las-retenciones-de-mis-ventas-con-qr",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/donde-descargo-mis-comprobantes-de-pago",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/donde-encuentro-el-codigo-de-extraccion",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/donde-veo-las-tasas-que-cobran-por-la-venta-de-un-cheque",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/donde-veo-mi-limite-de-transferencias",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/el-acceso-es-para-todas-mis-empresas--gm",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/en-que-dias-y-horarios-puedo-pagar-servicios-afip",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/en-que-dias-y-horarios-puedo-pagar-un-servicio",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/en-que-horario-puedo-subir-el-archivo-de-base-de-clientes-a-office-banking",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/en-que-horarios-puedo-suscribir-o-rescatar-fondos-fima",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/estados-de-las-ventas-de-cheques",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/esta-por-vencer-mi-firma-digital",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/fechas-importante-y-canales-gm",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/hasta-que-fecha-puedo-ingresar-dinero-en-la-cuenta-cera",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/lo-primero-que-tenes-que-saber-sobre-galicia-mas",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/lo-primero-que-tenes-que-saber-sobre-gm",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/los-fondos-fima-rinden-como-un-plazo-fijo",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/los-prestamos-inmediatos-son-precancelables",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/mas-que-nunca-cuidate-de-las-estafas",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/me-rechazaron-un-cheque-electronico",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/no-puedo-vender-un-cheque",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/olvide-mi-nombre-de-usuario-gm",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/para-que-sirve-un-convenio-de-pagos-masivos",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/planes-de-cobranza-integrada",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/por-que-invertir-en-fondos-fima",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/puedo-anular-una-transferencia/",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/puedo-invertir-el-dinero-cera",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/puedo-pagar-servicios-vencidos",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/puedo-recibir-notificaciones-sobre-mis-vencimientos",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/puedo-saber-el-rendimiento-que-va-a-tener-mi-inversion-en-fondos-fima",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/puedo-transferir-un-monto-superior-a-mi-limite",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-beneficios-tiene-mi-qr",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-comision-se-le-cobra-al-cliente-por-realizar-la-operacion",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-debe-hacer-mi-empleado-si-su-cuenta-figura-en-estado-%22abierta-i%22",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-debe-hacer-mi-empleado-una-vez-que-complete-el-alta",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-documentos-me-van-a-pedir-y-cuanto-tiempo-tengo-para-presentarlos",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-es-cobro-de-proveedores",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-es-el-cereo-nocturno",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-e-s-galicia-mas",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-es-la-cuotaparte",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-es-office-express",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-es-una-factura-de-credito-electronica",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-es-un-bloqueo-judicial-ofb",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-es-un-emisor-destacado",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-hago-si-envie-un-archivo-equivocado-o-con-algun-error",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-hago-si-mi-usuario-suspendido",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-incluye-la-cuota-de-un-prestamo-y-que-tasas-lo-componen",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-medios-de-pago-acepta-mi-qr-y-como-los-activo",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-necesito-para-invertir-en-fondos-fima",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-necesito-para-realizar-pagos-masivos-por-archivos-masivos",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-necesito-para-realizar-pagos-por-archivos",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-necesito-para-recibir-una-orden-de-pago",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-necesito-para-transferir-al-exterior",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-pasa-si-mi-cliente-no-es-cliente-de-galicia",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-pasa-si-no-pago-una-cuota",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-permisos-son-necesarios-para-poder-hacer-pagos-afip",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-son-la-tna-y-la-tea",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-sucede-si-me-excedo-del-acuerdo",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-tengo-que-hacer-si-yo-operaba-con-los-codigos-s32-y-b35-dolar-blend",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/quienes-pueden-ser-destinatarios-de-la-orden-de-extraccion",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/quien-puede-autorizar-una-operacion",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/quiero-registrar-o-cambiar-mi-celular-pero-no-recibo-el-codigo-por-sms",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/quiero-saber-que-significan-los-estados-de-los-cheques-electronicos",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/recibi-un-cheque-electronico-que-hago",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/sobre-que-tipo-de-cuentas-se-pueden-crear-ordenes-de-extraccion",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/tengo-mas-de-un-usuario-puedo-operar-con-el-mismo-office-token",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/una-empresa-con-firma-conjunta-puede-extraer-dinero-con-esta-funcionalidad",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/vencio-mi-firma-digital",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/cambie-perdi-o-me-robaron-el-celular",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-solicito-el-certificado-para-acciones-civiles",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/cuales-son-las-ventajas-de-usar-office-express",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/programas-maliciosos",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-pago-sueldos-sin-convenio",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-puedo-pagar-sueldos-por-transferencia",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-es-una-orden-de-extraccion",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/puedo-depositar-un-cheque-electronico-antes-de-la-fecha-de-pago",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-abro-las-cuentas-de-mis-empleados",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-agrego-un-nuevo-usuario",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-vendo-cheques-con-tasas-preferenciales",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/no-veo-mis-cheques",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-otorgo-o-modifico-permisos-para-sueldos",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-cambio-mi-mail",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-otorgo-o-modifico-permisos-cuentas",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-roles-de-usuarios-existen",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-descargo-mis-extractos-de-cuentas-dadas-de-baja",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-envio-mi-cheque-a-custodia",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-reactivo-un-debito-automatico",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/guia-para-empezar-a-pagar-sueldos",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/las-transferencias-al-exterior-tienen-comisiones",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/puedo-anular-la-solicitud-de-una-transferencia",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/quienes-pueden-autorizar-una-operacion",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/tengo-una-tarjeta-pendiente-y-no-puedo-autorizarla",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-activo-el-office-token",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/quiero-pausar-mis-debitos-automaticos",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/por-que-y-que-debo-hacer-si-me-rechazaron-un-cheque",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-modifico-el-alias-de-mis-cuentas",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-anulo-o-pido-la-devolucion-de-un-cheque-electronico",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-doy-de-baja-el-debito-automatico-de-un-servicio",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-solicito-una-constancia-de-cbu",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-cambio-mi-clave-de-acceso-ofb",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-consulto-y-descargo-mis-extractos",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-desbloqueo-el-office-token",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-descargo-el-comprobante-de-un-movimiento",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-elimino-un-usuario",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-funcionan-los-impuestos-en-las-compras-de-dolares",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-realizo-una-transferencia",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-transfiero-entre-cuentas-propias",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/perdi-o-me-robaron-la-tarjeta",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/puedo-pagar-sueldos-a-cuentas-de-otros-bancos",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/desinstale-y-volvi-a-instalar-la-app",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-abro-una-nueva-cuenta",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/donde-consulto-mi-celular-y-mail",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/cuanto-tiempo-demora-y-donde-puedo-retirar-mi-tarjeta-de-debito",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-autorizo-una-operacion",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-tipos-de-fondos-fima-existen",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/anular-una-transferencia-ofb",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-funciona-mi-agenda-de-contactos",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-genero-el-office-token",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-genero-una-orden-de-extraccion",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-pago-un-debin",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-pido-el-levantamiento-de-un-embargo-o-bloqueo-judicial-ofb",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-pido-permisos",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-registro-o-agrego-un-celular",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-simulo-y-solicito-un-prestamo-inmediato",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-solicito-la-liquidacion-de-una-orden-de-pago",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-solicito-la-reimpresion-de-mi-tarjeta-de-debito",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/donde-consulto-el-historial-de-pagos-por-archivo",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/mas-que-nunca-cuidate-de-las-estafas-gm",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/olvide-mi-nombre-de-usuario",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/puedo-anular-una-transferencia-que-realice",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/puedo-descargar-comprobantes-de-mis-debitos-automaticos",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-beneficios-tienemi-tarjeta-visa-business",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-es-pago-directo",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-es-una-cuenta-cera",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-tipos-de-venta-de-cheques-existen",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/quiero-saber-las-tarjetas-que-estan-asociadas-a-mi-cuenta",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-solicito-el-alta-de-mi-tarjeta-de-credito",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/puedo-pedir-la-devolucion-de-un-debito-automatico",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/donde-consulto-los-datos-de-mi-usuario",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/no-funciona-el-office-token",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-rescato-un-cheque-en-custodia",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/codigos-de-concepto-mas-frecuentes-para-una-orden-de-pago",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-adhiero-un-debito-automatico-a-mi-cuenta",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-apruebo-o-rechazo-la-solicitud-de-alta-de-un-usuario",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-cambio-mi-clave-de-acceso",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-doy-de-alta-o-baja-mi-terminal",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-doy-de-alta-un-convenio",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-doy-de-baja-mi-acuerdo",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-ingreso-dinero-en-la-cuenta-cera",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-le-doy-el-rol-de-administrador-a-un-usuario",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-lo-activo-y-que-necesito",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-otorgo-o-modifico-permisos-cobros",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-pago-sueldos-por-archivo",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-puedo-desconocer-una-compra-realizada-con-mi-tarjeta-de-credito",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-puedo-extraer-efectivo",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-puedo-saber-mi-limite-de-transferencias-en-dolares",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-realizo-los-pagos-de-fondo-de-cese-laboral",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-realizo-un-pago-masivo-pagos",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-solicito-el-alta-de-mi-tarjeta-de-debito",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-solicito-la-reimpresion-de-mi-tarjeta-de-credito",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-solicito-una-calificacion-crediticia-y-cuales-son-sus-estados",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-vendo-un-cheque-y-cuando-se-libera-el-disponible",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/conoce-nuestros-canales-oficiales",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/cuando-me-reintegran-los-fondos-debitados-por-un-embargo-judicial-ofb",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/cuanto-tarda-en-acreditarse-una-transferencia",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/demora-una-transferencia-que-realice",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/desconozco-un-movimiento",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/donde-encuentro-mi-alias-y-cbu",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/donde-puedo-consultar-y-descargar-mis-resumenes-new",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/estados-de-una-transferencia",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/fechas-importante-y-canales",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-documentacion-me-van-a-pedir-y-cuanto-tiempo-tengo-para-presentarla",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-es-una-prenda",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-es-un-embargo-judicial-ofb",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-significa-pendiente-banco-credito",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/quiero-vincular-nave-con-tiendanube",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/no-veo-una-de-mis-cuentas",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-es-y-como-funciona-el-debin",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-hago-si-me-piden-validar-mi-identidad-con-un-codigo-qr",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-descargo-el-comprobante-de-una-transferencia",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-creo-o-desbloqueo-mi-pin-banelco",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-leo-el-resumen-de-mi-tarjeta",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/puedo-simular-la-venta-de-un-cheque",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-es-y-como-solicito-el-formulario-raype",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/quienes-pueden-comprar-dolar-mep",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/mi-usuario-usuario-se-bloqueo",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/olvide-mi-clave-de-acceso",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-puedo-desconocer-una-compra-realizada-con-mi-tarjeta-de-debito",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-es-un-debin-recurrente-o-un-debin-preautorizado",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/a-que-productos-puedo-acceder-con-mi-calificacion",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-consulto-los-movimientos-de-mis-fondos-fima",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-copio-y-comparto-mi-alias-y-cbu",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-doy-de-alta-un-convenio-masivos-pagos",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-exporto-mis-contactos-a-un-archivo",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-pago-las-facturas-en-dolares-o-en-otra-moneda",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-puedo-pagar-sueldos-sin-tener-convenios",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-se-calculan-los-intereses-y-que-otros-cargos-me-cobran",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-solicito-la-carta-de-credito-y-cuales-son-los-tipos-de-solicitud",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/como-verifico-si-quedo-habilitado-un-convenio",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/creo-que-me-estafaron",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/donde-consulto-y-descargo-los-comprobantes-de-pagos-de-cuotas",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/donde-encuentro-el-codigo-de-pago-electronico-de-mi-servicio",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/donde-puedo-consultar-el-limite-de-mi-tarjeta-y-de-un-adicional",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/me-rechazaron-un-cheque-fisico",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/puedo-aumentar-mi-limite-de-transferencia",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-documentos-tengo-que-enviar-en-la-solicitud-de-una-orden-de-pago",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-documentos-tengo-que-enviar-en-la-solicitud-de-una-trasferencia",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-es-y-como-funciona-el-debin/",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/que-necesito-para-comprar-o-vender-dolar-mep",
    "https://ayudaempresas.galicia.ar/AyudajuridicaSPA/ini/n4/quiero-solicitar-y-descargar-el-archivo-de-cese-laboral"
]

def calificar_url(session, full_url):
    try:
        session.post(f"{full_url}/Utilidad", data={"valor": "1"})
        session.post(f"{full_url}/Satisfaccion", data={"valor": "5"})
        return True
    except:
        return False

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Bot Galicia N4 activo. Usá /activar 3 para calificar 3 URLs.")

def activar(update: Update, context: CallbackContext):
    cantidad = 1
    if context.args and context.args[0].isdigit():
        cantidad = min(int(context.args[0]), 10)

    if not URLS_N4:
        update.message.reply_text("No hay URLs disponibles para calificar.")
        return

    seleccionadas = random.sample(URLS_N4, min(cantidad, len(URLS_N4)))
    session = requests.Session()
    resumen = []

    for full_url in seleccionadas:
        exito = calificar_url(session, full_url)
        resumen.append(f"✅ {full_url}" if exito else f"❌ {full_url}")

    mensaje = "\n".join(resumen)
    update.message.reply_text(f"Calificación completa:\n{mensaje}")

import time

def correr_bot():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("activar", activar))
    updater.start_polling()
    print("Bot Galicia N4 está activo.")
    while True:
        time.sleep(10)

if __name__ == "__main__":
    Thread(target=correr_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
