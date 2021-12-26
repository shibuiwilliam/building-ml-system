package com.example.aianimals.listing

import android.os.Bundle
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import com.example.aianimals.R
import com.example.aianimals.repository.source.AnimalRepository

class AnimalListActivity : AppCompatActivity() {
    private val CURRENT_FILTERING_KEY = "CURRENT_FILTERING_KEY"
    private lateinit var animalListPresenter: AnimalListPresenter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.animal_list_activity)

        val animalListFragment = supportFragmentManager
            .findFragmentById(R.id.flagment_activity_main)
                as AnimalListFragment? ?:AnimalListFragment.newInstance().also{
                    supportFragmentManager
                        .beginTransaction()
                        .replace(R.id.flagment_activity_main, it)
                        .commit()
        }

        animalListPresenter = AnimalListPresenter(
            AnimalRepository(),
            animalListFragment)
    }

    public override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState.apply {
            putSerializable(CURRENT_FILTERING_KEY, null)
        })
    }
}