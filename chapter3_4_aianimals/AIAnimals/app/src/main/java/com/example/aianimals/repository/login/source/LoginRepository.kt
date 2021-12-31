package com.example.aianimals.repository.login.source


import com.example.aianimals.repository.login.Login
import com.example.aianimals.repository.login.source.local.LoginLocalDataSource
import com.example.aianimals.repository.login.source.remote.LoginRemoteDataSource
import java.util.*

class LoginRepository(
    val loginLocalDataSource: LoginLocalDataSource,
    val loginRemoteDataSource: LoginRemoteDataSource
) : LoginDataSource {
    private val TAG = LoginRepository::class.java.simpleName

    var login: Login? = null
        private set

    val isLoggedIn: Boolean
        get() = this.login != null

    init {
        this.login = null
    }

    override fun login(
        userID: String,
        password: String,
    ): Result<Login> {
        val login = Login(
            id = 0,
            userID = "a",
            displayName = "b",
            token = "",
            lastLoginAt = Date()
        )
        this.login = login
        return loginLocalDataSource.login(login)
    }

    override fun logout() {
        if (!isLoggedIn) {
            return
        }
        loginLocalDataSource.logout(this.login!!)
        this.login = null
    }

    companion object {
        private var INSTANCE: LoginRepository? = null

        @JvmStatic
        fun getInstance(
            loginLocalDataSource: LoginLocalDataSource,
            loginRemoteDataSource: LoginRemoteDataSource
        ): LoginRepository {
            return INSTANCE ?: LoginRepository(
                loginLocalDataSource,
                loginRemoteDataSource
            )
                .apply { INSTANCE = this }
        }

        @JvmStatic
        fun destroyInstance() {
            INSTANCE = null
        }
    }
}