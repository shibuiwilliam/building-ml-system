package com.example.aianimals.login

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData

class LoginPresenter(
    private val loginView: LoginContract.View
):LoginContract.Presenter {

    private val _loginResult = MutableLiveData<LoginResult>()
    override val loginResult: LiveData<LoginResult> = _loginResult

    init {
        this.loginView.presenter=this
    }

    override fun start() {
        this.loginView.show()
    }

    override fun login(id: String, password: String) {
        val result = true

        if (result) {
            _loginResult.value = LoginResult(success=1)
        } else {
            _loginResult.value= LoginResult(error=1)
        }
    }
}