package com.example.aianimals.posting.confirmation

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
import com.example.aianimals.repository.animal.Animal
import com.google.android.material.navigation.NavigationView

class ConfirmationActivity : AppCompatActivity() {
    private val TAG = ConfirmationActivity::class.java.simpleName

    private lateinit var confirmationPresenter: ConfirmationPresenter

    private lateinit var drawerLayout: DrawerLayout
    private lateinit var navigationView: NavigationView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.confirmation_activity)

        setupActionBar(R.id.toolbar) {
            setHomeAsUpIndicator(R.drawable.ic_menu)
            setDisplayHomeAsUpEnabled(true)
        }

        drawerLayout = findViewById(R.id.drawer_layout)
        navigationView = findViewById(R.id.navigation_view)
        navigationView.setNavigationItemSelectedListener { menuItem ->
            if (menuItem.itemId == R.id.list_animal) {
                val intent = Intent(
                    this@ConfirmationActivity,
                    AnimalListActivity::class.java
                )
                startActivity(intent)
            }
            menuItem.isChecked = true
            drawerLayout.closeDrawers()
            true
        }

        val confirmationFragment = supportFragmentManager
            .findFragmentById(R.id.confirmation_activity_frame) as ConfirmationFragment?
            ?: ConfirmationFragment.newInstance().also {
                supportFragmentManager
                    .beginTransaction()
                    .replace(R.id.confirmation_activity_frame, it)
                    .commit()
            }

        confirmationPresenter = ConfirmationPresenter(
            ANIMAL!!,
            Injection.provideAnimalRepository(applicationContext),
            confirmationFragment
        )
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState.apply {
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
        private val ANIMAL: Animal? = null
    }
}