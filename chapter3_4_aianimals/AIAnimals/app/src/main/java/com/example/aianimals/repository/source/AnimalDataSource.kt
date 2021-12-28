package com.example.aianimals.repository.source

import com.example.aianimals.repository.Animal

interface AnimalDataSource {
    interface ListAnimalsCallback {
        fun onListAnimal(animals: Map<String, Animal>)
        fun onDataNotAvailable()
    }

    interface GetAnimalCallback {
        fun onGetAnimal(animal: Animal)
        fun onDataNotAvailable()
    }

    fun listAnimals(callback: ListAnimalsCallback)
    fun getAnimal(animalID: String, callback: GetAnimalCallback)
    fun saveAnimal(animal: Animal)
}