package com.example.aianimals.repository.animal.source.local

import android.util.Log
import androidx.annotation.VisibleForTesting
import com.example.aianimals.middleware.AppExecutors
import com.example.aianimals.middleware.Utils
import com.example.aianimals.repository.animal.*
import com.example.aianimals.repository.animal.Animal
import com.example.aianimals.repository.animal.source.AnimalDataSource
import kotlinx.coroutines.withContext
import java.text.SimpleDateFormat
import java.util.*

class AnimalLocalDataSource private constructor(
    val appExecutors: AppExecutors,
    val animalDao: AnimalDao,
    val animalMetadataDao: AnimalMetadataDao
) : AnimalDataSource {
    private val TAG = AnimalLocalDataSource::class.java.simpleName

    override suspend fun createAnimals() {
        for (i in 0..20) {
            val id = Utils.generateUUID()
            val animal = Animal(
                id,
                "ネコ",
                "かわいい",
                0,
                "https://storage.googleapis.com/aianimals/images/0016e503d29a4be9a4b852f2a5b44525.jpg",
                "2020/11/24",
            )
            saveAnimal(animal)
            Log.i("AnimalRepository", "animal: $animal")
        }
    }

    override suspend fun listAnimals(
        animalCategoryNameEn: String?,
        animalCategoryNameJa: String?,
        animalSubcategoryNameEn: String?,
        animalSubcategoryNameJa: String?,
        query: String?,
        sortBy: String,
        offset: Int
    ): Animals {
        val animals = mutableListOf<Animal>()
        withContext(appExecutors.ioContext) {
            val count = animalDao.countAnimals()
            if (count == 0) {
                Log.i(TAG, "add pseudo animals")
                createAnimals()
            }
            val localAnimals = animalDao.listAnimals()
            withContext(appExecutors.defaultContext) {
                if (localAnimals.isNotEmpty()) {
                    localAnimals.forEach { it ->
                        animals.add(
                            Animal(
                                it.id,
                                it.name,
                                it.description,
                                it.like,
                                it.photoUrl,
                                it.created_at
                            )
                        )
                    }
                }
            }
        }
        return Animals(
            animals,
            animals.size,
            "",
            sortBy,
            null
        )
    }

    override suspend fun searchAnimalsByImage(animalID: String): Animals {
        val animals = mutableListOf<Animal>()
        withContext(appExecutors.ioContext) {
            val localAnimals = animalDao.listAnimals()
            withContext(appExecutors.defaultContext) {
                if (localAnimals.isNotEmpty()) {
                    localAnimals.forEach { it ->
                        animals.add(
                            Animal(
                                it.id,
                                it.name,
                                it.description,
                                it.like,
                                it.photoUrl,
                                it.created_at
                            )
                        )
                    }
                }
            }
        }
        return Animals(
            animals,
            animals.size,
            "",
            "image_similarity",
            null
        )
    }

    override suspend fun getAnimal(animalID: String): Animal? {
        var animal: Animal? = null
        withContext(appExecutors.ioContext) {
            val localAnimal = animalDao.getAnimal(animalID)
            if (localAnimal != null) {
                animal = Animal(
                    localAnimal.id,
                    localAnimal.name,
                    localAnimal.description,
                    localAnimal.like,
                    localAnimal.photoUrl,
                    SimpleDateFormat("yyyy/MM/dd").format(Date()).toString(),
                )
            }
        }
        return animal
    }

    override suspend fun saveAnimal(animal: Animal) {
        val localAnimal = com.example.aianimals.repository.animal.source.local.Animal(
            animal.id,
            animal.name,
            animal.description,
            animal.like,
            animal.photoUrl,
            animal.created_at,
        )
        withContext(appExecutors.ioContext) {
            animalDao.insertAnimal(localAnimal)
        }
    }

    override suspend fun loadAnimalMetadata(refresh: Boolean) {}

    override suspend fun listAnimalCategory(): List<AnimalCategory> {
        return animalMetadataDao.listAnimalCategories()
    }

    override suspend fun listAnimalSubcategory(
        animalCategoryNameEn: String?,
        animalCategoryNameJa: String?
    ): List<AnimalSubcategory> {
        if (animalCategoryNameEn == null && animalCategoryNameJa == null) {
            return animalMetadataDao.listAnimalSubcategories()
        } else if (animalCategoryNameEn != null && animalCategoryNameJa != null) {
            throw IllegalArgumentException("")
        }
        if (animalCategoryNameEn != null) {
            return animalMetadataDao.listAnimalSubcategoryByAnimalCategoryNameEn(
                animalCategoryNameEn
            )
        }
        if (animalCategoryNameJa != null) {
            return animalMetadataDao.listAnimalSubcategoryByAnimalCategoryNameJa(
                animalCategoryNameJa
            )
        }
        return listOf()
    }

    override suspend fun listAnimalSearchSortKey(): List<AnimalSearchSortKey> {
        return animalMetadataDao.listAnimalAnimalSearchSortKey()
    }

    override suspend fun getAnimalCategory(
        nameEn: String?,
        nameJa: String?
    ): AnimalCategory? {
        if ((nameEn == null && nameJa == null) || (nameEn != null && nameJa != null)) {
            throw IllegalArgumentException("")
        }
        if (nameEn != null) {
            return animalMetadataDao.getAnimalCategoryByNameEn(nameEn)
        }
        if (nameJa != null) {
            return animalMetadataDao.getAnimalCategoryByNameJa(nameJa)
        }
        return null
    }

    override suspend fun getAnimalSubcategory(
        nameEn: String?,
        nameJa: String?
    ): AnimalSubcategory? {
        if ((nameEn == null && nameJa == null) || (nameEn != null && nameJa != null)) {
            throw IllegalArgumentException("")
        }
        if (nameEn != null) {
            return animalMetadataDao.getAnimalSubcategoryByNameEn(nameEn)
        }
        if (nameJa != null) {
            return animalMetadataDao.getAnimalSubcategoryByNameJa(nameJa)
        }
        return null
    }

    override suspend fun likeAnimal(animalID: String) {
        TODO("Not yet implemented")
    }

    suspend fun saveAnimalMetadata(
        animalCategories: List<AnimalCategory>,
        animalSubcategories: List<AnimalSubcategory>,
        animalSearchSortKeys: List<AnimalSearchSortKey>
    ) {
        withContext(appExecutors.ioContext) {
            animalMetadataDao.deleteAllAnimalCategory()
            animalMetadataDao.deleteAllAnimalSubcategory()
            animalMetadataDao.deleteAllAnimalSearchSortKey()
            animalMetadataDao.bulkInsertAnimalCategory(animalCategories)
            animalMetadataDao.bulkInsertAnimalSubcategory(animalSubcategories)
            animalMetadataDao.bulkInsertAnimalSearchSortKey(animalSearchSortKeys)
        }
    }

    companion object {
        private var INSTANCE: AnimalLocalDataSource? = null

        @JvmStatic
        fun getInstance(
            appExecutors: AppExecutors,
            animalDao: AnimalDao,
            animalMetadataDao: AnimalMetadataDao
        ): AnimalLocalDataSource {
            if (INSTANCE == null) {
                synchronized(AnimalLocalDataSource::javaClass) {
                    INSTANCE = AnimalLocalDataSource(
                        appExecutors,
                        animalDao,
                        animalMetadataDao
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