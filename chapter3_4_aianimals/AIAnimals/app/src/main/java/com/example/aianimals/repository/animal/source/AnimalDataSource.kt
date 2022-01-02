package com.example.aianimals.repository.animal.source

import com.example.aianimals.repository.animal.Animal

interface AnimalDataSource {
    interface ListAnimalsCallback {
        fun onListAnimal(animals: Map<String, Animal>)
        fun onDataNotAvailable()
    }

    interface GetAnimalCallback {
        fun onGetAnimal(animal: Animal)
        fun onDataNotAvailable()
    }

    fun createAnimals()
    fun listAnimals(callback: ListAnimalsCallback)
    fun getAnimal(animalID: String, callback: GetAnimalCallback)
    fun saveAnimal(animal: Animal)
    suspend fun getMetadata(token: String): AnimalMetadata?
}