package com.example.aianimals.repository.login.source.local

import androidx.annotation.VisibleForTesting
import com.example.aianimals.middleware.AppExecutors
import com.example.aianimals.repository.login.Login
import com.example.aianimals.repository.login.source.LoginDataSource
import com.example.aianimals.repository.login.source.Result

class LoginLocalDataSource private constructor(
    val appExecutors: AppExecutors,
    val loginDao: LoginDao
) : LoginDataSource {
    private val TAG = LoginLocalDataSource::class.java.simpleName

    override fun login(
        userID: String,
        password: String
    ): Result<Login> {
        return Result.Error(Exception())
    }

    fun login(login: Login): Result<Login> {
        appExecutors.diskIO.execute {
            loginDao.insertLogin(login)
        }
        return Result.Success(login)
    }

    override fun logout() {}

    fun logout(login: Login) {
        appExecutors.diskIO.execute {
            loginDao.deleteLogin(login)
        }
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