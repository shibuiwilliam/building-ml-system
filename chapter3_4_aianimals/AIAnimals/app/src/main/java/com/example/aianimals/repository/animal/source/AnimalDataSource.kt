package com.example.aianimals.repository.animal.source

import com.example.aianimals.repository.animal.Animal
import com.example.aianimals.repository.animal.AnimalCategory
import com.example.aianimals.repository.animal.AnimalSearchSortKey
import com.example.aianimals.repository.animal.AnimalSubcategory

interface AnimalDataSource {
    suspend fun createAnimals()
    suspend fun listAnimals(
        animalCategoryNameEn: String?,
        animalCategoryNameJa: String?,
        animalSubcategoryNameEn: String?,
        animalSubcategoryNameJa: String?,
        query: String?,
        sortBy: String,
        offset: Int
    ): Map<String, Animal>

    suspend fun searchAnimalsByImage(
        animalID: String
    ): Map<String, Animal>

    suspend fun getAnimal(animalID: String): Animal?
    suspend fun saveAnimal(animal: Animal)

    suspend fun loadAnimalMetadata(refresh: Boolean)
    suspend fun listAnimalCategory(): List<AnimalCategory>
    suspend fun listAnimalSubcategory(
        animalCategoryNameEn: String?,
        animalCategoryNameJa: String?
    ): List<AnimalSubcategory>

    suspend fun listAnimalSearchSortKey(): List<AnimalSearchSortKey>

    suspend fun getAnimalCategory(
        nameEn: String?,
        nameJa: String?
    ): AnimalCategory?

    suspend fun getAnimalSubcategory(
        nameEn: String?,
        nameJa: String?
    ): AnimalSubcategory?

    suspend fun likeAnimal(animalID: String)
}