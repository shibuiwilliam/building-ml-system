package com.example.aianimals.services.login

import android.content.Context
import android.content.Intent
import com.example.aianimals.core.platform.BaseActivity

class LoginActivity : BaseActivity() {
    companion object {
        fun callingIntent(context: Context) = Intent(context, LoginActivity::class.java)
    }

    override fun fragment() = LoginFragment()
}
