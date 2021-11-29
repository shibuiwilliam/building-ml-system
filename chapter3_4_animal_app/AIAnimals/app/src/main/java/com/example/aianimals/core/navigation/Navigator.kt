package com.example.aianimals.core.navigation

import android.content.Context
import android.view.View
import android.widget.ImageView
import androidx.core.app.ActivityOptionsCompat
import androidx.fragment.app.FragmentActivity
import com.example.aianimals.services.animal.listing.AnimalDetailsActivity
import com.example.aianimals.services.animal.listing.AnimalView
import com.example.aianimals.services.animal.listing.AnimalsActivity
import com.example.aianimals.services.login.Authenticator
import com.example.aianimals.services.login.LoginActivity
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class Navigator
@Inject constructor(private val authenticator: Authenticator) {

    private fun showLogin(context: Context) =
        context.startActivity(LoginActivity.callingIntent(context))

    fun showMain(context: Context) {
        when (authenticator.userLoggedIn()) {
            true -> showAnimals(context)
            false -> showLogin(context)
        }
    }

    private fun showAnimals(context: Context) =
        context.startActivity(AnimalsActivity.callingIntent(context))

    fun showAnimalDetails(
        activity: FragmentActivity,
        animal: AnimalView,
        navigationExtras: Extras
    ) {
        val intent = AnimalDetailsActivity.callingIntent(activity, animal)
        val sharedView = navigationExtras.transitionSharedElement as ImageView
        val activityOptions = ActivityOptionsCompat
            .makeSceneTransitionAnimation(activity, sharedView, sharedView.transitionName)
        activity.startActivity(intent, activityOptions.toBundle())
    }

    class Extras(val transitionSharedElement: View)
}


