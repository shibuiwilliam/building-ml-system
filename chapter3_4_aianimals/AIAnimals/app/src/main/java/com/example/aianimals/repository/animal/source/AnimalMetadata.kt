package com.example.aianimals.repository.animal.source


data class AnimalCategory(
    val id: Int,
    val nameEn: String,
    val nameJa: String,
)

data class AnimalSubcategory(
    val id: Int,
    val animalCategoryId: Int,
    val animalCategoryNameEn: String,
    val animalCategoryNameJa: String,
    val nameEn: String,
    val nameJa: String,
)

data class AnimalMetadata(
    val animalCategoryMap: Map<Int, AnimalCategory>,
    val animalSubcategoryMap: Map<Int, Map<Int, AnimalSubcategory>>,
)
