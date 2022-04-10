package com.example.aianimals.repository.access_log.source.remote

data class AccessLogPost(
    val phrases: List<String>,
    val animalCategoryId: Int?,
    val animalSubcategoryId: Int?,
    val animalId: String,
    val action: String
)
