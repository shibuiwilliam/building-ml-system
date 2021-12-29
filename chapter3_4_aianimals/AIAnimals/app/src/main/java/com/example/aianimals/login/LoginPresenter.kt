package com.example.aianimals.login

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import com.example.aianimals.repository.login.source.LoginRepository
import com.example.aianimals.repository.login.source.Result

class LoginPresenter(
    private val loginView: LoginContract.View,
    private val loginRepository: LoginRepository
) : LoginContract.Presenter {

    private val _loginResult = MutableLiveData<LoginResult>()
    override val loginResult: LiveData<LoginResult> = _loginResult

    init {
        this.loginView.presenter = this
    }

    override fun start() {
        this.loginView.show()
    }

    override fun login(id: String, password: String) {
        val result = loginRepository.login(id, password)

        if (result is Result.Success) {
            _loginResult.value = LoginResult(success = 1)
        } else {
            _loginResult.value = LoginResult(error = 1)
        }
    }
}