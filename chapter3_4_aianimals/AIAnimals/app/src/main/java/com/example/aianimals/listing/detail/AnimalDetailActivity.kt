package com.example.aianimals.listing.detail

import android.content.Intent
import android.os.Bundle
import android.view.MenuItem
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.GravityCompat
import androidx.drawerlayout.widget.DrawerLayout
import com.example.aianimals.Injection
import com.example.aianimals.R
import com.example.aianimals.listing.listing.AnimalListActivity
import com.example.aianimals.middleware.setupActionBar
import com.example.aianimals.posting.registration.AnimalRegistrationActivity
import com.google.android.material.navigation.NavigationView

class AnimalDetailActivity : AppCompatActivity() {
    private lateinit var animalDetailPresenter: AnimalDetailPresenter

    private lateinit var drawerLayout: DrawerLayout
    private lateinit var navigationView: NavigationView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.animal_detail_activity)

        setupActionBar(R.id.toolbar) {
            setHomeAsUpIndicator(R.drawable.ic_menu)
            setDisplayHomeAsUpEnabled(true)
        }

        drawerLayout = findViewById(R.id.drawer_layout)
        navigationView = findViewById(R.id.navigation_view)
        navigationView.setNavigationItemSelectedListener { menuItem ->
            if (menuItem.itemId == R.id.register_animal) {
                val intent = Intent(
                    this@AnimalDetailActivity,
                    AnimalRegistrationActivity::class.java
                )
                startActivity(intent)
            }
            if (menuItem.itemId == R.id.list_animal) {
                val intent = Intent(
                    this@AnimalDetailActivity,
                    AnimalListActivity::class.java
                )
                startActivity(intent)
            }
            menuItem.isChecked = true
            drawerLayout.closeDrawers()
            true
        }

        val animalID = intent.getStringExtra(EXTRA_ANIMAL_ID)!!

        val animalDetailFragment = supportFragmentManager
            .findFragmentById(R.id.animal_detail_activity) as AnimalDetailFragment?
            ?: AnimalDetailFragment.newInstance(animalID).also {
                supportFragmentManager
                    .beginTransaction()
                    .replace(R.id.animal_detail_activity, it)
                    .commit()
            }

        animalDetailPresenter = AnimalDetailPresenter(
            animalID,
            Injection.provideAnimalRepository(applicationContext),
            animalDetailFragment
        )
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        if (item.itemId == android.R.id.home) {
            drawerLayout.openDrawer(GravityCompat.START)
            return true
        }
        return super.onOptionsItemSelected(item)
    }

    companion object {
        const val EXTRA_ANIMAL_ID = "ANIMAL_ID"
    }
}