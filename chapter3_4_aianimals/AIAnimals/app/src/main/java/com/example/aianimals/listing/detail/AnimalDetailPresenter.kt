package com.example.aianimals.listing.detail

import com.example.aianimals.middleware.AppExecutors
import com.example.aianimals.repository.animal.Animal
import com.example.aianimals.repository.animal.source.AnimalRepository
import com.example.aianimals.repository.login.source.LoginRepository
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.withContext

class AnimalDetailPresenter(
    private val animalID: String,
    private val animalRepository: AnimalRepository,
    private val loginRepository: LoginRepository,
    private val animalDetailView: AnimalDetailContract.View,
    private val appExecutors: AppExecutors = AppExecutors()
) : AnimalDetailContract.Presenter {

    override var animal: Animal? = null

    init {
        this.animalDetailView.presenter = this
    }

    override fun start() {
        getAnimal(this.animalID)
    }

    override fun getAnimal(animalID: String) = runBlocking {
        withContext(appExecutors.ioContext) {
            animal = animalRepository.getAnimal(animalID)
        }
        if (animal != null) {
            animalDetailView.showAnimal(animal!!)
        }
    }

    override fun likeAnimal(animal: Animal) = runBlocking {
        animalRepository.likeAnimal(animal.id)
    }

    override fun logout() = runBlocking {
        withContext(appExecutors.defaultContext) {
            loginRepository.logout()
        }
    }
}