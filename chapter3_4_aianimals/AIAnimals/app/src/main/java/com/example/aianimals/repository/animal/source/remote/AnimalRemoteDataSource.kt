package com.example.aianimals.repository.animal.source.remote

import android.util.Log
import androidx.annotation.VisibleForTesting
import com.example.aianimals.middleware.AppExecutors
import com.example.aianimals.repository.animal.Animal
import com.example.aianimals.repository.animal.source.AnimalCategory
import com.example.aianimals.repository.animal.source.AnimalDataSource
import com.example.aianimals.repository.animal.source.AnimalMetadata
import com.example.aianimals.repository.animal.source.AnimalSubcategory
import kotlinx.coroutines.withContext
import java.util.*

class AnimalRemoteDataSource private constructor(
    val appExecutors: AppExecutors,
    val animalAPI: AnimalAPIInterface
) : AnimalDataSource {
    private val TAG = AnimalRemoteDataSource::class.java.simpleName

    private var token: String? = null

    fun setToken(token: String?) {
        this.token = token
    }

    override suspend fun createAnimals() {}

    override suspend fun listAnimals(query: String?): Map<String, Animal> {
        if (token == null) {
            return mapOf()
        }
        val animals = mutableMapOf<String, Animal>()
        withContext(appExecutors.ioContext) {
            val phrases = mutableListOf<String>()
            if (query != null) {
                phrases.addAll(query.split(" "))
            }
            val animalSearchPost = AnimalSearchPost(
                animalCategoryNameEn = null,
                animalCategoryNameJa = null,
                animalSubcategoryNameEn = null,
                animalSubcategoryNameJa = null,
                phrases = phrases
            )
            val response = animalAPI.postSearchAnimal(
                token!!,
                100,
                0,
                animalSearchPost,
            )
            response.body()!!.results.forEach {
                animals[it.id] = Animal(
                    id = it.id,
                    name = it.name,
                    description = it.description,
                    date = it.created_at,
                    likes = 0,
                    imageUrl = it.photoUrl
                )
            }
        }
        return animals
    }

    override suspend fun getAnimal(animalID: String): Animal? {
        if (token == null) {
            return null
        }
        var animal: Animal? = null
        withContext(appExecutors.ioContext) {
            val response = animalAPI.getAnimal(token!!, animalID, false, 1, 0)
            if (response.isSuccessful) {
                val body = response.body()!!
                if (body.isEmpty()) {
                    return@withContext
                }
                animal = Animal(
                    id = body[0].id,
                    name = body[0].name,
                    description = body[0].description,
                    date = body[0].created_at,
                    likes = body[0].like,
                    imageUrl = body[0].photoUrl
                )
            }
        }
        return animal
    }

    override suspend fun saveAnimal(animal: Animal) {
        TODO("Not yet implemented")
    }

    override suspend fun getMetadata(): AnimalMetadata? {
        if (token == null) {
            return null
        }
        var animalMetadata: AnimalMetadata? = null
        withContext(appExecutors.ioContext) {
            val response = animalAPI.getMetadata(token!!)
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
                animalMetadata = AnimalMetadata(
                    animalCategoryMap = animalCategory,
                    animalSubcategoryMap = animalSubcategory
                )
            }
        }
        if (animalMetadata != null) {
            return animalMetadata
        }
        Log.e(TAG, "failed to get metadata")
        return null
    }

    companion object {
        private var INSTANCE: AnimalRemoteDataSource? = null

        @JvmStatic
        fun getInstance(
            appExecutors: AppExecutors,
            animalAPI: AnimalAPIInterface
        ): AnimalRemoteDataSource {
            if (INSTANCE == null) {
                synchronized(AnimalRemoteDataSource::javaClass) {
                    INSTANCE = AnimalRemoteDataSource(appExecutors, animalAPI)
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