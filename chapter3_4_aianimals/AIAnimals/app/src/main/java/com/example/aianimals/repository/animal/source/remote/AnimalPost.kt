package com.example.aianimals.repository.animal.source.remote

data class AnimalPost(
    val animalCategoryId: Int,
    val animalSubcategoryId: Int,
    val userId: String,
    val name: String,
    val description: String
)