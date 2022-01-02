package com.example.aianimals.repository.animal.source


import android.util.Log
import com.example.aianimals.repository.animal.Animal
import com.example.aianimals.repository.animal.source.local.AnimalLocalDataSource
import com.example.aianimals.repository.animal.source.remote.AnimalRemoteDataSource

class AnimalRepository(
    val animalLocalDataSource: AnimalDataSource,
    val animalRemoteDataSource: AnimalRemoteDataSource
) : AnimalDataSource {
    private val TAG = AnimalRepository::class.java.simpleName

    var cachedAnimals: MutableMap<String, Animal> = mutableMapOf()

    override suspend fun createAnimals() {}

    override suspend fun listAnimals(
        query: String?,
        refresh: Boolean
    ): Map<String, Animal> {
        if (!refresh && this.cachedAnimals.isNotEmpty()) {
            return this.cachedAnimals
        }

        val localAnimals = animalLocalDataSource.listAnimals(query, refresh)
        if (localAnimals.isNotEmpty()) {
            cacheAnimals(localAnimals)
            return localAnimals
        }
        return mapOf()
    }

    override suspend fun getAnimal(animalID: String): Animal? {
        val animal = getAnimalFromCache(animalID)
        if (animal != null) {
            return animal
        }

        val localAnimal = animalLocalDataSource.getAnimal(animalID)
        return localAnimal
    }

    override suspend fun saveAnimal(animal: Animal) {
        Log.i("AnimalRepository", "register ${animal}")
        animalLocalDataSource.saveAnimal(animal)
    }

    override suspend fun getMetadata(token: String): AnimalMetadata? {
        return animalRemoteDataSource.getMetadata(token)
    }

    private fun cacheAnimal(animal: Animal) {
        this.cachedAnimals[animal.id] = animal
    }

    private fun cacheAnimals(animals: Map<String, Animal>) {
        animals.forEach {
            cacheAnimal(it.value)
        }
    }

    private fun getAnimalFromCache(animalID: String): Animal? {
        return this.cachedAnimals[animalID]
    }

    companion object {
        private var INSTANCE: AnimalRepository? = null

        @JvmStatic
        fun getInstance(
            animalLocalDataSource: AnimalLocalDataSource,
            animalRemoteDataSource: AnimalRemoteDataSource
        ): AnimalRepository {
            return INSTANCE ?: AnimalRepository(
                animalLocalDataSource,
                animalRemoteDataSource
            )
                .apply { INSTANCE = this }
        }

        @JvmStatic
        fun destroyInstance() {
            INSTANCE = null
        }
    }
}