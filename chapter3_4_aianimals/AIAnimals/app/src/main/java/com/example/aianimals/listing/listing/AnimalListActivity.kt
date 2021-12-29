package com.example.aianimals.listing.listing

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.example.aianimals.Injection
import com.example.aianimals.R

class AnimalListActivity : AppCompatActivity() {
    private val TAG = AnimalListActivity::class.java.simpleName

    private val CURRENT_FILTERING_KEY = "CURRENT_FILTERING_KEY"
    private lateinit var animalListPresenter: AnimalListPresenter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.animal_list_activity)

        val animalListFragment = supportFragmentManager
            .findFragmentById(R.id.animal_list_activity_frame)
                as AnimalListFragment? ?: AnimalListFragment.newInstance().also {
            supportFragmentManager
                .beginTransaction()
                .replace(R.id.animal_list_activity_frame, it)
                .commit()
        }

        animalListPresenter = AnimalListPresenter(
            Injection.provideAnimalRepository(applicationContext),
            animalListFragment
        )
    }

    public override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState.apply {
            putSerializable(CURRENT_FILTERING_KEY, null)
        })
    }
}