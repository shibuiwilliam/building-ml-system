package com.example.aianimals.repository.source.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.example.aianimals.repository.Animal

@Dao
interface AnimalDao {
    @Query("SELECT * FROM animals") fun listAnimals(): List<Animal>
    @Query("SELECT * FROM animals WHERE id = :animalID") fun getAnimal(animalID: String): Animal?
    @Insert(onConflict = OnConflictStrategy.REPLACE) fun insertAnimal(animal: Animal)
}