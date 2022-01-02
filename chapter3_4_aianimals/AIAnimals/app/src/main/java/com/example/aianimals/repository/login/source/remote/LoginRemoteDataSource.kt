package com.example.aianimals.repository.login.source.remote

import androidx.annotation.VisibleForTesting
import com.example.aianimals.repository.login.Login
import com.example.aianimals.repository.login.source.LoginDataSource
import com.example.aianimals.repository.login.source.Result

class LoginRemoteDataSource private constructor(
    val loginAPI: LoginAPIInterface
) : LoginDataSource {
    private val TAG = LoginRemoteDataSource::class.java.simpleName

    override fun login(
        handleName: String,
        password: String
    ): Result<Login> {
        TODO("Not yet implemented")
    }

    override fun logout() {
        TODO("Not yet implemented")
    }

    companion object {
        private var INSTANCE: LoginRemoteDataSource? = null

        @JvmStatic
        fun getInstance(loginAPI: LoginAPIInterface): LoginRemoteDataSource {
            if (INSTANCE == null) {
                synchronized(LoginRemoteDataSource::javaClass) {
                    INSTANCE = LoginRemoteDataSource(loginAPI)
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