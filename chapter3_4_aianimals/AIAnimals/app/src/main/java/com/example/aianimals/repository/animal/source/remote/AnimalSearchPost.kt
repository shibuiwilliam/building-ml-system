package com.example.aianimals.repository.animal.source.remote

data class AnimalSearchPost(
    val animalCategoryNameEn: String?,
    val animalCategoryNameJa: String?,
    val animalSubcategoryNameEn: String?,
    val animalSubcategoryNameJa: String?,
    val phrases: List<String>
)
