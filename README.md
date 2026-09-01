# backend
poryecto del sena

# atulizacion el 01/09/2026
se cambio bootstrap para que cree estados de pedido estados de pago y metodos de pago porque tuvo un error el pedido y el pago tronaban con error 500 al no encontrar esos datos

se creo size color y product variant porque no existian y sin eso nunca se podia agregar stock ni completar una compra

se agrego rate limit al registro de usuarios porque no tenia limite y era vulnerable a registros masivos

se probo el flujo completo primero con sqlite y luego confirmado por ti en docker con mariadb login crear producto crear variante registrar cliente agregar direccion agregar al carrito crear pedido y el stock bajo correctamente

se instalo y configuro docker en tu arch linux se arreglo el grupo docker y los permisos

se te dio un script para probar el flujo de compra contra tu contenedor cuando quieras

se genero un pdf con toda la documentacion de la api

pendiente si lo quieres el renombrado de archivos que hablamos hace rato y las cosas menores que quedaron marcadas como no bloqueantes comment y el lifespan
