package com.example.aianimals.repository.access_log

data class AccessLog(
    val phrases: List<String>,
    val animalCategoryID: Int?,
    val animalSubcategoryID: Int?,
    val animalID: String,
    val action: String
)
