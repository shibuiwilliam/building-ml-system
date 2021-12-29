package com.example.aianimals.login

import androidx.lifecycle.LiveData
import com.example.aianimals.BasePresenter
import com.example.aianimals.BaseView

interface LoginContract {
    interface Presenter: BasePresenter{
        val loginResult: LiveData<LoginResult>
        fun login(id: String, password: String)
    }

    interface View: BaseView<Presenter>{
        fun show()
        fun login()
    }
}