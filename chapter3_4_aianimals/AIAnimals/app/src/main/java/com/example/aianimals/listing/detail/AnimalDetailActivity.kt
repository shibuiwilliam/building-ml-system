package com.example.aianimals.listing.detail

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
import com.example.aianimals.login.LoginActivity
import com.example.aianimals.middleware.setupActionBar
import com.example.aianimals.posting.registration.AnimalRegistrationActivity
import com.google.android.material.navigation.NavigationView

class AnimalDetailActivity : AppCompatActivity() {
    private val TAG = AnimalDetailActivity::class.java.simpleName

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
            Injection.provideLoginRepository(applicationContext),
            Injection.provideAccessLogReposiotry(applicationContext),
            animalDetailFragment
        )
        animalDetailPresenter.queryString = intent.getStringExtra(EXTRA_QUERY_STRING)
        animalDetailPresenter.queryAnimalCategory = intent.getStringExtra(EXTRA_QUERY_ANIMAL_CATEGORY)!!
        animalDetailPresenter.queryAnimalSubcategory = intent.getStringExtra(EXTRA_QUERY_ANIMAL_SUBCATEGORY)!!

        drawerLayout = findViewById(R.id.drawer_layout)
        navigationView = findViewById(R.id.navigation_view)
        navigationView.setNavigationItemSelectedListener { menuItem ->
            if (menuItem.itemId == R.id.register_animal) {
                animalDetailPresenter.stayLong(animalDetailPresenter.animal!!)
                val intent = Intent(
                    this@AnimalDetailActivity,
                    AnimalRegistrationActivity::class.java
                )
                startActivity(intent)
            }
            if (menuItem.itemId == R.id.list_animal) {
                animalDetailPresenter.stayLong(animalDetailPresenter.animal!!)
                val intent = Intent(
                    this@AnimalDetailActivity,
                    AnimalListActivity::class.java
                )
                startActivity(intent)
            }
            if (menuItem.itemId == R.id.logout) {
                animalDetailPresenter.stayLong(animalDetailPresenter.animal!!)
                animalDetailPresenter.logout()
                val intent = Intent(
                    this@AnimalDetailActivity,
                    LoginActivity::class.java
                )
                startActivity(intent)
            }
            menuItem.isChecked = true
            drawerLayout.closeDrawers()
            true
        }
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
        const val EXTRA_QUERY_STRING: String = "QUERY_STRING"
        const val EXTRA_QUERY_ANIMAL_CATEGORY: String = "QUERY_ANIMAL_CATEGORY"
        const val EXTRA_QUERY_ANIMAL_SUBCATEGORY: String = "QUERY_ANIMAL_SUBCATEGORY"
    }
}