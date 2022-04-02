package com.example.aianimals.repository.animal

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.PrimaryKey

@Entity(tableName = "animal_categories")
data class AnimalCategory @JvmOverloads constructor(
    @PrimaryKey @ColumnInfo(name = "id") var id: Int,
    @ColumnInfo(name = "nameEn", index = true) var nameEn: String,
    @ColumnInfo(name = "nameJa", index = true) var nameJa: String,
)

@Entity(
    tableName = "animal_subcategories",
    foreignKeys = [ForeignKey(
        entity = AnimalCategory::class,
        parentColumns = arrayOf("id"),
        childColumns = arrayOf("animalCategoryId"),
        onDelete = ForeignKey.CASCADE
    )]
)
data class AnimalSubcategory @JvmOverloads constructor(
    @PrimaryKey @ColumnInfo(name = "id") var id: Int,
    @ColumnInfo(name = "animalCategoryId", index = true) var animalCategoryId: Int,
    @ColumnInfo(name = "nameEn", index = true) var nameEn: String,
    @ColumnInfo(name = "nameJa", index = true) var nameJa: String,
)

@Entity(tableName = "animal_search_sort_keys")
data class AnimalSearchSortKey @JvmOverloads constructor(
    @PrimaryKey @ColumnInfo(name = "name") var name: String,
)
