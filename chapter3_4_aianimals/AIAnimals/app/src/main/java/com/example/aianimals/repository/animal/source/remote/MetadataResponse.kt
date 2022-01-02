package com.example.aianimals.repository.animal.source.remote

data class AnimalCategoryResponse(
    val id: Int,
    val nameEn: String,
    val nameJa: String,
    val isDeleted: Boolean,
    val createdAt: String,
    val updatedAt: String
)

data class AnimalSubcategoryResponse(
    val id: Int,
    val animalCategoryId: Int,
    val animalCategoryNameEn: String,
    val animalCategoryNameJa: String,
    val nameEn: String,
    val nameJa: String,
    val isDeleted: Boolean,
    val createdAt: String,
    val updatedAt: String
)

data class MetadataResponse(
    val animalCategory: List<AnimalCategoryResponse>,
    val animalSubcategory: List<AnimalSubcategoryResponse>,
)
