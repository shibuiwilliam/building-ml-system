package com.example.aianimals.repository.animal.source.remote

data class AnimalPost(
    val animalCategoryID: Int,
    val animalSubcategoryID: Int,
    val userID: String,
    val name: String,
    val description: String
)