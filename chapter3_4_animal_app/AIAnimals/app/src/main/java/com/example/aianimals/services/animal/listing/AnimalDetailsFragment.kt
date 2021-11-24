package com.example.aianimals.services.animal.listing

import android.os.Bundle
import android.view.View
import androidx.core.os.bundleOf
import androidx.fragment.app.viewModels
import com.example.aianimals.R
import com.example.aianimals.core.exception.Failure
import com.example.aianimals.core.extension.*
import com.example.aianimals.core.platform.BaseFragment
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.android.synthetic.main.fragment_animal_details.*
import kotlinx.android.synthetic.main.toolbar.*
import javax.inject.Inject

@AndroidEntryPoint
class AnimalDetailsFragment : BaseFragment() {

    companion object {
        private const val PARAM_ANIMAL = "param_animal"

        fun forAnimal(animal: AnimalView?) = AnimalDetailsFragment().apply {
            arguments = bundleOf(PARAM_ANIMAL to animal)
        }
    }

    @Inject
    lateinit var animalDetailsAnimator: AnimalDetailsAnimator

    private val animalDetailsViewModel by viewModels<AnimalDetailsViewModel>()

    override fun layoutId() = R.layout.fragment_animal_details

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        activity?.let { animalDetailsAnimator.postponeEnterTransition(it) }

        with(animalDetailsViewModel) {
            observe(animalDetails, ::renderAnimalDetails)
            failure(failure, ::handleFailure)
        }
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        if (firstTimeCreated(savedInstanceState)) {
            animalDetailsViewModel.loadAnimalDetails((arguments?.get(PARAM_ANIMAL) as AnimalView).id)
        } else {
            animalDetailsAnimator.scaleUpView(animalPlay)
            animalDetailsAnimator.cancelTransition(animalPoster)
            animalPoster.loadFromUrl((requireArguments()[PARAM_ANIMAL] as AnimalView).poster)
        }
    }

    override fun onBackPressed() {
        animalDetailsAnimator.fadeInvisible(scrollView, animalDetails)
        if (animalPlay.isVisible())
            animalDetailsAnimator.scaleDownView(animalPlay)
        else
            animalDetailsAnimator.cancelTransition(animalPoster)
    }

    private fun renderAnimalDetails(animal: AnimalDetailsView?) {
        animal?.let {
            with(animal) {
                activity?.let {
                    animalPoster.loadUrlAndPostponeEnterTransition(poster, it)
                    it.toolbar.title = title
                }
                animalSummary.text = summary
                animalCast.text = cast
                animalDirector.text = director
                animalYear.text = year.toString()
                animalPlay.setOnClickListener { animalDetailsViewModel.playAnimal(trailer) }
            }
        }
        animalDetailsAnimator.fadeVisible(scrollView, animalDetails)
        animalDetailsAnimator.scaleUpView(animalPlay)
    }

    private fun handleFailure(failure: Failure?) {
        when (failure) {
            is Failure.NetworkConnection -> {
                notify(R.string.failure_network_connection); close()
            }
            is Failure.ServerError -> {
                notify(R.string.failure_server_error); close()
            }
            is AnimalFailure.NonExistentAnimal -> {
                notify(R.string.failure_animal_non_existent); close()
            }
            else -> {
                notify(R.string.failure_server_error); close()
            }
        }
    }
}
