package com.example.aianimals.repository.animal.source.remote

import androidx.annotation.VisibleForTesting
import com.example.aianimals.middleware.AppExecutors
import com.example.aianimals.repository.animal.Animal
import com.example.aianimals.repository.animal.AnimalCategory
import com.example.aianimals.repository.animal.AnimalSubcategory
import com.example.aianimals.repository.animal.source.AnimalDataSource
import kotlinx.coroutines.withContext
import java.util.*

class AnimalRemoteDataSource private constructor(
    val appExecutors: AppExecutors,
    val animalAPI: AnimalAPIInterface
) : AnimalDataSource {
    private val TAG = AnimalRemoteDataSource::class.java.simpleName

    private var token: String? = null
    private var userID: String? = null

    fun setToken(token: String?) {
        this.token = token
    }

    fun setUserID(userID: String?) {
        this.userID = userID
    }

    override suspend fun createAnimals() {}

    override suspend fun listAnimals(
        animalCategoryNameEn: String?,
        animalCategoryNameJa: String?,
        animalSubcategoryNameEn: String?,
        animalSubcategoryNameJa: String?,
        query: String?,
        offset: Int
    ): Map<String, Animal> {
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
                animalCategoryNameEn = animalCategoryNameEn,
                animalCategoryNameJa = animalCategoryNameJa,
                animalSubcategoryNameEn = animalSubcategoryNameEn,
                animalSubcategoryNameJa = animalSubcategoryNameJa,
                phrases = phrases
            )
            val response = animalAPI.postSearchAnimal(
                token!!,
                100,
                offset,
                animalSearchPost,
            )
            response.body()!!.results.forEach {
                animals[it.id] = Animal(
                    id = it.id,
                    name = it.name,
                    description = it.description,
                    date = it.created_at,
                    likes = it.likes,
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
                    likes = body[0].likes,
                    imageUrl = body[0].photoUrl
                )
            }
        }
        return animal
    }

    override suspend fun saveAnimal(animal: Animal) {}

    override suspend fun loadAnimalMetadata(refresh: Boolean) {}

    override suspend fun listAnimalCategory(): List<AnimalCategory> {
        TODO("Not yet implemented")
    }

    override suspend fun listAnimalSubcategory(
        animalCategoryNameEn: String?,
        animalCategoryNameJa: String?
    ): List<AnimalSubcategory> {
        TODO("Not yet implemented")
    }

    override suspend fun getAnimalCategory(nameEn: String?, nameJa: String?): AnimalCategory? {
        TODO("Not yet implemented")
    }

    override suspend fun getAnimalSubcategory(
        nameEn: String?,
        nameJa: String?
    ): AnimalSubcategory? {
        TODO("Not yet implemented")
    }

    override suspend fun likeAnimal(animalID: String) {
        if (token == null || userID == null) {
            return
        }
        withContext(appExecutors.ioContext) {
            animalAPI.postLikeAnimal(
                token!!,
                AnimalLikePost(
                    animalID,
                    userID!!
                )
            )
        }
    }

    suspend fun requestAnimalMetadata(): MetadataResponse? {
        if (token == null) {
            return null
        }
        var body: MetadataResponse? = null
        withContext(appExecutors.ioContext) {
            val response = animalAPI.getMetadata(token!!)
            if (response.isSuccessful) {
                body = response.body()!!
            }
        }
        return body
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
                    INSTANCE = AnimalRemoteDataSource(
                        appExecutors,
                        animalAPI
                    )
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