package com.example.aianimals.repository.animal.source.local

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import com.example.aianimals.repository.animal.Animal

@Database(
    entities = [Animal::class],
    version = 3,
    exportSchema = false
)
abstract class AnimalDatabase : RoomDatabase() {
    abstract fun animalDao(): AnimalDao

    companion object {
        private var INSTANCE: AnimalDatabase? = null
        private val lock = Any()

        fun getInstance(context: Context): AnimalDatabase {
            synchronized(lock) {
                if (INSTANCE == null) {
                    INSTANCE = Room.databaseBuilder(
                        context.applicationContext,
                        AnimalDatabase::class.java,
                        "Animals.db"
                    )
                        .fallbackToDestructiveMigration()
                        .build()
                }
                return INSTANCE!!
            }
        }
    }
}