package com.example.aianimals.repository.login.source.local

import android.util.Log
import androidx.annotation.VisibleForTesting
import com.example.aianimals.middleware.AppExecutors
import com.example.aianimals.repository.login.Login
import com.example.aianimals.repository.login.source.LoginDataSource
import com.example.aianimals.repository.login.source.Result
import kotlinx.coroutines.withContext

class LoginLocalDataSource private constructor(
    val appExecutors: AppExecutors,
    val loginDao: LoginDao
) : LoginDataSource {
    private val TAG = LoginLocalDataSource::class.java.simpleName

    override suspend fun login(
        handleName: String,
        password: String
    ): Result<Login> {
        return Result.Error(Exception())
    }

    suspend fun login(login: Login): Result<Login> {
        var currentLogin: Login? = null
        withContext(appExecutors.ioContext) {
            loginDao.insertLogin(login)
            currentLogin = loginDao.getLogin(login.id)
            Log.i(TAG, "login as ${currentLogin}")
        }
        return Result.Success(login)
    }

    override suspend fun logout() {}

    suspend fun logout(login: Login) {
        withContext(appExecutors.ioContext) {
            loginDao.deleteLogin(login)
            Log.i(TAG, "logout")
        }
    }

    override suspend fun isLoggedIn(): Login? {
        var currentLogin: Login? = null
        withContext(appExecutors.ioContext) {
            currentLogin = loginDao.getLogin(0)
            Log.i(TAG, "login as ${currentLogin}")
        }
        return currentLogin
    }

    companion object {
        private var INSTANCE: LoginLocalDataSource? = null

        @JvmStatic
        fun getInstance(
            appExecutors: AppExecutors,
            loginDao: LoginDao
        ): LoginLocalDataSource {
            if (INSTANCE == null) {
                synchronized(LoginLocalDataSource::javaClass) {
                    INSTANCE = LoginLocalDataSource(appExecutors, loginDao)
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