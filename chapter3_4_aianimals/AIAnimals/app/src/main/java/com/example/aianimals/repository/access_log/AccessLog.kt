package com.example.aianimals.repository.access_log

data class AccessLog(
    val searchID: String,
    val phrases: List<String>,
    val animalCategoryID: Int?,
    val animalSubcategoryID: Int?,
    val sortBy: String,
    val modelName: String?,
    val animalID: String,
    val action: String,
)
