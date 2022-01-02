package com.example.aianimals.repository.login.source

import com.example.aianimals.repository.login.Login

interface LoginDataSource {
    fun login(
        handleName: String,
        password: String
    ): Result<Login>

    fun logout()
}