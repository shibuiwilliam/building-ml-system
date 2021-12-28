package com.example.aianimals

import android.content.Context
import com.example.aianimals.middleware.AppExecutors
import com.example.aianimals.repository.source.AnimalRepository
import com.example.aianimals.repository.source.local.AnimalDatabase
import com.example.aianimals.repository.source.local.AnimalLocalDataSource

object Injection {
    fun provideAnimalRepository(context: Context): AnimalRepository {
        val database = AnimalDatabase.getInstance(context)
        return AnimalRepository.getInstance(
            AnimalLocalDataSource.getInstance(
                AppExecutors(),
                database.animalDao()
            )
        )
    }
}