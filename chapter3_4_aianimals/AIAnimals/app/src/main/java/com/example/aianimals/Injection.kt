package com.example.aianimals

import android.content.Context
import com.example.aianimals.middleware.AppExecutors
import com.example.aianimals.repository.AIAnimalsDatabase
import com.example.aianimals.repository.animal.source.AnimalRepository
import com.example.aianimals.repository.animal.source.local.AnimalLocalDataSource
import com.example.aianimals.repository.animal.source.remote.AnimalAPIClient
import com.example.aianimals.repository.animal.source.remote.AnimalRemoteDataSource
import com.example.aianimals.repository.login.source.LoginRepository
import com.example.aianimals.repository.login.source.local.LoginLocalDataSource
import com.example.aianimals.repository.login.source.remote.LoginAPIClient
import com.example.aianimals.repository.login.source.remote.LoginRemoteDataSource

object Injection {
    fun provideAnimalRepository(context: Context): AnimalRepository {
        val database = AIAnimalsDatabase.getInstance(context)
        return AnimalRepository.getInstance(
            AnimalLocalDataSource.getInstance(
                AppExecutors(),
                database.animalDao()
            ),
            AnimalRemoteDataSource.getInstance(
                AnimalAPIClient.animalAPI
            )
        )
    }

    fun provideLoginRepository(context: Context): LoginRepository {
        val database = AIAnimalsDatabase.getInstance(context)
        return LoginRepository.getInstance(
            LoginLocalDataSource.getInstance(
                AppExecutors(),
                database.loginDao()
            ),
            LoginRemoteDataSource.getInstance(LoginAPIClient.loginAPI)
        )
    }
}