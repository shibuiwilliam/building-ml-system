package com.example.aianimals.repository.source

import android.util.Log
import com.example.aianimals.repository.Animal
import com.example.aianimals.repository.source.local.AnimalLocalDataSource

class AnimalRepository(
    val animalLocalDataSource: AnimalLocalDataSource
) : AnimalDataSource {
    var animals: MutableMap<Int, Animal> = mutableMapOf()

    override fun listAnimals(callback: AnimalDataSource.ListAnimalsCallback) {
        callback.onListAnimal(this.animals)
    }

    override fun getAnimal(animalID: Int, callback: AnimalDataSource.GetAnimalCallback) {
        val animal = this.animals[animalID]!!
        callback.onGetAnimal(animal)
    }

    companion object {
        private var INSTANCE: AnimalRepository? = null

        @JvmStatic
        fun getInstance(
            animalLocalDataSource : AnimalLocalDataSource
        ): AnimalRepository {
            return INSTANCE ?: AnimalRepository(animalLocalDataSource)
                .apply { INSTANCE = this }
        }

        @JvmStatic
        fun destroyInstance() {
            INSTANCE = null
        }
    }
}