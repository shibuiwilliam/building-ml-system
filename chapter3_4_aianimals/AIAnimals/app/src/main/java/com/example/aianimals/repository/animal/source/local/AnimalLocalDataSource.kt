package com.example.aianimals.repository.animal.source.local

import android.util.Log
import androidx.annotation.VisibleForTesting
import com.example.aianimals.middleware.AppExecutors
import com.example.aianimals.middleware.Utils
import com.example.aianimals.repository.animal.Animal
import com.example.aianimals.repository.animal.source.AnimalDataSource
import com.example.aianimals.repository.animal.source.AnimalMetadata

class AnimalLocalDataSource private constructor(
    val appExecutors: AppExecutors,
    val animalDao: AnimalDao
) : AnimalDataSource {
    private val TAG = AnimalLocalDataSource::class.java.simpleName

    override fun createAnimals() {
        for (i in 0..20) {
            val id = Utils.generateUUID()
            val animal = Animal(
                id,
                "ネコ",
                "かわいい",
                "2020/11/24",
                0,
                "https://www.anicom-sompo.co.jp/nekonoshiori/wp-content/uploads/2018/12/724-2.jpg"
            )
            saveAnimal(animal)
            Log.i("AnimalRepository", "animal: ${animal}")
        }
    }

    override fun listAnimals(callback: AnimalDataSource.ListAnimalsCallback) {
        appExecutors.diskIO.execute {
            val animals = this.animalDao.listAnimals()
            appExecutors.mainThread.execute {
                if (animals.isEmpty()) {
                    callback.onDataNotAvailable()
                } else {
                    val mAnimals = animals.map { it.id to it }.toMap()
                    callback.onListAnimal(mAnimals)
                }
            }
        }
    }

    override fun getAnimal(animalID: String, callback: AnimalDataSource.GetAnimalCallback) {
        appExecutors.diskIO.execute {
            val animal = this.animalDao.getAnimal(animalID)
            appExecutors.mainThread.execute {
                if (animal != null) {
                    callback.onGetAnimal(animal)
                } else {
                    callback.onDataNotAvailable()
                }
            }
        }
    }

    override fun saveAnimal(animal: Animal) {
        appExecutors.diskIO.execute {
            this.animalDao.insertAnimal(animal)
        }
    }

    override suspend fun getMetadata(token: String): AnimalMetadata? {
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