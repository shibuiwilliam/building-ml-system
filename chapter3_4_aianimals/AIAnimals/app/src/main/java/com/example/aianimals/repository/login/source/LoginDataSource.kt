package com.example.aianimals.repository.login.source

import com.example.aianimals.repository.login.Login

interface LoginDataSource {
    suspend fun login(
        handleName: String,
        password: String
    ): Result<Login>

    suspend fun logout()

    suspend fun isLoggedIn(): Login?
}