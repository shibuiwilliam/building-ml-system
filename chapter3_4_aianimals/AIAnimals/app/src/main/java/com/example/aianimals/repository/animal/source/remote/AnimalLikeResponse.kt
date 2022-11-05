package com.example.aianimals.repository.animal.source.remote

data class AnimalLikeResponse(
    val id: String,
    val animalID: String,
    val userID: String,
    val created_at: String,
    val updated_at: String
)
