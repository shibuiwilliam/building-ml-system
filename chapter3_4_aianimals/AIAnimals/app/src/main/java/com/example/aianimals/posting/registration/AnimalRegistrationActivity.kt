package com.example.aianimals.posting.registration

import android.os.Bundle
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import com.example.aianimals.Injection
import com.example.aianimals.R

class AnimalRegistrationActivity : AppCompatActivity() {
    private val TAG = AnimalRegistrationActivity::class.java.simpleName

    private lateinit var animalRegistrationPresenter: AnimalRegistrationPresenter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.animal_registration_activity)

        val imageUri = intent.getStringExtra(IMAGE_URI)
        Log.i(TAG, "registering image: ${imageUri}")

        val animalRegistrationFragment = supportFragmentManager
            .findFragmentById(R.id.animal_registration_activity_frame)
                as AnimalRegistrationFragment?
            ?: AnimalRegistrationFragment.newInstance(imageUri).also {
                supportFragmentManager
                    .beginTransaction()
                    .replace(R.id.animal_registration_activity_frame, it)
                    .commit()
            }

        animalRegistrationPresenter = AnimalRegistrationPresenter(
            imageUri,
            Injection.provideAnimalRepository(applicationContext),
            animalRegistrationFragment
        )
    }

    companion object {
        val IMAGE_URI: String? = null
    }
}