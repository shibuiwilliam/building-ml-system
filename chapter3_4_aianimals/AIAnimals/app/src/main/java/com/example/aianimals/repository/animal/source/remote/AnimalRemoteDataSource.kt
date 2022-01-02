package com.example.aianimals.repository.animal.source.remote

import androidx.annotation.VisibleForTesting
import com.example.aianimals.repository.animal.Animal
import com.example.aianimals.repository.animal.source.AnimalDataSource

class AnimalRemoteDataSource private constructor(
    val animalAPI: AnimalAPIInterface
) : AnimalDataSource {
    private val TAG = AnimalRemoteDataSource::class.java.simpleName

    override fun createAnimals() {}

    override fun listAnimals(callback: AnimalDataSource.ListAnimalsCallback) {
        TODO("Not yet implemented")
    }

    override fun getAnimal(animalID: String, callback: AnimalDataSource.GetAnimalCallback) {
        TODO("Not yet implemented")
    }

    override fun saveAnimal(animal: Animal) {
        TODO("Not yet implemented")
    }


    companion object {
        private var INSTANCE: AnimalRemoteDataSource? = null

        @JvmStatic
        fun getInstance(animalAPI: AnimalAPIInterface): AnimalRemoteDataSource {
            if (INSTANCE == null) {
                synchronized(AnimalRemoteDataSource::javaClass) {
                    INSTANCE = AnimalRemoteDataSource(animalAPI)
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