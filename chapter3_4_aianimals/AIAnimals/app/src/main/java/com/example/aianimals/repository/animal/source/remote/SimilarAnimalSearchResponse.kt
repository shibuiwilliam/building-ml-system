package com.example.aianimals.repository.animal.source.remote

data class SimilarAnimalSearchResult(
    val id: String,
    val name: String,
    val description: String,
    val photoUrl: String,
    val animalCategoryNameEn: String,
    val animalCategoryNameJa: String,
    val animalSubcategoryNameEn: String,
    val animalSubcategoryNameJa: String,
    val userHandleName: String,
    val like: Int,
    val created_at: String
)

data class SimilarAnimalSearchResponse(
    val results: List<SimilarAnimalSearchResult>,
    val searchId: String,
    val sortBy: String,
    val modelName: String?
)
