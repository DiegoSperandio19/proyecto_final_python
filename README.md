# proyecto_final

## Instrucciones de ejecución:

1) Docker: docker compose up 

2) Al terminar de levantar, entrar a la dirección: http://localhost:8000

3) Pgadmin se encuentra en la dirección: http://localhost:5050

4) Se coloca en el login de pgadmin el usuario admin@admin.com y la contraseña admin

5) Se registra un servidor y se debe colocar db en la dirección, postgres en el usuario y postgres en la contraseña. El nombre del servidor no importa cual sea

6) Para ejecutarse con usuarios de admin y cliente de prueba, ejecutar en pgadmin el archivo inserts.sql del proyecto
   
7) Para iniciar sesión en la página se utiliza el correo del usuario:
   	Para admin: username:admin@gmail.com password:admin
   	Para cliente: username:client@gmail.com password:client
   
8) El admin puede acceder a todas las funcionalidades del programa, pero el cliente no


## Explicación de la arquitectura:

El directorio raíz "proyecto_final_python" tiene dos subdirectorios: alembic (contiene las migraciones a la base de datos) y app (donde se encuentra la aplicación). 
Dentro de app, se encuentran 4 subdirectorios correspondientes cada módulo del proyecto: auth, restaurants, reservations y menu, los cuales a su vez se dividen cada uno en tres subdirectorios: domain (lógica del negocio, sus subdirectorios son: entities, repositories, services y value_objects), infrastructure (exterior que interactúa con el dominio, sus subdirectorios son: orm_entities, repositories y utils en el caso de auth) y api (puertas de entrada y salida al dominio tiene como subdirectorio a controllers que tiene a los routers de la aplicación). Por último, tiene además un subdirectorio shared en el que se encuentra el archivo exceptions.py para comunicar errores de manera más clara y controlada entre componentes del sistema.
