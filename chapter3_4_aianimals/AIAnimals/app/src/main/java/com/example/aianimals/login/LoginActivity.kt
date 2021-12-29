package com.example.aianimals.login

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import com.example.aianimals.R

class LoginActivity : AppCompatActivity() {
    private val TAG = LoginActivity::class.java.simpleName

    private lateinit var loginPresenter: LoginPresenter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.login_activity)

        val loginFragment = supportFragmentManager
            .findFragmentById(R.id.login_activity_frame)
        as LoginFragment? ?: LoginFragment.newInstance().also {
            supportFragmentManager
                .beginTransaction()
                .replace(R.id.login_activity_frame, it)
                .commit()
        }

        loginPresenter = LoginPresenter(
            loginFragment
        )
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState.apply {
            putString(LOGIN_USER, "")
        })
    }

    companion object{
        private val LOGIN_USER: String? = null
    }
}