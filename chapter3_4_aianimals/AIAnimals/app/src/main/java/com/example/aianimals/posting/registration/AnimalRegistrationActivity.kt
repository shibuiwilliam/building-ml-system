package com.example.aianimals.posting.registration

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.example.aianimals.Injection
import com.example.aianimals.R

class AnimalRegistrationActivity : AppCompatActivity() {
    private lateinit var animalRegistrationPresenter: AnimalRegistrationPresenter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.animal_registration_activity)

        val animalRegistrationFragment = supportFragmentManager
            .findFragmentById(R.id.animal_registration_activity_frame)
                as AnimalRegistrationFragment? ?: AnimalRegistrationFragment.newInstance().also {
            supportFragmentManager
                .beginTransaction()
                .replace(R.id.animal_registration_activity_frame, it)
                .commit()
        }

        animalRegistrationPresenter = AnimalRegistrationPresenter(
            Injection.provideAnimalRepository(applicationContext),
            animalRegistrationFragment
        )
    }
}