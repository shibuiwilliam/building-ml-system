package com.example.aianimals.repository.animal.source.local

import android.util.Log
import androidx.annotation.VisibleForTesting
import com.example.aianimals.middleware.AppExecutors
import com.example.aianimals.middleware.Utils
import com.example.aianimals.repository.animal.Animal
import com.example.aianimals.repository.animal.source.AnimalDataSource
import com.example.aianimals.repository.animal.source.AnimalMetadata
import kotlinx.coroutines.withContext

class AnimalLocalDataSource private constructor(
    val appExecutors: AppExecutors,
    val animalDao: AnimalDao
) : AnimalDataSource {
    private val TAG = AnimalLocalDataSource::class.java.simpleName

    override suspend fun createAnimals() {
        for (i in 0..20) {
            val id = Utils.generateUUID()
            val animal = Animal(
                id,
                "ネコ",
                "かわいい",
                "2020/11/24",
                0,
                "https://storage.googleapis.com/aianimals/images/0016e503d29a4be9a4b852f2a5b44525.jpg"
            )
            saveAnimal(animal)
            Log.i("AnimalRepository", "animal: ${animal}")
        }
    }

    override suspend fun listAnimals(query: String?): Map<String, Animal> {
        val animalMap = mutableMapOf<String, Animal>()
        withContext(appExecutors.ioContext) {
            val count = animalDao.countAnimals()
            if (count == 0) {
                createAnimals()
            }
            val animals = animalDao.listAnimals()
            withContext(appExecutors.defaultContext) {
                if (animals.isNotEmpty()) {
                    animals.forEach { animalMap[it.id] = it }
                }
            }
        }
        return animalMap
    }

    override suspend fun getAnimal(animalID: String): Animal? {
        var animal: Animal? = null
        withContext(appExecutors.ioContext) {
            animal = animalDao.getAnimal(animalID)
        }
        return animal
    }

    override suspend fun saveAnimal(animal: Animal) {
        withContext(appExecutors.ioContext) {
            animalDao.insertAnimal(animal)
        }
    }

    override suspend fun getMetadata(): AnimalMetadata? {
        return null
    }

    companion object {
        private var INSTANCE: AnimalLocalDataSource? = null

        @JvmStatic
        fun getInstance(
            appExecutors: AppExecutors,
            animalDao: AnimalDao
        ): AnimalLocalDataSource {
            if (INSTANCE == null) {
                synchronized(AnimalLocalDataSource::javaClass) {
                    INSTANCE = AnimalLocalDataSource(appExecutors, animalDao)
                }
            }
            return INSTANCE!!
        }

        @VisibleForTesting
        fun clearInstance() {
            INSTANCE = null
        }
    }
}