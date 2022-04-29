package com.example.aianimals.repository.access_log.source.remote

data class AccessLogPost(
    val searchId: String,
    val phrases: List<String>,
    val animalCategoryId: Int?,
    val animalSubcategoryId: Int?,
    val sortBy: String,
    val modelName: String?,
    val animalId: String,
    val action: String
)
