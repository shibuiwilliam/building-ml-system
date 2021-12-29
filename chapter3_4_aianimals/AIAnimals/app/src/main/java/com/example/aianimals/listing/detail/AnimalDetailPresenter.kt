package com.example.aianimals.listing.detail

import com.example.aianimals.repository.animal.Animal
import com.example.aianimals.repository.animal.source.AnimalDataSource
import com.example.aianimals.repository.animal.source.AnimalRepository

class AnimalDetailPresenter(
    private val animalID: String,
    private val animalRepository: AnimalRepository,
    private val animalDetailView: AnimalDetailContract.View
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
}