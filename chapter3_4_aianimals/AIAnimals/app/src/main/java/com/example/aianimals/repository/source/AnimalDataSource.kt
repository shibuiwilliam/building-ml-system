package com.example.aianimals.repository.source

import com.example.aianimals.repository.Animal

interface AnimalDataSource {
    interface ListAnimalsCallback {
        fun onListAnimal(animals: Map<Int, Animal>)
        fun onDataNotAvailable()
    }

    interface GetAnimalCallback {
        fun onGetAnimal(animal: Animal)
        fun onDataNotAvailable()
    }

    fun listAnimals(callback: ListAnimalsCallback)
    fun getAnimal(animalID: Int, callback: GetAnimalCallback)
}