package com.example.aianimals.login

import android.util.Log
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import com.example.aianimals.middleware.AppExecutors
import com.example.aianimals.repository.access_log.source.AccessLogRepository
import com.example.aianimals.repository.animal.source.AnimalRepository
import com.example.aianimals.repository.login.source.LoginRepository
import com.example.aianimals.repository.login.source.Result
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.withContext

class LoginPresenter(
    private val loginView: LoginContract.View,
    private val loginRepository: LoginRepository,
    private val animalRepository: AnimalRepository,
    private val accessLogRepository: AccessLogRepository,
    private val appExecutors: AppExecutors = AppExecutors()
) : LoginContract.Presenter {
    private val TAG = LoginPresenter::class.java.simpleName

    private val _loginResult = MutableLiveData<LoginResult>()
    override val loginResult: LiveData<LoginResult> = _loginResult

    override var isLoggedIn: Boolean = false

    init {
        this.loginView.presenter = this
        isLoggedIn()
    }

    override fun start() {
        loginView.show()
        isLoggedIn()
    }

    override fun login(
        handleName: String,
        password: String
    ) = runBlocking {
        withContext(appExecutors.defaultContext) {
            val result = loginRepository.login(handleName, password)
            if (result is Result.Success) {
                isLoggedIn = true
                animalRepository.animalRemoteDataSource.setToken(result.data.token)
                animalRepository.animalRemoteDataSource.setUserID(result.data.userID)
                accessLogRepository.accessLogRemoteDataSource.setToken(result.data.token)
                _loginResult.postValue(LoginResult(success = 1))
            } else {
                isLoggedIn = false
                _loginResult.postValue(LoginResult(error = 1))
            }
        }
    }

    override fun isLoggedIn() = runBlocking {
        withContext(appExecutors.defaultContext) {
            Log.i(TAG, "is logged in?")
            val login = loginRepository.isLoggedIn()
            if (login != null) {
                isLoggedIn = true
                animalRepository.animalRemoteDataSource.setToken(login.token)
                animalRepository.animalRemoteDataSource.setUserID(login.userID)
                accessLogRepository.accessLogRemoteDataSource.setToken(login.token)
                _loginResult.postValue(LoginResult(success = 1))
            }
        }
    }
}