package com.example.aianimals.repository.animal.source.remote

import android.util.Log
import androidx.annotation.VisibleForTesting
import com.example.aianimals.repository.animal.Animal
import com.example.aianimals.repository.animal.source.AnimalCategory
import com.example.aianimals.repository.animal.source.AnimalDataSource
import com.example.aianimals.repository.animal.source.AnimalMetadata
import com.example.aianimals.repository.animal.source.AnimalSubcategory

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

    override suspend fun getMetadata(token: String): AnimalMetadata? {
        val response = animalAPI.getMetadata(token)
        if (response.isSuccessful) {
            val body = response.body()!!
            val animalCategory = body.animalCategory.map {
                it.id to AnimalCategory(
                    id = it.id,
                    nameEn = it.nameEn,
                    nameJa = it.nameJa
                )
            }.toMap()
            val animalSubcategory = mutableMapOf<Int, MutableMap<Int, AnimalSubcategory>>()
            for (s in body.animalSubcategory) {
                if (animalSubcategory.containsKey(s.animalCategoryId)) {
                    animalSubcategory[s.animalCategoryId]!![s.id] = AnimalSubcategory(
                        id = s.id,
                        animalCategoryId = s.animalCategoryId,
                        animalCategoryNameEn = s.animalCategoryNameEn,
                        animalCategoryNameJa = s.animalCategoryNameJa,
                        nameEn = s.nameEn,
                        nameJa = s.nameJa
                    )
                } else {
                    animalSubcategory[s.animalCategoryId] = mutableMapOf(
                        s.id to AnimalSubcategory(
                            id = s.id,
                            animalCategoryId = s.animalCategoryId,
                            animalCategoryNameEn = s.animalCategoryNameEn,
                            animalCategoryNameJa = s.animalCategoryNameJa,
                            nameEn = s.nameEn,
                            nameJa = s.nameJa
                        )
                    )
                }
            }
            return AnimalMetadata(
                animalCategoryMap = animalCategory,
                animalSubcategoryMap = animalSubcategory
            )
        }
        Log.e(TAG, "failed to get metadata")
        return null
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