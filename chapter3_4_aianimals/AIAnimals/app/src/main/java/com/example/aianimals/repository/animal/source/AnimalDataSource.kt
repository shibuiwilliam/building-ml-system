package com.example.aianimals.repository.animal.source

import com.example.aianimals.repository.animal.Animal

interface AnimalDataSource {
    suspend fun createAnimals()
    suspend fun listAnimals(
        query: String?,
        refresh: Boolean
    ): Map<String, Animal>
    suspend fun getAnimal(animalID: String): Animal?
    suspend fun saveAnimal(animal: Animal)
    suspend fun getMetadata(token: String): AnimalMetadata?
}