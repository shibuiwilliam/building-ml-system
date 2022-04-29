package com.example.aianimals.repository.animal

data class Animal(
    val id: String,
    val name: String,
    val description: String,
    val like: Int,
    val photoUrl: String,
    val created_at: String
)

data class Animals(
    val animals: List<Animal>,
    val size: Int,
    val searchID: String,
    val sortBy: String,
    val modelName: String?
)
