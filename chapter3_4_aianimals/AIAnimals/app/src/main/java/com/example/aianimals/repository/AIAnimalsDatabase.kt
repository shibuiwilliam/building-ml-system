package com.example.aianimals.repository

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import androidx.room.TypeConverters
import com.example.aianimals.middleware.Converters
import com.example.aianimals.repository.animal.AnimalCategory
import com.example.aianimals.repository.animal.AnimalSearchSortKey
import com.example.aianimals.repository.animal.AnimalSubcategory
import com.example.aianimals.repository.animal.source.local.Animal
import com.example.aianimals.repository.animal.source.local.AnimalDao
import com.example.aianimals.repository.animal.source.local.AnimalMetadataDao
import com.example.aianimals.repository.login.Login
import com.example.aianimals.repository.login.source.local.LoginDao


@Database(
    entities = [
        Login::class,
        Animal::class,
        AnimalCategory::class,
        AnimalSubcategory::class,
        AnimalSearchSortKey::class
    ],
    version = 3,
    exportSchema = false
)
@TypeConverters(Converters::class)
abstract class AIAnimalsDatabase : RoomDatabase() {
    abstract fun loginDao(): LoginDao
    abstract fun animalDao(): AnimalDao
    abstract fun animalMetadataDao(): AnimalMetadataDao

    companion object {
        private var INSTANCE: AIAnimalsDatabase? = null
        private val lock = Any()

        fun getInstance(context: Context): AIAnimalsDatabase {
            synchronized(lock) {
                if (INSTANCE == null) {
                    INSTANCE = Room.databaseBuilder(
                        context.applicationContext,
                        AIAnimalsDatabase::class.java,
                        "AIAnimals.db"
                    )
                        .fallbackToDestructiveMigration()
                        .build()
                }
                return INSTANCE!!
            }
        }
    }
}