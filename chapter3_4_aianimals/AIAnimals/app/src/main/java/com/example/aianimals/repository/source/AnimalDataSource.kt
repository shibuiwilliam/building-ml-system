package com.example.aianimals.repository.source

import com.example.aianimals.repository.Animal

interface AnimalDataSource {
    interface ListAnimalsCallback {
        fun onListAnimal(animals: Map<Int, Animal>)
    }
    interface GetAnimalCallback {
        fun onGetAnimal(animal: Animal)
    }
    fun listAnimals(callback: ListAnimalsCallback)
    fun getAnimal(animalID: Int, callback: GetAnimalCallback)
}