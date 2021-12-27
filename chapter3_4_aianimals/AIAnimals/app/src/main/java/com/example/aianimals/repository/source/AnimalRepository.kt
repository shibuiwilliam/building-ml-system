package com.example.aianimals.repository.source

import android.util.Log
import com.example.aianimals.repository.Animal

class AnimalRepository(): AnimalDataSource{
    var animals: MutableMap<Int, Animal> = mutableMapOf<Int, Animal>()
    init {
        this.animals = this.createDummyAnimalList()
    }

    private fun createDummyAnimalList(): MutableMap<Int, Animal> {
        val animals: MutableMap<Int, Animal> = mutableMapOf<Int, Animal>()
        val range = (10..50)
        for (i in 0..20) {
            val animal = Animal(i,"Kotlinスタートブック", range.random()*100, "2020/11/24")
            animals[i] = animal
            Log.i("AnimalRepository", "animal: ${animal}")
        }
        return animals
    }

    override fun listAnimals(callback: AnimalDataSource.ListAnimalsCallback) {
        callback.onListAnimal(this.animals)
    }

    override fun getAnimal(animalID: Int, callback: AnimalDataSource.GetAnimalCallback) {
        val animal = this.animals[animalID]!!
        callback.onGetAnimal(animal)
    }

    companion object {
        private var INSTANCE: AnimalRepository? = null
        @JvmStatic fun getInstance(): AnimalRepository {
            return INSTANCE ?: AnimalRepository()
                .apply { INSTANCE = this }
        }
        @JvmStatic fun destroyInstance() {
            INSTANCE = null
        }
    }
}