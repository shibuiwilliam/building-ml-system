package com.example.aianimals.services.animal.listing

import android.content.Context
import android.content.Intent
import com.example.aianimals.core.platform.BaseActivity

class AnimalsActivity : BaseActivity() {

    companion object {
        fun callingIntent(context: Context) = Intent(context, AnimalsActivity::class.java)
    }

    override fun fragment() = AnimalsFragment()
}
