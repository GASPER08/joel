package main

import (
	"github.com/gin-gonic/gin"
	"github.com/tuusuario/crud-app/config"
	"github.com/tuusuario/crud-app/routes"
)

func main() {
	config.ConectarMongo()

	r := gin.Default()

	routes.UsuarioRoutes(r)

	r.Run(":4000")
}
