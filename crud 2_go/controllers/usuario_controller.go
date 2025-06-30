package controllers

import (
	"context"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/tuusuario/crud-app/config"
	"github.com/tuusuario/crud-app/models"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

// Crear usuario
func CrearUsuario(c *gin.Context) {
	var nuevo models.Usuario
	if err := c.ShouldBindJSON(&nuevo); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	res, err := config.Coleccion.InsertOne(context.Background(), nuevo)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "No se pudo crear"})
		return
	}
	c.JSON(http.StatusOK, res)
}

// Obtener todos
func ObtenerUsuarios(c *gin.Context) {
	cursor, err := config.Coleccion.Find(context.Background(), bson.M{})
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al obtener datos"})
		return
	}
	defer cursor.Close(context.Background())

	var usuarios []models.Usuario
	if err = cursor.All(context.Background(), &usuarios); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al convertir datos"})
		return
	}
	if usuarios == nil {
		usuarios = []models.Usuario{}
	}
	c.JSON(http.StatusOK, usuarios)
}

// Actualizar usuario
func ActualizarUsuario(c *gin.Context) {
	id := c.Param("id")
	objID, err := primitive.ObjectIDFromHex(id)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "ID inválido"})
		return
	}

	var datos models.Usuario
	if err := c.ShouldBindJSON(&datos); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	update := bson.M{"$set": bson.M{"nombre": datos.Nombre, "correo": datos.Correo}}
	_, err = config.Coleccion.UpdateOne(context.Background(), bson.M{"_id": objID}, update)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al actualizar"})
		return
	}
	c.JSON(http.StatusOK, gin.H{"mensaje": "Actualizado"})
}

// Eliminar usuario
func EliminarUsuario(c *gin.Context) {
	id := c.Param("id")
	objID, err := primitive.ObjectIDFromHex(id)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "ID inválido"})
		return
	}

	_, err = config.Coleccion.DeleteOne(context.Background(), bson.M{"_id": objID})
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al eliminar"})
		return
	}
	c.JSON(http.StatusOK, gin.H{"mensaje": "Eliminado"})
}
