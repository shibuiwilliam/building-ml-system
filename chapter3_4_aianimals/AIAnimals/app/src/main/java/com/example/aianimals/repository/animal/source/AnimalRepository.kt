package com.example.aianimals.repository.animal.source


import android.util.Log
import com.example.aianimals.BuildConfig
import com.example.aianimals.repository.animal.Animal
import com.example.aianimals.repository.animal.AnimalCategory
import com.example.aianimals.repository.animal.AnimalSearchSortKey
import com.example.aianimals.repository.animal.AnimalSubcategory
import com.example.aianimals.repository.animal.source.local.AnimalLocalDataSource
import com.example.aianimals.repository.animal.source.remote.AnimalRemoteDataSource

class AnimalRepository(
    val animalLocalDataSource: AnimalLocalDataSource,
    val animalRemoteDataSource: AnimalRemoteDataSource
) : AnimalDataSource {
    private val TAG = AnimalRepository::class.java.simpleName

    override suspend fun createAnimals() {}

    override suspend fun listAnimals(
        animalCategoryNameEn: String?,
        animalCategoryNameJa: String?,
        animalSubcategoryNameEn: String?,
        animalSubcategoryNameJa: String?,
        query: String?,
        sortBy: String,
        offset: Int
    ): Map<String, Animal> {
        if (BuildConfig.USE_LOCAL_DATA) {
            val localAnimals = animalLocalDataSource.listAnimals(
                animalCategoryNameEn,
                animalCategoryNameJa,
                animalSubcategoryNameEn,
                animalSubcategoryNameJa,
                query,
                sortBy,
                offset
            )
            if (localAnimals.isNotEmpty()) {
                return localAnimals
            }
        }

        val remoteAnimals = animalRemoteDataSource.listAnimals(
            animalCategoryNameEn,
            animalCategoryNameJa,
            animalSubcategoryNameEn,
            animalSubcategoryNameJa,
            query,
            sortBy,
            offset
        )
        if (remoteAnimals.isNotEmpty()) {
            return remoteAnimals
        }
        return mapOf()
    }

    override suspend fun getAnimal(animalID: String): Animal? {
        if (BuildConfig.USE_LOCAL_DATA) {
            return animalLocalDataSource.getAnimal(animalID)
        }
        return animalRemoteDataSource.getAnimal(animalID)
    }

    override suspend fun saveAnimal(animal: Animal) {
        Log.i("AnimalRepository", "register ${animal}")
        if (BuildConfig.USE_LOCAL_DATA) {
            animalLocalDataSource.saveAnimal(animal)
        }
        animalRemoteDataSource.saveAnimal(animal)
    }

    override suspend fun loadAnimalMetadata(refresh: Boolean) {
        if (refresh) {
            val animalMetadata = animalRemoteDataSource.requestAnimalMetadata()
            if (animalMetadata != null) {
                val animalCategories = animalMetadata.animalCategory.map {
                    AnimalCategory(
                        id = it.id,
                        nameEn = it.nameEn,
                        nameJa = it.nameJa
                    )
                }
                val animalSubcategories = animalMetadata.animalSubcategory.map {
                    AnimalSubcategory(
                        id = it.id,
                        animalCategoryId = it.animalCategoryId,
                        nameEn = it.nameEn,
                        nameJa = it.nameJa
                    )
                }
                val animalSearchSortKeys = animalMetadata.animalSearchSortKey.map {
                    AnimalSearchSortKey(name = it)
                }
                animalLocalDataSource.saveAnimalMetadata(
                    animalCategories,
                    animalSubcategories,
                    animalSearchSortKeys
                )
            }
        }
    }

    override suspend fun listAnimalCategory(): List<AnimalCategory> {
        var data = animalLocalDataSource.listAnimalCategory()
        if (data.isEmpty()) {
            loadAnimalMetadata(true)
            data = animalLocalDataSource.listAnimalCategory()
        }
        return data
    }

    override suspend fun listAnimalSubcategory(
        animalCategoryNameEn: String?,
        animalCategoryNameJa: String?
    ): List<AnimalSubcategory> {
        var data = animalLocalDataSource.listAnimalSubcategory(
            animalCategoryNameEn,
            animalCategoryNameJa
        )
        if (data.isEmpty()) {
            loadAnimalMetadata(true)
            data = animalLocalDataSource.listAnimalSubcategory(
                animalCategoryNameEn,
                animalCategoryNameJa
            )
        }
        return data
    }

    override suspend fun listAnimalSearchSortKey(): List<AnimalSearchSortKey> {
        var data = animalLocalDataSource.listAnimalSearchSortKey()
        if (data.isEmpty()) {
            loadAnimalMetadata(true)
            data = animalLocalDataSource.listAnimalSearchSortKey()
        }
        return data
    }

    override suspend fun getAnimalCategory(
        nameEn: String?,
        nameJa: String?
    ): AnimalCategory? {
        val data = animalLocalDataSource.getAnimalCategory(nameEn, nameJa)
        if (data != null) {
            return data
        }
        return animalRemoteDataSource.getAnimalCategory(nameEn, nameJa)
    }

    override suspend fun getAnimalSubcategory(
        nameEn: String?,
        nameJa: String?
    ): AnimalSubcategory? {
        val data = animalLocalDataSource.getAnimalSubcategory(nameEn, nameJa)
        if (data != null) {
            return data
        }
        return animalRemoteDataSource.getAnimalSubcategory(nameEn, nameJa)
    }

    override suspend fun likeAnimal(animalID: String) {
        animalRemoteDataSource.likeAnimal(animalID)
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