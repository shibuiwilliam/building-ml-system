package com.example.aianimals.listing.detail

import com.example.aianimals.repository.Animal
import com.example.aianimals.repository.source.AnimalDataSource
import com.example.aianimals.repository.source.AnimalRepository

class AnimalDetailPresenter(
    private val animalID: Int,
    val animalRepository: AnimalRepository,
    val animalDetailView: AnimalDetailContract.View
) : AnimalDetailContract.Presenter{
    init {
        this.animalDetailView.presenter = this
    }

    override fun start() {
        getAnimal(this.animalID)
    }

    override fun getAnimal(animalID: Int) {
        this.animalRepository.getAnimal(animalID, object : AnimalDataSource.GetAnimalCallback{
            override fun onGetAnimal(animal: Animal) {
                animalDetailView.showAnimal(animal)
            }
        })
    }
}