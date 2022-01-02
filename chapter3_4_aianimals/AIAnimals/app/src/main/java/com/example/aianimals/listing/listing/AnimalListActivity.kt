package com.example.aianimals.listing.listing

import android.content.Intent
import android.os.Bundle
import android.view.MenuItem
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.GravityCompat
import androidx.drawerlayout.widget.DrawerLayout
import com.example.aianimals.Injection
import com.example.aianimals.R
import com.example.aianimals.login.LoginActivity
import com.example.aianimals.middleware.setupActionBar
import com.example.aianimals.posting.registration.AnimalRegistrationActivity
import com.google.android.material.navigation.NavigationView

class AnimalListActivity : AppCompatActivity() {
    private val TAG = AnimalListActivity::class.java.simpleName

    private val CURRENT_FILTERING_KEY = "CURRENT_FILTERING_KEY"
    private lateinit var animalListPresenter: AnimalListPresenter

    private lateinit var drawerLayout: DrawerLayout
    private lateinit var navigationView: NavigationView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.animal_list_activity)

        setupActionBar(R.id.toolbar) {
            setHomeAsUpIndicator(R.drawable.ic_menu)
            setDisplayHomeAsUpEnabled(true)
        }

        drawerLayout = findViewById(R.id.drawer_layout)
        navigationView = findViewById(R.id.navigation_view)
        navigationView.setNavigationItemSelectedListener { menuItem ->
            if (menuItem.itemId == R.id.register_animal) {
                val intent = Intent(
                    this@AnimalListActivity,
                    AnimalRegistrationActivity::class.java
                )
                startActivity(intent)
            }
            if (menuItem.itemId == R.id.logout) {
                animalListPresenter.logout()
                val intent = Intent(
                    this@AnimalListActivity,
                    LoginActivity::class.java
                )
                startActivity(intent)
            }
            menuItem.isChecked = true
            drawerLayout.closeDrawers()
            true
        }

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
            Injection.provideLoginRepository(applicationContext),
            animalListFragment
        )
    }

    public override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState.apply {
            putSerializable(CURRENT_FILTERING_KEY, null)
        })
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        if (item.itemId == android.R.id.home) {
            drawerLayout.openDrawer(GravityCompat.START)
            return true
        }
        return super.onOptionsItemSelected(item)
    }
}