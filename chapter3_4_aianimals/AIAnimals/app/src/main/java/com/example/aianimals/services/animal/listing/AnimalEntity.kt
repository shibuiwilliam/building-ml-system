package com.example.aianimals.services.animal.listing

data class AnimalEntity(private val id: Int, private val poster: String) {
    fun toAnimal() = Animal(id, poster)
}