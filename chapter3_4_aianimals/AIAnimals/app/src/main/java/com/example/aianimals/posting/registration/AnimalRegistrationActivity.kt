package com.example.aianimals.posting.registration

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.MenuItem
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.GravityCompat
import androidx.drawerlayout.widget.DrawerLayout
import com.example.aianimals.Injection
import com.example.aianimals.R
import com.example.aianimals.listing.listing.AnimalListActivity
import com.example.aianimals.middleware.setupActionBar
import com.google.android.material.navigation.NavigationView

class AnimalRegistrationActivity : AppCompatActivity() {
    private val TAG = AnimalRegistrationActivity::class.java.simpleName

    private lateinit var animalRegistrationPresenter: AnimalRegistrationPresenter

    private lateinit var drawerLayout: DrawerLayout
    private lateinit var navigationView: NavigationView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.animal_registration_activity)

        setupActionBar(R.id.toolbar) {
            setHomeAsUpIndicator(R.drawable.ic_menu)
            setDisplayHomeAsUpEnabled(true)
        }

        drawerLayout=findViewById(R.id.drawer_layout)
        navigationView = findViewById(R.id.navigation_view)
        navigationView.setNavigationItemSelectedListener { menuItem ->
            if (menuItem.itemId == R.id.list_animal) {
                val intent = Intent(
                    this@AnimalRegistrationActivity,
                    AnimalListActivity::class.java)
                startActivity(intent)
            }
            menuItem.isChecked = true
            drawerLayout.closeDrawers()
            true
        }

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
        if (ANIMAL_NAME != null) {
            animalRegistrationPresenter.setAnimalName(ANIMAL_NAME)
        }
        if (ANIMAL_DESCRIPTION != null) {
            animalRegistrationPresenter.setAnimalDescription(ANIMAL_DESCRIPTION)
        }
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState.apply {
            putString(ANIMAL_NAME, animalRegistrationPresenter.getAnimalName())
            putString(ANIMAL_DESCRIPTION, animalRegistrationPresenter.getAnimalDescription())
        })
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        if (item.itemId == android.R.id.home) {
            drawerLayout.openDrawer(GravityCompat.START)
            return true
        }
        return super.onOptionsItemSelected(item)
    }

    companion object {
        val IMAGE_URI: String? = null

        private val ANIMAL_NAME: String? = null
        private val ANIMAL_DESCRIPTION: String? = null
    }
}