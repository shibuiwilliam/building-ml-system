package com.example.aianimals.repository.animal.source


import android.util.Log
import com.example.aianimals.BuildConfig
import com.example.aianimals.repository.animal.Animal
import com.example.aianimals.repository.animal.source.local.AnimalLocalDataSource
import com.example.aianimals.repository.animal.source.remote.AnimalRemoteDataSource

data class LastSearchedQuery(
    val animalCategoryNameEn: String?,
    val animalCategoryNameJa: String?,
    val animalSubcategoryNameEn: String?,
    val animalSubcategoryNameJa: String?,
    val phrases: String?
)

class AnimalRepository(
    val animalLocalDataSource: AnimalDataSource,
    val animalRemoteDataSource: AnimalRemoteDataSource
) : AnimalDataSource {
    private val TAG = AnimalRepository::class.java.simpleName

    override suspend fun createAnimals() {}

    override suspend fun listAnimals(query: String?): Map<String, Animal> {
        if (BuildConfig.USE_LOCAL_DATA) {
            val localAnimals = animalLocalDataSource.listAnimals(query)
            if (localAnimals.isNotEmpty()) {
                return localAnimals
            }
        }

        val remoteAnimals = animalRemoteDataSource.listAnimals(query)
        if (remoteAnimals.isNotEmpty()) {
            return remoteAnimals
        }
        return mapOf()
    }

    override suspend fun getAnimal(animalID: String): Animal? {
        if (BuildConfig.USE_LOCAL_DATA) {
            val localAnimal = animalLocalDataSource.getAnimal(animalID)
            return localAnimal
        }

        val animal = animalRemoteDataSource.getAnimal(animalID)
        return animal
    }

    override suspend fun saveAnimal(animal: Animal) {
        Log.i("AnimalRepository", "register ${animal}")
        animalLocalDataSource.saveAnimal(animal)
    }

    override suspend fun getMetadata(): AnimalMetadata? {
        return animalRemoteDataSource.getMetadata()
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