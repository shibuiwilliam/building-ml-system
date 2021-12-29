package com.example.aianimals.repository.login.source


import com.example.aianimals.repository.login.Login
import com.example.aianimals.repository.login.source.local.LoginLocalDataSource

class LoginRepository(
    val loginLocalDataSource: LoginLocalDataSource
) : LoginDataSource {
    private val TAG = LoginRepository::class.java.simpleName

    override fun login(
        id: String,
        password: String
    ): Result<Login> {
        return loginLocalDataSource.login(id, password)
    }

    companion object {
        private var INSTANCE: LoginRepository? = null

        @JvmStatic
        fun getInstance(
            loginLocalDataSource: LoginLocalDataSource
        ): LoginRepository {
            return INSTANCE ?: LoginRepository(loginLocalDataSource)
                .apply { INSTANCE = this }
        }

        @JvmStatic
        fun destroyInstance() {
            INSTANCE = null
        }
    }
}