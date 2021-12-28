package com.example.aianimals.listing.listing

import com.example.aianimals.repository.Animal
import com.example.aianimals.repository.source.AnimalDataSource
import com.example.aianimals.repository.source.AnimalRepository

class AnimalListPresenter(
    private val animalRepository: AnimalRepository,
    private val animalListView: AnimalListContract.View
) : AnimalListContract.Presenter {
    init {
        this.animalListView.presenter = this
    }

    override fun start() {
        listAnimals()
    }

    override fun listAnimals() {
        this.animalRepository.listAnimals(object : AnimalDataSource.ListAnimalsCallback {
            override fun onListAnimal(animals: Map<String, Animal>) {
                animalListView.showAnimals(animals)
            }

            override fun onDataNotAvailable() {
            }
        })
    }
}