package com.example.aianimals.repository.login.source


import com.example.aianimals.repository.login.Login
import com.example.aianimals.repository.login.source.local.LoginLocalDataSource
import com.example.aianimals.repository.login.source.remote.LoginRemoteDataSource


class LoginRepository(
    val loginLocalDataSource: LoginLocalDataSource,
    val loginRemoteDataSource: LoginRemoteDataSource
) : LoginDataSource {
    private val TAG = LoginRepository::class.java.simpleName

    var login: Login? = null
        private set

    init {
        this.login = null
    }

    override suspend fun login(
        handleName: String,
        password: String,
    ): Result<Login> {
        val result = loginRemoteDataSource.login(handleName, password)
        val login = result.getLogin()
        return when (result) {
            is Result.Success<*> -> {
                this.login = login
                loginLocalDataSource.login(this.login!!)
            }
            is Result.Error -> result
        }
    }

    override suspend fun logout() {
        if (isLoggedIn() == null) {
            return
        }
        loginLocalDataSource.logout(this.login!!)
        this.login = null
    }

    override suspend fun isLoggedIn(): Login? {
        if (this.login != null) {
            return this.login
        }
        this.login = loginLocalDataSource.isLoggedIn()
        return this.login
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