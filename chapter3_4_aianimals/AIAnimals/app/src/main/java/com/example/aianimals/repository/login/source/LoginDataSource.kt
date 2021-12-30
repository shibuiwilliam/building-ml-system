package com.example.aianimals.repository.login.source

import com.example.aianimals.repository.login.Login

interface LoginDataSource {
    fun login(
        userID: String,
        password: String
    ): Result<Login>

    fun logout()
}