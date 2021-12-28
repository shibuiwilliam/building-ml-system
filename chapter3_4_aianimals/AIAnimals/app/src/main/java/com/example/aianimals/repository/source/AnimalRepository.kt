package com.example.aianimals.repository.source


import com.example.aianimals.repository.Animal
import com.example.aianimals.repository.source.local.AnimalLocalDataSource

class AnimalRepository(
    val animalLocalDataSource: AnimalDataSource
) : AnimalDataSource {
    var cachedAnimals: MutableMap<String, Animal> = mutableMapOf()

    override fun listAnimals(callback: AnimalDataSource.ListAnimalsCallback) {
        if (this.cachedAnimals.isNotEmpty()) {
            callback.onListAnimal(this.cachedAnimals)
            return
        }

        animalLocalDataSource.listAnimals(object : AnimalDataSource.ListAnimalsCallback{
            override fun onListAnimal(animals: Map<String, Animal>) {
                cacheAnimals(animals)
                callback.onListAnimal(cachedAnimals)
            }

            override fun onDataNotAvailable() {
            }
        })
    }

    override fun getAnimal(
        animalID: String,
        callback: AnimalDataSource.GetAnimalCallback) {
        val animal = getAnimalFromCache(animalID)
        if (animal != null) {
            callback.onGetAnimal(animal)
            return
        }

        animalLocalDataSource.getAnimal(animalID, object : AnimalDataSource.GetAnimalCallback{
            override fun onGetAnimal(animal: Animal) {
                cacheAnimal(animal)
                callback.onGetAnimal(animal)
            }

            override fun onDataNotAvailable() {
            }
        })
    }

    override fun saveAnimal(animal: Animal) {
        animalLocalDataSource.saveAnimal(animal)
    }

    private fun cacheAnimal(animal: Animal) {
        this.cachedAnimals[animal.id] = animal
    }

    private fun cacheAnimals(animals: Map<String, Animal>){
        animals.forEach{
            cacheAnimal(it.value)
        }
    }

    private fun getAnimalFromCache(animalID: String) : Animal? {
        return this.cachedAnimals[animalID]
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