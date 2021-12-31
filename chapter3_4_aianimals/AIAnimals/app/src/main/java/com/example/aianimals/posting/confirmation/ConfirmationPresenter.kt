package com.example.aianimals.posting.confirmation

import com.example.aianimals.repository.animal.Animal
import com.example.aianimals.repository.animal.source.AnimalRepository

class ConfirmationPresenter(
    private val animal: Animal,
    private val animalRepository: AnimalRepository,
    private val confirmationView: ConfirmationContract.View
) : ConfirmationContract.Presenter {
    init {
        this.confirmationView.presenter = this
    }

    override fun start() {
        showAnimal()
    }

    override fun showAnimal() {
        confirmationView.showAnimal(animal)
    }

    override fun confirmRegistration() {
    }

    override fun cancelRegistration() {
    }
}