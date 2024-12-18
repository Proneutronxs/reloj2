from django.urls import path
from App.API.vistas.calidad import calidad, bascula, empaque
from App.API.vistas.Rondin import rondin
from App.API.vistas.Contabilidad import contable
urlpatterns = [
    ######################### CALIDAD EMPAQUE ###################################

    path('calidad/image/caja', calidad.image_caja, name="guarda_caja_imagen"),
    path('calidad/image/plu', calidad.image_plu, name="guarda_plu_imagen"),
    path('calidad/image/caja_plu', calidad.image_caja_plu, name="guarda_plu_caja"),
    
    path('calidad/caja/<str:nombre>', calidad.ver_caja, name='ver_caja'),

    path('calidad/prueba', calidad.pruebas_sql, name="pruebas_sql"),

    ######################## MADUREZ DE FRUTOS ###########################

    path('calidad/presiones/inserta', calidad.inserta_presiones, name='inserta_presiones'),
    path('calidad/presiones/busqueda', calidad.busca_presiones, name='busca_presiones'),
    path('calidad/presiones/mostrar', calidad.muestra_presiones, name='muestra_presiones'),
    path('calidad/presiones/promedio', calidad.promedio_presiones, name='promedio_presiones'),

    ######################## ENDPOINTS CALIDAD BASCULA ###########################

    path('calidad-bascula/data-inicial/', bascula.dataInicial, name='bascula_data_inicial'),

    path('calidad-bascula/data-lotes/', bascula.traeLotes, name='trae_lotes'),

    path('calidad-bascula/data-detalle-lote/', bascula.traeDetalleLotes, name='detalle_lotes'),

    path('calidad-bascula/inserta-data/', bascula.Ejecuta_Procedimientos, name='ejecuta_procedimientos'),

    path('calidad-bascula/ver-data/', bascula.resultadosInsert, name='resultadosInsert'),

    path('calidad-empaque/subir-imagen/', calidad.upload_image_from_directory, name='subir_imagen_directorio'),



    ####RONDIN

    #path('rondin-empaque/recibe-fichadas/', rondin.insert_fichada_rondin, name='recibe_fichadas_rondin'),

    path('rondin-empaque/recibe-registros/', rondin.insertaRegistrosRondin, name='rondin_recibe_registros'),

    path('rondin-empaque/envia-sereno/', rondin.devuelveLegajoNombre, name='rondin_envia_sereno'),

    path('rondin-empaque/envia-ubicacion/', rondin.devuelveNombreSector, name='rondin_envia_ubicacion'),

    path('rondin-empaque/busca-resgistros/', rondin.buscaRegistros, name='rondin_busca_registros'),


    ######################## ENDPOINTS CALIDAD CONTROL EMPAQUE ###########################

    path('calidad-empaque/busqueda-caja/', empaque.busquedaCaja, name='calidad_empaque_busqueda_caja'),

    path('calidad-empaque/enviar-caja/', empaque.guardaCaja, name='calidad_empaque_guarda_caja'),

    path('calidad-empaque/update-caja/', empaque.actualizarCaja, name='calidad_empaque_update_caja'),

    path('calidad-empaque/busqueda-dia-caja/', empaque.busquedaCajaDia, name='calidad_empaque_busqueda_dia_caja'),

    path('calidad-empaque/busqueda-update-caja/', empaque.busquedaCajaUpdate, name='calidad_empaque_busqueda_update_caja'),


    ######################## ENDPOINTS CONTABILIDAD ###########################

    path('contabilidad/habilitar-cerrar/', contable.guardar_periodo_habilitado, name='guardar_periodo_habilitado'),


]