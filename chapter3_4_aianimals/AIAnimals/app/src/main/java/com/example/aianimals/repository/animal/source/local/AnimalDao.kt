package com.example.aianimals.repository.animal.source.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query

@Dao
interface AnimalDao {
    @Query("SELECT COUNT(*) FROM animals")
    fun countAnimals(): Int

    @Query("SELECT * FROM animals")
    fun listAnimals(): List<Animal>

    @Query("SELECT * FROM animals WHERE id = :animalID")
    fun getAnimal(animalID: String): Animal?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    fun insertAnimal(animal: Animal)
}