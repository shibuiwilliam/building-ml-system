package com.example.aianimals.login

import androidx.lifecycle.LiveData
import com.example.aianimals.BasePresenter
import com.example.aianimals.BaseView

interface LoginContract {
    interface Presenter : BasePresenter {
        val loginResult: LiveData<LoginResult>
        var isLoggedIn: Boolean
        fun login(
            handleName: String,
            password: String
        )

        fun isLoggedIn()
    }

    interface View : BaseView<Presenter> {
        fun show()
        fun login()
    }
}