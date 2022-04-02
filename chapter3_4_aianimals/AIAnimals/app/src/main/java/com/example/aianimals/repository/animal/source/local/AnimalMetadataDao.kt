package com.example.aianimals.repository.animal.source.local

import androidx.room.*
import com.example.aianimals.repository.animal.AnimalCategory
import com.example.aianimals.repository.animal.AnimalSearchSortKey
import com.example.aianimals.repository.animal.AnimalSubcategory

@Dao
interface AnimalMetadataDao {
    @Query("SELECT * FROM animal_categories")
    fun listAnimalCategories(): List<AnimalCategory>

    @Query("SELECT * FROM animal_subcategories")
    fun listAnimalSubcategories(): List<AnimalSubcategory>

    @Query("SELECT * FROM animal_search_sort_keys")
    fun listAnimalAnimalSearchSortKey(): List<AnimalSearchSortKey>

    @Query("SELECT * FROM animal_categories WHERE nameEn = :nameEn")
    fun getAnimalCategoryByNameEn(nameEn: String): AnimalCategory?

    @Query("SELECT * FROM animal_categories WHERE nameJa = :nameJa")
    fun getAnimalCategoryByNameJa(nameJa: String): AnimalCategory?

    @Query("SELECT * FROM animal_subcategories WHERE nameEn = :nameEn")
    fun getAnimalSubcategoryByNameEn(nameEn: String): AnimalSubcategory?

    @Query("SELECT * FROM animal_subcategories WHERE nameJa = :nameJa")
    fun getAnimalSubcategoryByNameJa(nameJa: String): AnimalSubcategory?

    @Query(
        "SELECT s.id,s.animalCategoryId,s.nameEn,s.nameJa " +
                "FROM animal_subcategories s " +
                "LEFT JOIN animal_categories c ON s.animalCategoryId = c.id " +
                "WHERE c.nameEn = :nameEn"
    )
    fun listAnimalSubcategoryByAnimalCategoryNameEn(nameEn: String): List<AnimalSubcategory>

    @Query(
        "SELECT s.id,s.animalCategoryId,s.nameEn,s.nameJa " +
                "FROM animal_subcategories s " +
                "LEFT JOIN animal_categories c ON s.animalCategoryId = c.id " +
                "WHERE c.nameJa = :nameJa"
    )
    fun listAnimalSubcategoryByAnimalCategoryNameJa(nameJa: String): List<AnimalSubcategory>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    fun insertAnimalCategory(animalCategory: AnimalCategory)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    fun insertAnimalSubcategory(animalSubcategory: AnimalSubcategory)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    fun insertAnimalSearchSortKey(animalSearchSortKey: AnimalSearchSortKey)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    fun bulkInsertAnimalCategory(animalCategories: List<AnimalCategory>)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    fun bulkInsertAnimalSubcategory(animalSubcategories: List<AnimalSubcategory>)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    fun bulkInsertAnimalSearchSortKey(animalSearchSortKeys: List<AnimalSearchSortKey>)

    @Delete
    fun deleteAnimalCategory(animalCategory: AnimalCategory)

    @Delete
    fun deleteAnimalSubcategory(animalSubcategory: AnimalSubcategory)

    @Delete
    fun deleteAnimalMetadata(animalMetadata: AnimalSearchSortKey)

    @Query("DELETE FROM animal_categories")
    fun deleteAllAnimalCategory()

    @Query("DELETE FROM animal_subcategories")
    fun deleteAllAnimalSubcategory()

    @Query("DELETE FROM animal_search_sort_keys")
    fun deleteAllAnimalSearchSortKey()
}