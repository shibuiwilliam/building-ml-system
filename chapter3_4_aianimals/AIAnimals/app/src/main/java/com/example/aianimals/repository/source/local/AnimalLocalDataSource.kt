package com.example.aianimals.repository.source.local

import android.util.Log
import androidx.annotation.VisibleForTesting
import com.example.aianimals.middleware.AppExecutors
import com.example.aianimals.repository.Animal
import com.example.aianimals.repository.source.AnimalDataSource
import com.example.aianimals.repository.source.AnimalRepository

class AnimalLocalDataSource private constructor(
    val appExecutors: AppExecutors,
    val animalDao: AnimalDao
): AnimalDataSource{
    var animals: MutableMap<Int, Animal> = mutableMapOf<Int, Animal>()

    init {
        this.animals = this.createDummyAnimalList()
    }

    private fun createDummyAnimalList(): MutableMap<Int, Animal> {
        val animals: MutableMap<Int, Animal> = mutableMapOf<Int, Animal>()
        val range = (10..50)
        for (i in 0..20) {
            val animal = Animal(i, "Kotlinスタートブック", range.random() * 100, "2020/11/24")
            animals[i] = animal
            Log.i("AnimalRepository", "animal: ${animal}")
        }
        return animals
    }

    override fun listAnimals(callback: AnimalDataSource.ListAnimalsCallback) {
        appExecutors.diskIO.execute{
            val animals = animalDao.listAnimals()
            appExecutors.mainThread.execute{
                if (animals.isEmpty()){
                    callback.onDataNotAvailable()
                } else {
                    callback.onListAnimal(this.animals)
                }
            }
        }
    }

    override fun getAnimal(animalID: Int, callback: AnimalDataSource.GetAnimalCallback) {
        appExecutors.diskIO.execute{
            val animal = animalDao.getAnimal(animalID)
            appExecutors.mainThread.execute{
                if (animal != null) {
                    callback.onGetAnimal(animal)
                } else {
                    callback.onDataNotAvailable()
                }
            }
        }
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
                    INSTANCE= AnimalLocalDataSource(appExecutors, animalDao)
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