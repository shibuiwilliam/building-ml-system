package com.example.aianimals

import android.content.Context
import com.example.aianimals.middleware.AppExecutors
import com.example.aianimals.repository.animal.source.AnimalRepository
import com.example.aianimals.repository.animal.source.local.AnimalDatabase
import com.example.aianimals.repository.animal.source.local.AnimalLocalDataSource
import com.example.aianimals.repository.login.source.LoginRepository
import com.example.aianimals.repository.login.source.local.LoginLocalDataSource

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

    fun provideLoginRepository(context: Context): LoginRepository {
        return LoginRepository.getInstance(
            LoginLocalDataSource.getInstance()
        )
    }
}