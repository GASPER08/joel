package models

import "go.mongodb.org/mongo-driver/bson/primitive"

type Usuario struct {
	ID     primitive.ObjectID `bson:"_id,omitempty" json:"id,omitempty"`
	Nombre string             `bson:"nombre" json:"nombre"`
	Correo string             `bson:"correo" json:"correo"`
}
