package com.example.aianimals.listing.detail

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.example.aianimals.Injection
import com.example.aianimals.R

class AnimalDetailActivity : AppCompatActivity() {
    private lateinit var animalDetailPresenter: AnimalDetailPresenter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.animal_detail_activity)

        val animalID = intent.getStringExtra(EXTRA_ANIMAL_ID)!!

        val animalDetailFragment = supportFragmentManager
            .findFragmentById(R.id.animal_detail_activity_frame) as AnimalDetailFragment?
            ?: AnimalDetailFragment.newInstance(animalID).also {
                supportFragmentManager
                    .beginTransaction()
                    .replace(R.id.animal_detail_activity_frame, it)
                    .commit()
            }

        animalDetailPresenter = AnimalDetailPresenter(
            animalID,
            Injection.provideAnimalRepository(applicationContext),
            animalDetailFragment
        )
    }

    companion object {
        const val EXTRA_ANIMAL_ID = "ANIMAL_ID"
    }
}