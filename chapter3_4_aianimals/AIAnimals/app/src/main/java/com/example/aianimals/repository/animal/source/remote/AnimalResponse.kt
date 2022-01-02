package com.example.aianimals.repository.animal.source.remote

data class AnimalResponse(
    val id: String,
    val name: String,
    val description: String,
    val photoUrl: String,
    val like: Int,
    val animalCategoryNameEn: String,
    val animalCategoryNameJa: String,
    val animalSubcategoryNameEn: String,
    val animalSubcategoryNameJa: String,
    val userHandleName: String,
    val created_at: String
)
