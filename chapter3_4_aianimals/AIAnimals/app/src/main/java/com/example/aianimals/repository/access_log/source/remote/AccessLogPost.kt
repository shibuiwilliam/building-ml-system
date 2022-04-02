package com.example.aianimals.repository.access_log.source.remote

data class AccessLogPost(
    val phrases: List<String>,
    val animalCategoryID: Int,
    val animalSubcategoryID: Int,
    val animalID: String,
    val action: String
)
