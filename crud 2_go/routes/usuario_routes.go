package routes

import (
	"github.com/gin-gonic/gin"
	"github.com/tuusuario/crud-app/controllers"
)

func UsuarioRoutes(r *gin.Engine) {
	r.GET("/", func(c *gin.Context) {
		c.String(200, "Bienvenido al API CRUD en capas con Go + Gin + MongoDB 🚀")
	})

	r.GET("/usuarios", controllers.ObtenerUsuarios)
	r.POST("/usuarios", controllers.CrearUsuario)
	r.PUT("/usuarios/:id", controllers.ActualizarUsuario)
	r.DELETE("/usuarios/:id", controllers.EliminarUsuario)
}
