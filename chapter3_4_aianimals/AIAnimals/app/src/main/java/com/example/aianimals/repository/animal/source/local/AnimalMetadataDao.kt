package com.example.aianimals.repository.animal.source.local

import androidx.room.*
import com.example.aianimals.repository.animal.AnimalCategory
import com.example.aianimals.repository.animal.AnimalSubcategory

@Dao
interface AnimalMetadataDao {
    @Query("SELECT * FROM animal_categories")
    fun listAnimalCategories(): List<AnimalCategory>

    @Query("SELECT * FROM animal_subcategories")
    fun listAnimalSubcategories(): List<AnimalSubcategory>

    @Query("SELECT * FROM animal_categories WHERE nameEn = :nameEn")
    fun getAnimalCategoryByNameEn(nameEn: String): AnimalCategory?

    @Query("SELECT * FROM animal_categories WHERE nameJa = :nameJa")
    fun getAnimalCategoryByNameJa(nameJa: String): AnimalCategory?

    @Query("SELECT * FROM animal_subcategories WHERE nameEn = :nameEn")
    fun getAnimalSubcategoryByNameEn(nameEn: String): AnimalSubcategory?

    @Query("SELECT * FROM animal_subcategories WHERE nameJa = :nameJa")
    fun getAnimalSubcategoryByNameJa(nameJa: String): AnimalSubcategory?

    @Query("SELECT * FROM animal_subcategories s LEFT JOIN animal_categories c ON s.animalCategoryId = c.id WHERE c.nameEn = :nameEn")
    fun listAnimalSubcategoryByAnimalCategoryNameEn(nameEn: String): List<AnimalSubcategory>

    @Query("SELECT * FROM animal_subcategories s LEFT JOIN animal_categories c ON s.animalCategoryId = c.id WHERE c.nameJa = :nameJa")
    fun listAnimalSubcategoryByAnimalCategoryNameJa(nameJa: String): List<AnimalSubcategory>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    fun insertAnimalCategory(animalCategory: AnimalCategory)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    fun insertAnimalSubcategory(animalSubcategory: AnimalSubcategory)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    fun bulkInsertAnimalCategory(animalCategories: List<AnimalCategory>)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    fun bulkInsertAnimalSubcategory(animalSubcategories: List<AnimalSubcategory>)

    @Delete
    fun deleteAnimalCategory(animalCategory: AnimalCategory)

    @Delete
    fun deleteAnimalSubcategory(animalSubcategory: AnimalSubcategory)

    @Query("DELETE FROM animal_categories")
    fun deleteAllAnimalCategory()

    @Query("DELETE FROM animal_subcategories")
    fun deleteAllAnimalSubcategory()
}