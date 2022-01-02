package com.example.aianimals.listing.detail

import com.example.aianimals.repository.animal.Animal
import com.example.aianimals.repository.animal.source.AnimalDataSource
import com.example.aianimals.repository.animal.source.AnimalRepository
import com.example.aianimals.repository.login.source.LoginRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.withContext
import kotlin.coroutines.CoroutineContext

class AnimalDetailPresenter(
    private val animalID: String,
    private val animalRepository: AnimalRepository,
    private val loginRepository: LoginRepository,
    private val animalDetailView: AnimalDetailContract.View,
    private val context: CoroutineContext = Dispatchers.Default
) : AnimalDetailContract.Presenter {
    init {
        this.animalDetailView.presenter = this
    }

    override fun start() {
        getAnimal(this.animalID)
    }

    override fun getAnimal(animalID: String) {
        this.animalRepository.getAnimal(
            animalID,
            object : AnimalDataSource.GetAnimalCallback {
                override fun onGetAnimal(animal: Animal) {
                    animalDetailView.showAnimal(animal)
                }

                override fun onDataNotAvailable() {
                }
            })
    }

    override fun logout() = runBlocking {
        withContext(context) {
            loginRepository.logout()
        }
    }
}