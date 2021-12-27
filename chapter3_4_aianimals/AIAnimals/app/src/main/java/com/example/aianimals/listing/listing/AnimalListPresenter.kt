package com.example.aianimals.listing.listing

import com.example.aianimals.repository.Animal
import com.example.aianimals.repository.source.AnimalDataSource
import com.example.aianimals.repository.source.AnimalRepository

class AnimalListPresenter(
    val animalRepository: AnimalRepository,
    val animalListView: AnimalListContract.View
) : AnimalListContract.Presenter {
    init {
        this.animalListView.presenter = this
    }

    override fun start() {
        listAnimals()
    }

    override fun listAnimals() {
        this.animalRepository.listAnimals(object : AnimalDataSource.ListAnimalsCallback {
            override fun onListAnimal(animals: Map<Int, Animal>) {
                animalListView.showAnimals(animals)
            }

            override fun onDataNotAvailable() {
            }
        })
    }
}