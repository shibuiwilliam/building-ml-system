package com.example.aianimals.repository.login.source.local

import androidx.annotation.VisibleForTesting
import com.example.aianimals.repository.login.Login
import com.example.aianimals.repository.login.source.LoginDataSource
import com.example.aianimals.repository.login.source.Result

class LoginLocalDataSource private constructor() : LoginDataSource {
    private val TAG = LoginLocalDataSource::class.java.simpleName

    override fun login(
        id: String,
        password: String,
    ): Result<Login> {
        return Result.Success(Login(userID = "a", displayName = "b"))
    }

    companion object {
        private var INSTANCE: LoginLocalDataSource? = null

        @JvmStatic
        fun getInstance(): LoginLocalDataSource {
            if (INSTANCE == null) {
                synchronized(LoginLocalDataSource::javaClass) {
                    INSTANCE = LoginLocalDataSource()
                }
            }
            return INSTANCE!!
        }

        @VisibleForTesting
        fun clearInstance() {
            INSTANCE = null
        }
    }
}