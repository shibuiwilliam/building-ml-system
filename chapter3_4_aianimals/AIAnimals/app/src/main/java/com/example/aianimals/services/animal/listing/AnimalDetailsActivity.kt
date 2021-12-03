package com.example.aianimals.services.animal.listing

import android.content.Context
import android.content.Intent
import com.example.aianimals.core.platform.BaseActivity

class AnimalDetailsActivity : BaseActivity() {

    companion object {
        private const val INTENT_EXTRA_PARAM_ANIMAL = "com.example.aianimals.INTENT_PARAM_ANIMAL"

        fun callingIntent(context: Context, animal: AnimalView) =
            Intent(context, AnimalDetailsActivity::class.java).apply {
                putExtra(INTENT_EXTRA_PARAM_ANIMAL, animal)
            }
    }

    override fun fragment() =
        AnimalDetailsFragment.forAnimal(intent.getParcelableExtra(INTENT_EXTRA_PARAM_ANIMAL))
}
