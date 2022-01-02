package com.example.aianimals.repository.animal.source.remote

data class AnimalSearchResult(
    val score: Float,
    val id: String,
    val name: String,
    val description: String,
    val photoUrl: String,
    val animalCategoryNameEn: String,
    val animalCategoryNameJa: String,
    val animalSubcategoryNameEn: String,
    val animalSubcategoryNameJa: String,
    val userHandleName: String
)

data class AnimalSearchResponse(
    val hits: Int,
    val maxScore: Float,
    val results: List<AnimalSearchResult>
)
