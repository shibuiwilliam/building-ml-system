package com.example.aianimals.repository.login.source.remote

import android.util.Log
import androidx.annotation.VisibleForTesting
import com.example.aianimals.middleware.AppExecutors
import com.example.aianimals.repository.login.Login
import com.example.aianimals.repository.login.source.LoginDataSource
import com.example.aianimals.repository.login.source.Result
import kotlinx.coroutines.withContext
import java.util.*

class LoginRemoteDataSource private constructor(
    val appExecutors: AppExecutors,
    val loginAPI: LoginAPIInterface
) : LoginDataSource {
    private val TAG = LoginRemoteDataSource::class.java.simpleName

    override suspend fun login(
        handleName: String,
        password: String
    ): Result<Login> {
        var login: Login? = null
        withContext(appExecutors.ioContext) {
            val response = loginAPI.postLogin(LoginPost(handleName, password))
            if (response.isSuccessful) {
                login = Login(
                    id = 0,
                    handleName = handleName,
                    emailAddress = "",
                    token = response.body()!!.token,
                    lastLoginAt = Date()
                )
            }
        }
        if (login == null) {
            Log.e(TAG, "login failed")
            return Result.Error(Exception("failed to login"))
        }
        Log.i(TAG, "login succeeded")
        return Result.Success(login!!)
    }

    override suspend fun logout() {
    }

    override suspend fun isLoggedIn(): Login? {
        return null
    }

    companion object {
        private var INSTANCE: LoginRemoteDataSource? = null

        @JvmStatic
        fun getInstance(
            appExecutors: AppExecutors,
            loginAPI: LoginAPIInterface
        ): LoginRemoteDataSource {
            if (INSTANCE == null) {
                synchronized(LoginRemoteDataSource::javaClass) {
                    INSTANCE = LoginRemoteDataSource(appExecutors, loginAPI)
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